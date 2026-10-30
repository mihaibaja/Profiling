#!/usr/bin/env bash
# Ejecuta el analisis con las dependencias locales de analisis/python_libs.
set -euo pipefail
cd "$(dirname "$0")"
exec "${PYTHON:-python3}" comparar_resultados.py "$@"
