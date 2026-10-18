#!/bin/bash
# ---------------------------------------------------------------------------
# run_assembly_microbench.sh - Compila (si hace falta) y perfila con RAVE los
#   microbenchmarks de ensamblador de rvv-evaluation. Guarda un JSON por kernel
#   en resultados/assembly_microbench/<subgrupo>/<kernel>.json, junto a un
#   .log con la salida del binario (que incluye su tabla de tiempos).
#
# Uso:
#   ./run_assembly_microbench.sh [subgrupo ...]
#
#   subgrupos (por defecto, los 4):
#     arith_instr  operaciones aritmeticas escalares/RVV (52 kernels)
#     ldst_instr   cargas/almacenamientos escalares/RVV (62 kernels)
#     gather       cargas indexadas (vluxei) y segmentadas (vlseg) (8 kernels)
#     reduction    reducciones vectoriales (15 kernels)
#
# Ejemplos:
#   ./run_assembly_microbench.sh arith_instr
#   ITERS=100000 ./run_assembly_microbench.sh gather reduction
#   SKIP_BUILD=1 ./run_assembly_microbench.sh ldst_instr
#   ONLY=vadd ./run_assembly_microbench.sh arith_instr      # filtro por nombre
#
# Variables de entorno:
#   ITERS       iteraciones de cada kernel (defecto por subgrupo: ver ITERS_DEF)
#   VLEN        VLEN de RAVE en bits (defecto 256)  <-- ver NOTA 1
#   EXTENSIONS  extensiones extra del -cpu de QEMU (defecto zfh/zvfh, ver NOTA 4)
#   TIMEOUT     segundos maximos por ejecucion (defecto 600)
#   SKIP_BUILD  1 = no recompilar, usar los .x actuales
#   COMPILERS   compiladores a construir (defecto "clang")
#   ONLY        subcadena: solo ejecuta los kernels que la contengan
#   OUT         carpeta de resultados (defecto resultados/assembly_microbench)
#
# NOTAS
# 1) VLEN: los kernels vuelcan el registro v0 sobre `int32_t buf[32]` y el volcado
#    tiene VLMAX = VLEN/SEW elementos. Con el VLEN por defecto de RAVE (16384) o
#    con 512 los kernels de 8 bits (VLMAX = 64) desbordan la pila -> SIGSEGV (no
#    es culpa del plugin: sin plugin tambien peta). Con VLEN=256 VLMAX <= 32 para
#    todos los SEW (32/16/8/4), que es lo maximo que cabe.
# 2) Los drivers de arith_instr y ldst_instr se han parcheado para aceptar las
#    iteraciones por argv[1] (igual que gather/reduction ya hacian), porque con
#    las 1e8 iteraciones que traian de serie perfilar un kernel tarda >10 min.
# 3) Solo se compila con clang: el toolchain EPI no trae un gcc de Linux
#    (riscv64-unknown-linux-gnu-g++), que es lo que usan los config_gcc.mk.
# 4) RAVE_TRACE_EXTENDED=1: activa la clasificacion extendida, de la que salen
#    los contadores de mascara (counters.masked del JSON) y el resto de TYPE_EXT.
# 5) Los kernels de coma flotante de 16 bits (vfadd/vfmul/vfdiv/vfmacc/... _16)
#    se compilan con -march=rv64gcv_zfh_zvfh, pero el -cpu de RAVE no trae esas
#    extensiones -> SIGILL (exit 132). Se anaden con RAVE_CUSTOM_EXTENSIONS.
# ---------------------------------------------------------------------------
set -u

# Raiz del repositorio, config local y rutas por defecto (relativas al repo).
source "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/lib/common.sh"

SRC=$RVV_EVAL_HOME/assembly_microbench
OUT=${OUT:-$RESULTS_DIR/assembly_microbench}
TIMEOUT=${TIMEOUT:-600}
VLEN=${VLEN:-256}
EXTENSIONS=${EXTENSIONS:-"zfh=true,zvfh=true"}
COMPILERS=${COMPILERS:-"clang"}
ONLY=${ONLY:-}

SUBS=(arith_instr ldst_instr gather reduction)
FOUND=()
for arg in "$@"; do
	for s in "${SUBS[@]}"; do
		[ "$arg" = "$s" ] && FOUND+=("$arg")
	done
done
[ ${#FOUND[@]} -eq 0 ] && FOUND=("${SUBS[@]}")

# Iteraciones por defecto de cada subgrupo (el valor que traen de serie, salvo
# arith/ldst, que traen 1e8 y bajo RAVE son inviables: ~1000 s por kernel).
# 2e5 en arith/ldst/gather son ~10 s por kernel con contadores.
iters_def(){
	case "$1" in
		reduction) echo 10000 ;;
		*)         echo 200000 ;;
	esac
}

# Carpeta de binarios de cada subgrupo: arith/ldst separan por compilador
# (build/clang21, build/gcc15); gather/reduction compilan en un unico build/.
bdir_for(){
	case "$1:$2" in
		arith_instr:clang|ldst_instr:clang) echo "$SRC/$1/build/clang21" ;;
		arith_instr:gcc|ldst_instr:gcc)     echo "$SRC/$1/build/gcc15" ;;
		gather:*|reduction:*)               echo "$SRC/$1/build" ;;
		*)                                  echo "" ;;
	esac
}

# --- compilacion -----------------------------------------------------------
if [ "${SKIP_BUILD:-0}" != "1" ]; then
	use_toolchain
	if ! command -v clang++ >/dev/null 2>&1; then
		echo "ERROR: no encuentro clang++ (toolchain EPI en $TOOLCHAIN)" >&2
		exit 1
	fi
	echo "== Compilando con clang++ (llvm-EPI = $(clang++ --version | head -1)) =="
	for sub in "${FOUND[@]}"; do
		d=$SRC/$sub
		case "$sub" in
			arith_instr|ldst_instr)
				if ( cd "$d" && make clang >/dev/null 2>&1 ); then
					echo "   $sub OK"
				else
					echo "   $sub FALLO al compilar" >&2
				fi
				;;
			gather|reduction)
				# su Makefile trae CXX := g++: lo sobreescribimos por clang++
				if ( cd "$d" && make CXX=clang++ >/dev/null 2>&1 ); then
					echo "   $sub OK"
				else
					echo "   $sub FALLO al compilar" >&2
				fi
				;;
		esac
	done
fi

# --- comprobaciones --------------------------------------------------------
load_rave_environment
require_rave

# --- ejecucion -------------------------------------------------------------
mkdir -p "$OUT"
{ echo "fecha:    $(date)"; echo "VLEN:     $VLEN"; echo "ITERS:    ${ITERS:-por subgrupo}";
  echo "EXTRA:    $EXTENSIONS"; echo "TIMEOUT:  $TIMEOUT"; } > "$OUT/run_info.txt"
echo "== Perfilando con RAVE (VLEN=$VLEN, timeout=${TIMEOUT}s, salida=$OUT) =="
total=0
for sub in "${FOUND[@]}"; do
	d=$SRC/$sub
	iters=${ITERS:-$(iters_def "$sub")}
	mkdir -p "$OUT/$sub"
	# gather/reduction tienen un unico build/ (no separan por compilador)
	case "$sub" in
		arith_instr|ldst_instr)
			DIRS=(); for c in $COMPILERS; do DIRS+=("$(bdir_for "$sub" "$c")"); done ;;
		*)
			DIRS=("$(bdir_for "$sub" clang)") ;;
	esac
	for bdir in "${DIRS[@]}"; do
		[ -d "$bdir" ] || { echo "   $sub: no hay $bdir (¿compilado?)"; continue; }
		for exe in "$bdir"/*.x; do
			[ -e "$exe" ] || continue
			name=$(basename "$exe" .x)
			[ -n "$ONLY" ] && case "$name" in *"$ONLY"*) ;; *) continue ;; esac
			json=$OUT/$sub/$name.json
			log=$OUT/$sub/$name.log
			t0=$(date +%s)
			( cd "$d" && RAVE_VLEN=$VLEN \
				RAVE_TRACE_EXTENDED=1 \
				RAVE_CUSTOM_EXTENSIONS=$EXTENSIONS \
				timeout "$TIMEOUT" "$RAVE_CMD" --json "$json" "$exe" "$iters" >"$log" 2>&1 )
			rc=$?
			t1=$(date +%s)
			total=$((total+1))
			printf '   %-34s %-6s iters=%-9s exit=%-3s %3ss\n' \
				"$sub/$name" "$(basename "$bdir")" "$iters" "$rc" "$((t1-t0))"
		done
	done
done

echo
echo "ejecuciones: $total"
echo "JSON en:    $OUT"
