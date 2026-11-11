#!/usr/bin/env bash

# Validar que se haya pasado un directorio como parámetro
if [ -z "$1" ]; then
    echo "Uso: $0 <carpeta>"
    exit 1
fi

CARPETA="$1"

# Comprobar que el directorio exista
if [ ! -d "$CARPETA" ]; then
    echo "Error: '$CARPETA' no es un directorio válido."
    exit 1
fi

# Obtener el nombre del directorio (última parte del path)
NOMBRE_CARPETA=$(basename "$CARPETA")
DIR_FIGURAS="FIGURAS/$NOMBRE_CARPETA"

# Crear la carpeta de salida si no existe
mkdir -p "$DIR_FIGURAS"

# Recorrer todos los elementos del directorio
for archivo in "$CARPETA"/*; do
    # Asegurarse de que sea un archivo regular (omite carpetas como FIGURAS)
    if [ -f "$archivo" ]; then
        echo "Procesando: $archivo"
        python3 ../rave-ext/utils/generate_figures.py -o "$DIR_FIGURAS" "$archivo"
    fi
done

# Ranking de instrucciones: lee todos los JSON de ../resultados y escribe
# sus CSV y figuras en salida_ranking/.
echo "Generando ranking de instrucciones..."
python3 ranking_instrucciones.py

echo "Procesamiento completado."
