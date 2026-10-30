#!/usr/bin/env bash
# Ejecuta el ranking de instrucciones con las dependencias locales.
set -euo pipefail
cd "$(dirname "$0")"
exec "${PYTHON:-python3}" ranking_instrucciones.py "$@"
