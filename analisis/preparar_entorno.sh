#!/usr/bin/env bash
# Prepara las dependencias locales de analisis/ sin tocar el Python del sistema.
set -euo pipefail
cd "$(dirname "$0")"

PY="${PYTHON:-python3}"

if [ ! -d vendor ] || [ -z "$(find vendor -maxdepth 1 -name '*.whl' -print -quit 2>/dev/null)" ]; then
    echo "[1/2] Descargando ruedas en vendor/ ..."
    "$PY" -m pip download --no-cache-dir --only-binary=:all: --dest vendor -r requirements.txt
else
    echo "[1/2] vendor/ ya contiene ruedas."
fi

if [ ! -d python_libs/matplotlib ] || [ ! -d python_libs/numpy ]; then
    echo "[2/2] Instalando Matplotlib y NumPy en python_libs/ ..."
    "$PY" -m pip install --no-cache-dir --no-index --find-links vendor --target python_libs -r requirements.txt
else
    echo "[2/2] python_libs/ ya contiene Matplotlib y NumPy."
fi

"$PY" -c 'import sys; sys.path.insert(0, "python_libs"); import matplotlib, numpy; print("matplotlib", matplotlib.__version__, "| numpy", numpy.__version__)'
