#!/usr/bin/env bash

# Lanza la generacion de figuras para TODOS los JSON de resultados/ y, al
# final, el ranking de instrucciones. No recibe argumentos: recorre todo el
# arbol de resultados/ y replica su estructura bajo FIGURAS/:
#
#   resultados/<carpeta>/<app>.json -> FIGURAS/<carpeta>/<APP>/<region>/*.png
set -euo pipefail
cd "$(dirname "$0")"

# Dependencias Python locales (numpy, matplotlib) instaladas en python_libs/
# con las ruedas de vendor/: el Python del sistema no las trae.
export PYTHONPATH="$PWD/python_libs${PYTHONPATH:+:$PYTHONPATH}"
export MPLCONFIGDIR="${MPLCONFIGDIR:-$PWD/.matplotlib}"

RESULTADOS="../resultados"

if [ ! -d "$RESULTADOS" ]; then
	echo "Error: '$RESULTADOS' no es un directorio valido." >&2
	exit 1
fi

mapfile -t JSONS < <(find "$RESULTADOS" -name '*.json' | sort)
if [ ${#JSONS[@]} -eq 0 ]; then
	echo "Error: no hay JSON en '$RESULTADOS'." >&2
	exit 1
fi

echo "Procesando ${#JSONS[@]} JSON de $RESULTADOS ..."

for archivo in "${JSONS[@]}"; do
	# Carpeta relativa del JSON respecto a resultados/: replica la estructura
	rel_dir=$(dirname "${archivo#$RESULTADOS/}")
	dir_figuras="FIGURAS/$rel_dir"
	mkdir -p "$dir_figuras"
	echo "Procesando: $archivo"
	python3 ../rave-ext/utils/generate_figures.py -o "$dir_figuras" "$archivo"
done

# Ranking de instrucciones: lee todos los JSON de ../resultados y escribe
# sus CSV y figuras en salida_ranking/.
echo "Generando ranking de instrucciones..."
python3 ranking_instrucciones.py

echo "Procesamiento completado."
