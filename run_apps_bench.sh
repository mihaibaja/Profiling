#!/bin/bash
# ---------------------------------------------------------------------------
# run_apps_bench.sh - Compila (si hace falta) y perfila con RAVE las
#   aplicaciones de rvv-evaluation (hoy solo qsim_rvv, que es un submódulo).
#   Guarda un JSON por app en resultados/apps_bench/qsim_rvv/<app>.json + .log
#
# Uso:
#   ./run_apps_bench.sh [app ...]
#
#   apps (por defecto: qsim_base_rvv):
#     qsim_base_rvv   simulador con el backend RVV escrito a mano (el del paper)
#     qsim_base       misma app autovectorizada por el compilador
#
# Ejemplos:
#   ./run_apps_bench.sh
#   QUBITS=14 ./run_apps_bench.sh qsim_base_rvv
#   CIRCUIT=circuits/circuit_q24 ./run_apps_bench.sh       # circuito del repo
#   SKIP_BUILD=1 ./run_apps_bench.sh
#
# Variables de entorno:
#   QUBITS      qubits del circuito GHZ que se genera si falta (defecto 20)
#   CIRCUIT     circuito a usar (por defecto circuits/ghz_q<QUBITS>)
#   QSIM_ARGS   argumentos de la app (defecto "-t 1 -f 3 -v 3")
#   TIMEOUT     segundos maximos por ejecucion (defecto 900)
#   SKIP_BUILD  1 = no recompilar
#
# NOTAS
# 1) El submódulo apps_bench/qsim_rvv hay que tenerlo clonado:
#       git -C rvv-evaluation submodule update --init --recursive
#    (la URL HTTPS está en rvv-evaluation/.gitmodules)
# 2) La raiz del repo trae CXX=riscv64-unknown-linux-gnu-g++ (gcc de Linux, que el
#    toolchain EPI no incluye), asi que se sobreescribe con clang++.
# 3) Se compilan apps sueltas, NO el target agregado `make qsim`: ese incluye
#    qsim_von_neumann / qsim_amplitudes, que no enlazan con este toolchain porque
#    les falta la libreria de matematicas vectoriales del EPI (__epi_*).
# 4) Tamano: con contadores, cada qubit dobla el trabajo. Medido con RAVE:
#    q14 ~1 s, q20 ~19 s, q24 (el circuito del repo) > 5 min. Por eso 20.
# 5) -t 1: un solo hilo (los contadores por hilo de RAVE son mas limpios asi).
# ---------------------------------------------------------------------------
set -u

# Raiz del repositorio, config local y rutas por defecto (relativas al repo).
source "$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)/lib/common.sh"

SRC=$RVV_EVAL_HOME/apps_bench/qsim_rvv
OUT=${OUT:-$RESULTS_DIR/apps_bench/qsim_rvv}
TIMEOUT=${TIMEOUT:-900}
QUBITS=${QUBITS:-20}
QSIM_ARGS=${QSIM_ARGS:-"-t 1 -f 3 -v 3"}
APPS_DEF=("qsim_base_rvv")

FOUND=()
if [ "$#" -eq 0 ]; then
	FOUND=("${APPS_DEF[@]}")
else
	FOUND=("$@")
fi

# --- comprobaciones --------------------------------------------------------
if [ ! -d "$SRC/apps" ]; then
	echo "ERROR: el submodulo qsim_rvv no esta clonado ($SRC/apps no existe)." >&2
	echo "       git -C $RVV_EVAL_HOME submodule update --init --recursive" >&2
	exit 1
fi

# circuito: se genera un GHZ del tamano pedido si no existe
CIRCUIT=${CIRCUIT:-circuits/ghz_q$QUBITS}
if [ ! -f "$SRC/$CIRCUIT" ]; then
	case "$CIRCUIT" in
		circuits/*)
			echo "   generando $CIRCUIT (GHZ de $QUBITS qubits)"
			{ echo "$QUBITS"; echo "0 h 0"; i=1
			  for q in $(seq 1 $((QUBITS-1))); do echo "$i cnot 0 $q"; i=$((i+1)); done
			} > "$SRC/$CIRCUIT"
			;;
		*)
			echo "ERROR: no encuentro el circuito $SRC/$CIRCUIT" >&2
			exit 1
			;;
	esac
fi

# --- compilacion -----------------------------------------------------------
if [ "${SKIP_BUILD:-0}" != "1" ]; then
	use_toolchain
	if ! command -v clang++ >/dev/null 2>&1; then
		echo "ERROR: no encuentro clang++ (toolchain EPI en $TOOLCHAIN)" >&2
		exit 1
	fi
	echo "== Compilando apps con clang++ =="
	for app in "${FOUND[@]}"; do
		if ( cd "$SRC" && make -C apps/ "$app.x" \
			CXX=clang++ CXXFLAGS="-O3 -std=c++17" ARCHFLAGS="-march=rv64gcv" \
			>/dev/null 2>&1 ); then
			echo "   $app OK"
		else
			echo "   $app FALLO al compilar (¿necesita la libm vectorial del EPI?)"
		fi
	done
fi

if ! command -v "$RAVE_CMD" >/dev/null 2>&1; then
	load_rave_environment
fi
require_rave

# --- ejecucion -------------------------------------------------------------
echo "== Perfilando con RAVE (circuito=$CIRCUIT, timeout=${TIMEOUT}s, salida=$OUT) =="
mkdir -p "$OUT"
total=0
for app in "${FOUND[@]}"; do
	exe=$SRC/apps/$app.x
	[ -x "$exe" ] || { echo "   $app: falta el binario $exe"; continue; }
	json=$OUT/$app.json
	log=$OUT/$app.log
	t0=$(date +%s)
	( cd "$SRC" && timeout "$TIMEOUT" "$RAVE_CMD" --json "$json" "apps/$app.x" \
		-c "$CIRCUIT" $QSIM_ARGS >"$log" 2>&1 )
	rc=$?
	t1=$(date +%s)
	total=$((total+1))
	printf '   %-18s exit=%-3s %4ss\n' "$app" "$rc" "$((t1-t0))"
done

echo
echo "ejecuciones: $total"
echo "JSON en:    $OUT"
