#!/bin/bash
# ============================================================================
# lib/common.sh - Utilidades comunes de los scripts de profiling
#
# No se ejecuta directamente: se carga desde los scripts de la raiz con
#
#     source "$(dirname "$0")/lib/common.sh"
#
# Resuelve la raiz del repositorio a partir de la ubicacion de este archivo,
# carga `config.sh` (si existe) y define los valores por defecto de todas las
# rutas. Todos los valores por defecto son relativos a la raiz del repo.
# ============================================================================

_COMMON_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROFILING_ROOT="$(cd -- "$_COMMON_DIR/.." && pwd)"
export PROFILING_ROOT

# Configuracion local opcional (no versionada).
if [ -f "$PROFILING_ROOT/config.sh" ]; then
	# shellcheck source=/dev/null
	. "$PROFILING_ROOT/config.sh"
fi

# ---------------------------------------------------------------------------
# Rutas por defecto (relativas a la raiz del repositorio)
# ---------------------------------------------------------------------------
: "${RAVE_HOME:=$PROFILING_ROOT/rave-ext}"
: "${RIVEC_HOME:=$PROFILING_ROOT/RiVEC}"
: "${RVV_EVAL_HOME:=$PROFILING_ROOT/rvv-evaluation}"
: "${RESULTS_DIR:=$PROFILING_ROOT/resultados}"
: "${TOOLCHAIN:=$RAVE_HOME/build/llvm-cross/llvm-EPI-development-toolchain-cross}"
: "${RAVE_RVV:=1_0}"
: "${RAVE_BIN:=}"

export RAVE_HOME RIVEC_HOME RVV_EVAL_HOME RESULTS_DIR TOOLCHAIN RAVE_RVV

# Ejecutable de RAVE: RAVE_BIN si esta definido; si no, el que haya en PATH.
RAVE_CMD="${RAVE_BIN:-rave}"

# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
die() {
	printf 'ERROR: %s\n' "$*" >&2
	exit 1
}

have() {
	command -v "$1" >/dev/null 2>&1
}

# Anade el toolchain cross al PATH y comprueba que existe.
use_toolchain() {
	[ -d "$TOOLCHAIN/bin" ] || die "no encuentro el toolchain en $TOOLCHAIN
       Compila rave-ext o ajusta TOOLCHAIN en config.sh."
	export PATH="$TOOLCHAIN/bin:$PATH"
}

# Carga el entorno de rave-ext (PATH de qemu/llvm e interfaces de Python).
# Es opcional: se puede desactivar con LOAD_RAVE_ENV=0.
load_rave_environment() {
	[ "${LOAD_RAVE_ENV:-1}" = "1" ] || return 0
	[ -f "$RAVE_HOME/environment.sh" ] || return 0
	# shellcheck source=/dev/null
	. "$RAVE_HOME/environment.sh" "$RAVE_RVV" >/dev/null 2>&1 || true
}

# Comprueba que el ejecutable de RAVE esta disponible.
require_rave() {
	have "$RAVE_CMD" || die "'$RAVE_CMD' no esta en PATH.
       Ejecuta 'source $RAVE_HOME/environment.sh $RAVE_RVV' o define
       RAVE_BIN en config.sh."
}

# Reescribe el campo "binary" del JSON de RAVE para que sea siempre relativo a
# la raiz del repositorio. RAVE guarda la ruta tal cual se le pasa, por lo que
# sin esto un rerun volveria a introducir rutas absolutas.
#
# Uso: normalize_json_binary <json> <ruta_del_binario>
normalize_json_binary() {
	local json=$1 binary=$2 rel
	[ -f "$json" ] || return 0
	rel=$(realpath --relative-to="$PROFILING_ROOT" "$binary" 2>/dev/null) || rel=$binary
	sed -i "s|\"binary\": \"[^\"]*\"|\"binary\": \"$rel\"|" "$json"
}

# Muestra una cabecera comun.
print_banner() {
	printf '== %s ==\n' "$*"
}
