#!/bin/bash
# ---------------------------------------------------------------------------
# run_rivec.sh - Compila los benchmarks de RiVEC en su version VECTORIAL, los
#                ejecuta bajo RAVE (RVV 1.0) y guarda un JSON por app en
#                resultados/<tamano>/<app>.json
#
# Uso:
#   ./run_rivec.sh <tamano> [app ...]
#
#   <tamano>     tiny | small | medium | large    (presets de los run.sh de RiVEC)
#                El propio tamano da nombre a la subcarpeta de resultados.
#   [app ...]    opcional: subconjunto de apps. Por defecto, las 12.
#
# Ejemplos:
#   ./run_rivec.sh tiny
#   ./run_rivec.sh small spmv matmul
#   SKIP_BUILD=1 ./run_rivec.sh medium
#   TIMEOUT=1200 ./run_rivec.sh large
#
# Variables de entorno:
#   TIMEOUT      segundos maximos por ejecucion           (defecto: 300)
#   SKIP_BUILD   1 = no recompilar, usar los .exe actuales (defecto: 0)
#
# Notas:
#   - Solo RVV 1.0 y SOLO la variante vectorial: no se compilan ni ejecutan
#     los _serial, y los JSON salen como <app>.json (sin sufijo _vector).
#   - Se compila con el toolchain EPI que trae RAVE (target Linux), el unico
#     cuyos binarios RAVE puede perfilar.
#   - Las metricas son las de la traza extendida (RAVE_TRACE_EXTENDED=1).
#     Formato de los campos: rave-ext/docs/PROFILER_JSON_API.md
# ---------------------------------------------------------------------------
set -u

SIZE=${1:-}
if [ -z "$SIZE" ]; then
	echo "Uso: $0 <tiny|small|medium|large> [app ...]" >&2
	exit 1
fi
case "$SIZE" in
	tiny|small|medium|large) ;;
	*) echo "ERROR: tamano '$SIZE' no valido (tiny|small|medium|large)" >&2; exit 1;;
esac
shift
APPS_FILTER=("$@")

# Raiz del repositorio, config local y rutas por defecto (relativas al repo).
source "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/lib/common.sh"

RIVEC=$RIVEC_HOME
OUT=$RESULTS_DIR/$SIZE          # la subcarpeta de resultados es el tamano
TIMEOUT=${TIMEOUT:-300}
RVV=${RAVE_RVV:-1_0}

APPS=(axpy blackscholes canneal jacobi-2d lavaMD matmul spmv swaptions streamcluster somier particlefilter pathfinder)

# --- argumentos de cada app segun el tamano (de los run.sh de RiVEC) -------
args_for(){
	local app=$1 size=$2 out=$3
	case "$app:$size" in
		axpy:tiny)            echo "256";;
		axpy:small)           echo "512";;
		axpy:medium)          echo "1024";;
		axpy:large)           echo "2048";;
		blackscholes:tiny)    echo "1 input/in_512.input $out";;
		blackscholes:small)   echo "1 input/in_4K.input $out";;
		blackscholes:medium)  echo "1 input/in_16K.input $out";;
		blackscholes:large)   echo "1 input/in_64K.input $out";;
		canneal:tiny)         echo "1 100 300 input/100.nets 8";;
		canneal:small)        echo "1 10000 2000 input/100000.nets 32";;
		canneal:medium)       echo "1 15000 2000 input/200000.nets 64";;
		canneal:large)        echo "1 15000 2000 input/400000.nets 128";;
		jacobi-2d:tiny)       echo "32 2 $out";;
		jacobi-2d:small)      echo "128 10 $out";;
		jacobi-2d:medium)     echo "256 100 $out";;
		jacobi-2d:large)      echo "256 2000 $out";;
		lavaMD:tiny)          echo "-cores 1 -boxes1d 1 -outputFile $out";;
		lavaMD:small)         echo "-cores 1 -boxes1d 4 -outputFile $out";;
		lavaMD:medium)        echo "-cores 1 -boxes1d 6 -outputFile $out";;
		lavaMD:large)         echo "-cores 1 -boxes1d 10 -outputFile $out";;
		matmul:tiny)          echo "input/data_64.in";;
		matmul:small)         echo "input/data_128.in";;
		matmul:medium)        echo "input/data_256.in";;
		matmul:large)         echo "input/data_512.in";;
		spmv:tiny)            echo "input/football.mtx input/football.verif";;
		spmv:small)           echo "input/lhr07.mtx input/lhr07.verif";;
		spmv:medium)          echo "input/venkat25.mtx input/venkat25.verif";;
		spmv:large)           echo "input/poisson3Db.mtx input/poisson3Db.verif";;
		swaptions:tiny)       echo "-ns 8 -sm 512 -nt 1";;
		swaptions:small)      echo "-ns 8 -sm 4096 -nt 1";;
		swaptions:medium)     echo "-ns 32 -sm 8192 -nt 1";;
		swaptions:large)      echo "-ns 64 -sm 16384 -nt 1";;
		streamcluster:tiny)   echo "3 10 128 128 128 10 none $out 1";;
		streamcluster:small)  echo "10 20 128 4096 4096 1000 none $out 1";;
		streamcluster:medium) echo "10 20 128 8192 8192 1000 none $out 1";;
		streamcluster:large)  echo "10 20 128 8192 8192 1000 none $out 1";;
		somier:tiny)          echo "2 64";;
		somier:small)         echo "4 64";;
		somier:medium)        echo "2 128";;
		somier:large)         echo "4 128";;
		particlefilter:tiny)   echo "-x 128 -y 128 -z 2 -np 256";;
		particlefilter:small)  echo "-x 128 -y 128 -z 8 -np 1024";;
		particlefilter:medium) echo "-x 128 -y 128 -z 16 -np 4096";;
		particlefilter:large)  echo "-x 128 -y 128 -z 24 -np 8192";;
		pathfinder:tiny)      echo "input/data_tiny.in";;
		pathfinder:small)     echo "input/data_small.in";;
		pathfinder:medium)    echo "input/data_medium.in";;
		pathfinder:large)     echo "input/data_large.in";;
		*) return 1;;
	esac
	return 0
}

selected(){
	local app=$1
	[ ${#APPS_FILTER[@]} -eq 0 ] && return 0
	case " ${APPS_FILTER[*]} " in *" $app "*) return 0;; *) return 1;; esac
}

# --- compilacion (solo variante vectorial) ---------------------------------
if [ "${SKIP_BUILD:-0}" != "1" ]; then
	echo "== Compilando variante vectorial (RISCV=$TOOLCHAIN) =="
	for app in "${APPS[@]}"; do
		selected "$app" || continue
		d=$RIVEC/_$app
		mkdir -p "$d/bin"   # no se usa 'make start' (hace 'rm bin/*.*' sin -f)
		if ( cd "$d" && make RISCV="$TOOLCHAIN" vector >/dev/null 2>&1 ); then
			echo "   $app OK"
		else
			echo "   $app FALLO al compilar la variante vectorial"
		fi
	done
fi

# --- entorno RAVE ----------------------------------------------------------
load_rave_environment
require_rave

# --- ejecucion -------------------------------------------------------------
mkdir -p "$OUT"

run_one(){
	local app=$1
	local d=$RIVEC/_$app
	local bin="${app}_vector.exe"
	local json="$OUT/$app.json"
	local aargs
	aargs=$(args_for "$app" "$SIZE" "${TMPDIR:-/tmp}/rivec_${app}_${SIZE}.out") || {
		echo "   (sin argumentos definidos para $app/$SIZE)"; return; }
	if [ ! -x "$d/bin/$bin" ]; then
		echo "   FALTA el binario $bin"
		return
	fi
	local t0 t1 rc sz
	t0=$(date +%s)
	if [ "$app" = "lavaMD" ]; then
		( cd "$d" && RAVE_TRACE_EXTENDED=1 RAVE_ACCUM_REGIONS=1 \
			timeout "$TIMEOUT" "$RAVE_CMD" --json "$json" "bin/$bin" $aargs >/dev/null 2>&1 )
	else
		( cd "$d" && RAVE_TRACE_EXTENDED=1 timeout "$TIMEOUT" \
			"$RAVE_CMD" --json "$json" "bin/$bin" $aargs >/dev/null 2>&1 )
	fi
	rc=$?
	normalize_json_binary "$json" "$d/bin/$bin"
	t1=$(date +%s)
	sz=$(stat -c %s "$json" 2>/dev/null || echo 0)
	printf '   %-18s exit=%-3s %3ss  %s\n' "$app" "$rc" "$((t1-t0))" "$(basename "$json")"
}

echo "== Ejecutando bajo RAVE (tamano=$SIZE, salida=$OUT) =="
for app in "${APPS[@]}"; do
	selected "$app" || continue
	run_one "$app"
done

echo
echo "JSON en:  $OUT"
