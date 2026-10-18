#!/bin/bash
# ============================================================================
# config.example.sh - Configuracion local del repositorio Profiling
#
# Copia este archivo a config.sh y edita solo lo que necesites:
#
#     cp config.example.sh config.sh
#
# `config.sh` NO se versiona (esta en .gitignore). Todos los valores por
# defecto son RELATIVOS a la raiz del repositorio, por lo que en la mayoria
# de equipos no hace falta cambiar nada.
#
# Tambien puedes exportar cualquiera de estas variables en tu shell antes de
# lanzar un script. Prioridad: config.sh > variable de entorno > valor por
# defecto relativo a la raiz del repositorio.
# ============================================================================

# Raiz del repositorio. Normalmente se detecta sola a partir de la ubicacion
# de los scripts; solo hace falta fijarla si mueves los scripts de sitio.
# PROFILING_ROOT="$HOME/Documents/TFG/Profiling"

# ---------------------------------------------------------------------------
# Submodulos (por defecto, carpetas dentro de la raiz del repositorio)
# ---------------------------------------------------------------------------
# RAVE_HOME="$PROFILING_ROOT/rave-ext"
# RIVEC_HOME="$PROFILING_ROOT/RiVEC"
# RVV_EVAL_HOME="$PROFILING_ROOT/rvv-evaluation"

# ---------------------------------------------------------------------------
# Toolchain y ejecutable de RAVE
# ---------------------------------------------------------------------------
# Toolchain LLVM cross construido por rave-ext. Se anade a PATH al compilar.
# TOOLCHAIN="$RAVE_HOME/build/llvm-cross/llvm-EPI-development-toolchain-cross"

# Binario `rave` que se debe ejecutar. Si se deja vacio se busca `rave` en
# PATH (por ejemplo, tras `source rave-ext/environment.sh 1_0`).
# RAVE_BIN="$RAVE_HOME/build/qemu-rave/RVV-1_0/bin/rave"

# Version de RVV usada por environment.sh de rave-ext: 1_0 o 0_7_1.
# RAVE_RVV="1_0"

# Poner a 0 para NO cargar rave-ext/environment.sh automaticamente.
# LOAD_RAVE_ENV=1

# ---------------------------------------------------------------------------
# Resultados y temporales
# ---------------------------------------------------------------------------
# Carpeta raiz de resultados (los scripts crean subcarpetas dentro).
# RESULTS_DIR="$PROFILING_ROOT/resultados"

# Los scripts de RiVEC escriben ficheros de salida temporales en TMPDIR.
# TMPDIR="${TMPDIR:-/tmp}"
