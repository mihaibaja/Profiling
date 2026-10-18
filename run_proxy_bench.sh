#!/bin/bash
# ---------------------------------------------------------------------------
# run_proxy_bench.sh - Compila (si hace falta) y perfila con RAVE los proxy
#   benchmarks de rvv-evaluation (darknet, gemm, spmv-v2), guardando un JSON por
#   binario en resultados/proxy_bench/<bench>/<variante>.json + .log.
#
# Uso:
#   ./run_proxy_bench.sh [bench ...]
#
#   benches (por defecto, los 3): darknet | gemm | spmv-v2
#
# Ejemplos:
#   ./run_proxy_bench.sh gemm
#   SKIP_BUILD=1 ./run_proxy_bench.sh spmv-v2
#   GEMM_ARGS="1 1 100 1" ./run_proxy_bench.sh gemm
#
# Variables de entorno:
#   VARIANTS    variantes a construir/ejecutar (defecto: las 6)
#               nonvec autovec autovec_1 autovec_2 autovec_4 autovec_8
#   PRECISIONS  solo gemm: "float" (defecto) o "float double"
#   THREADS     hilos de OpenMP con los que se ejecuta (defecto 1)
#   GEMM_ARGS   argumentos de gemm  (defecto "1 2 100 1"  = threads iters size rep)
#               (un tamano 2000 como el de su run.sh tarda >30 min con contadores)
#   SPMV_ARGS   argumentos de spmv  (defecto "1 2 6 3 1" = threads iters 2log radius rep)
#               (su run.sh usa "8 10 8 10 1", que con contadores son ~3 min por variante)
#   DARKNET_RUN 1 = ejecutar darknet (por defecto solo se compila)
#   DARKNET_ARGS  argumentos de darknet (p. ej. "classifier predict cfg/cifar.test.cfg <pesos> <imagen>")
#   TIMEOUT     segundos maximos por ejecucion (defecto 900)
#   SKIP_BUILD  1 = no recompilar
#
# NOTAS
# 1) Solo clang: el toolchain EPI no trae gcc de Linux (riscv64-unknown-linux-gnu-*),
#    que es el que usan los config_gcc.mk / GCC_CC de sus scripts.
# 2) darknet: las variantes RVV NO enlazan con este toolchain. El clang de EPI
#    vectoriza las llamadas a libm (exp, pow...) a funciones __epi_*(nxv4f64) que
#    vienen en una libreria de matematicas vectoriales que aqui no esta. Solo
#    compila la variante escalar (nonvec). El enlace falla con:
#       undefined reference to `__epi_exp_nxv4f64'
#    Ademas darknet necesita ficheros de pesos que no estan en el repo, asi que
#    por defecto solo se compila (DARKNET_RUN=1 + DARKNET_ARGS para ejecutarlo).
# 3) Se ejecuta con 1 hilo de OpenMP: el modelo de regiones/hilos de RAVE esta
#    pensado para un hilo y asi los contadores son deterministas.
# ---------------------------------------------------------------------------
set -u

# Raiz del repositorio, config local y rutas por defecto (relativas al repo).
source "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/lib/common.sh"

SRC=$RVV_EVAL_HOME/proxy_bench
OUT=${OUT:-$RESULTS_DIR/proxy_bench}
TIMEOUT=${TIMEOUT:-900}
THREADS=${THREADS:-1}
VARIANTS=${VARIANTS:-"nonvec autovec autovec_1 autovec_2 autovec_4 autovec_8"}
PRECISIONS=${PRECISIONS:-"float"}
GEMM_ARGS=${GEMM_ARGS:-"$THREADS 2 100 1"}
SPMV_ARGS=${SPMV_ARGS:-"$THREADS 2 6 3 1"}
DARKNET_RUN=${DARKNET_RUN:-0}
DARKNET_ARGS=${DARKNET_ARGS:-}

# opciones que pide el README de spmv-v2 para los binarios de clang con OpenMP
# de LLVM en un entorno estatico (si no, el runtime espera hilos ocultos)
OMP_ENV="OMP_NUM_THREADS=$THREADS OMP_TOOL=disabled LIBOMP_USE_HIDDEN_HELPER_TASK=FALSE LIBOMP_NUM_HIDDEN_HELPER_THREADS=0"

BENCHS=(darknet gemm spmv-v2)
FOUND=()
for arg in "$@"; do
	for b in "${BENCHS[@]}"; do
		[ "$arg" = "$b" ] && FOUND+=("$arg")
	done
done
[ ${#FOUND[@]} -eq 0 ] && FOUND=("${BENCHS[@]}")

clang_cc="clang -std=c11 -pthread -static"
clang_cxx="clang++ -std=gnu++20 -pthread -fmax-errors=1 -static"

# --- compilacion -----------------------------------------------------------
if [ "${SKIP_BUILD:-0}" != "1" ]; then
	use_toolchain
	if ! command -v clang++ >/dev/null 2>&1; then
		echo "ERROR: no encuentro clang++ (toolchain EPI en $TOOLCHAIN)" >&2
		exit 1
	fi
	echo "== Compilando variantes con clang++ =="
	for bench in "${FOUND[@]}"; do
		d=$SRC/$bench
		for v in $VARIANTS; do
			case "$v" in
				nonvec)     nv=1; lmul="" ;;
				autovec)    nv=0; lmul="" ;;
				autovec_*)  nv=0; lmul=${v#autovec_} ;;
				*)          echo "   (variante desconocida: $v)"; continue ;;
			esac
			case "$bench" in
				gemm)
					for prec in $PRECISIONS; do
						case "$prec" in float) fflag="float=1" ;; *) fflag="float=0" ;; esac
						out=$d/build/clang/$prec/gemm_$v
						mkdir -p "$d/build/clang/$prec"
						if ( cd "$d" && make clean >/dev/null 2>&1 &&
						     make gemm CC="$clang_cc" CXX="$clang_cxx" clang=1 \
						          nonvec=$nv ${lmul:+RVV_LMUL=$lmul} $fflag >/dev/null 2>&1 &&
						     mv gemm "$out" ); then
							echo "   gemm/$prec/$v OK"
						else
							echo "   gemm/$prec/$v FALLO al compilar"
						fi
						( cd "$d" && make clean >/dev/null 2>&1 )
					done
					;;
				spmv-v2)
					out=$d/build/clang/sparse_$v
					if ( cd "$d" && make clean >/dev/null 2>&1 &&
					     make sparse CC="$clang_cc" CXX="$clang_cxx" clang=1 \
					          nonvec=$nv ${lmul:+RVV_LMUL=$lmul} >/dev/null 2>&1 &&
					     mkdir -p "$d/build/clang" && mv sparse "$out" ); then
						echo "   spmv-v2/$v OK"
					else
						echo "   spmv-v2/$v FALLO al compilar"
					fi
					( cd "$d" && make clean >/dev/null 2>&1 )
					;;
				darknet)
					if [ "$nv" = "0" ]; then
						# fallo conocido: falta la libm vectorial del toolchain EPI
						[ "$v" = "autovec" ] && echo "   darknet/$v: las variantes RVV no enlazan (__epi_* ausente), se omiten"
						continue
					fi
					out=$d/build/clang/darknet_$v
					if ( cd "$d" && make clean >/dev/null 2>&1 &&
					     make CONFIG=config_clang.mk OPENMP=1 nonvec=$nv >/dev/null 2>&1 &&
					     mkdir -p "$d/build/clang" && mv darknet "$out" ); then
						echo "   darknet/$v OK"
					else
						echo "   darknet/$v FALLO al compilar"
					fi
					( cd "$d" && make clean >/dev/null 2>&1 )
					;;
			esac
		done
	done
fi

# --- comprobaciones --------------------------------------------------------
load_rave_environment
require_rave

# --- ejecucion -------------------------------------------------------------
echo "== Perfilando con RAVE (hilos=$THREADS, timeout=${TIMEOUT}s, salida=$OUT) =="
total=0
for bench in "${FOUND[@]}"; do
	d=$SRC/$bench
	mkdir -p "$OUT/$bench"
	case "$bench" in
		gemm)
			for prec in $PRECISIONS; do
				for v in $VARIANTS; do
					exe=$d/build/clang/$prec/gemm_$v
					[ -x "$exe" ] || continue
					json=$OUT/$bench/${prec}_gemm_$v.json
					log=$OUT/$bench/${prec}_gemm_$v.log
					t0=$(date +%s)
					( cd "$d" && env $OMP_ENV timeout "$TIMEOUT" \
						"$RAVE_CMD" --json "$json" "$exe" $GEMM_ARGS >"$log" 2>&1 )
					rc=$?; t1=$(date +%s); total=$((total+1))
					printf '   %-26s exit=%-3s %4ss\n' "gemm/$prec/$v" "$rc" "$((t1-t0))"
				done
			done
			;;
		spmv-v2)
			for v in $VARIANTS; do
				exe=$d/build/clang/sparse_$v
				[ -x "$exe" ] || continue
				json=$OUT/$bench/sparse_$v.json
				log=$OUT/$bench/sparse_$v.log
				t0=$(date +%s)
				( cd "$d" && env $OMP_ENV timeout "$TIMEOUT" \
					"$RAVE_CMD" --json "$json" "$exe" $SPMV_ARGS >"$log" 2>&1 )
				rc=$?; t1=$(date +%s); total=$((total+1))
				printf '   %-26s exit=%-3s %4ss\n' "spmv-v2/$v" "$rc" "$((t1-t0))"
			done
			;;
		darknet)
			if [ "$DARKNET_RUN" != "1" ]; then
				echo "   darknet: solo compilado (pon DARKNET_RUN=1 y DARKNET_ARGS=\"...\" para ejecutarlo)"
				continue
			fi
			if [ -z "$DARKNET_ARGS" ]; then
				echo "   darknet: DARKNET_ARGS esta vacio, no se ejecuta nada"
				continue
			fi
			for exe in "$d"/build/clang/darknet_*; do
				[ -x "$exe" ] || continue
				name=$(basename "$exe")
				json=$OUT/$bench/$name.json
				log=$OUT/$bench/$name.log
				t0=$(date +%s)
				( cd "$d" && env $OMP_ENV timeout "$TIMEOUT" \
					"$RAVE_CMD" --json "$json" "$exe" $DARKNET_ARGS >"$log" 2>&1 )
				rc=$?; t1=$(date +%s); total=$((total+1))
				printf '   %-26s exit=%-3s %4ss\n' "darknet/$name" "$rc" "$((t1-t0))"
			done
			;;
	esac
done

echo
echo "ejecuciones: $total"
echo "JSON en:    $OUT"
