#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Compara los resultados JSON de RAVE y genera diagramas de cajas.

El script:
  * recorre resultados/<tamano>/<benchmark>.json;
  * calcula totales y metricas derivadas por region;
  * agrupa los valores por tamano y por benchmark;
  * calcula media, desviacion, minimo, Q1, mediana, Q3, maximo, IQR y P10/P90;
  * escribe CSV de totales y de estadisticas;
  * genera un diagrama de cajas por metrica con Matplotlib.

Matplotlib se instala localmente en analisis/python_libs (ver
preparar_entorno.sh), sin modificar el Python del sistema.

Ejemplos:
  ./ejecutar.sh
  ./ejecutar.sh --resultados ../resultados
  ./ejecutar.sh --ejes conjunto,familia --min-muestras 2
  ./ejecutar.sh --ejes tamano
  ./ejecutar.sh --conjunto rivec --tamano medium
  ./ejecutar.sh --metricas oi_isa,ocupacion_media,masked_fraccion
  ./ejecutar.sh --listar-metricas
"""

from __future__ import annotations

import argparse
import csv
import fnmatch
import json
import math
import os
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Callable, Iterable

BASE = Path(__file__).resolve().parent
LIBS = BASE / "python_libs"
if LIBS.is_dir():
    sys.path.insert(0, str(LIBS))

# Matplotlib no debe escribir en el HOME del usuario.
os.environ.setdefault("MPLCONFIGDIR", str(BASE / ".matplotlib"))
os.environ.setdefault("MPLBACKEND", "Agg")

try:
    import numpy as np
except Exception as exc:  # pragma: no cover - solo para mensaje de ayuda
    np = None
    _NUMPY_ERROR = exc

TAMANOS = ("tiny", "small", "medium", "large")

METADATOS = (
    "archivo",
    "carpeta",
    "conjunto",
    "tamano",
    "familia",
    "benchmark",
    "run",
    "region",
    "region_idx",
    "esquema",
    "trace_extended",
    "vlen_bits",
    "generador",
    "binario",
)

EVENTOS_SV = (
    "broadcast_vx",
    "broadcast_vf",
    "scalar_to_vector",
    "vector_to_scalar",
    "scalar_result",
    "vsetvl_config",
)

CATEGORIAS_MOV = (
    "slides",
    "gathers",
    "compress",
    "reductions",
    "whole_register",
    "mask_ops_scans",
    "layout_conversions",
)

# Orden de columnas en los CSV. Las claves que no esten aqui se anaden
# alfabeticamente al final.
ORDEN_METRICAS = (
    # Totales basicos
    "instr_total",
    "instr_escalar",
    "instr_vector",
    "instr_vsetvl",
    "elems_total",
    "bytes_total",
    "bytes_escalar",
    "bytes_vector",
    "flops_total",
    "flops_escalar",
    "flops_vector",
    "elems_arith",
    "elems_reduction",
    "elems_mask",
    # Derivadas globales
    "oi_isa",
    "oi_isa_vector",
    "flops_por_elemento",
    "bytes_por_elemento",
    "ocupacion_media",
    "vl_medio",
    "vlmax_medio",
    "lmul_medio",
    "registros_vectoriales_unicos",
    "vsetvl_por_1k_vec",
    # Dependencias
    "dep_scalar_total",
    "dep_vector_total",
    "dep_raw_total",
    "dep_waw_total",
    "dep_war_total",
    "dep_raw_dist_media",
    "dep_waw_dist_media",
    "dep_war_dist_media",
    "raw_fraccion_le4",
    "war_fraccion_le8",
    "waw_fraccion_le8",
    # Mascaras
    "masked_instr",
    "masked_arith_instr",
    "masked_memory_instr",
    "masked_fraccion",
    "masked_densidad_media",
    "masked_elementos_activos",
    # Interfaz escalar-vector
    "sv_eventos_total",
    "sv_eventos_por_1k_vec",
    "sv_broadcast_vx",
    "sv_broadcast_vf",
    "sv_escalar_a_vector",
    "sv_vector_a_escalar",
    "sv_resultado_escalar",
    "sv_vsetvl",
    "sv_elementos_broadcast_vx",
    "sv_elementos_broadcast_vf",
    "sv_elementos_activos_totales",
    # Movimiento en el VRF
    "mov_instr_total",
    "mov_fraccion",
    "mov_bytes_vrf_total",
    "mov_bytes_vrf_por_op_aritmetica",
    "mov_slides_instr",
    "mov_gathers_instr",
    "mov_compress_instr",
    "mov_reducciones_instr",
    "mov_whole_register_instr",
    "mov_mask_ops_scans_instr",
    "mov_layout_conversions_instr",
    "mov_slides_bytes_vrf",
    "mov_gathers_bytes_vrf",
    "mov_compress_bytes_vrf",
    "mov_reducciones_bytes_vrf",
    "mov_whole_register_bytes_vrf",
    "mov_mask_ops_scans_bytes_vrf",
    "mov_layout_conversions_bytes_vrf",
    # Politicas
    "politica_tu",
    "politica_ta",
    "politica_mu",
    "politica_ma",
    "tu_fraccion",
    "mu_fraccion",
    "tail_preservados",
    "mask_preservados",
    "elementos_activos_escritos",
    "elementos_destino_totales",
    "presion_preservacion",
    "presion_tail",
    "presion_mask",
    # Memoria
    "mem_unit_elems",
    "mem_strided_elems",
    "mem_indexed_elems",
    "mem_total_elems",
    "mem_unit_fraccion",
    "mem_strided_fraccion",
    "mem_indexed_fraccion",
    "mem_irregular_fraccion",
    # Categorias de instrucciones
    "config_instr",
    "loadstore_instr",
    "arith_int_instr",
    "arith_fp_instr",
    "reduction_instr",
    "permutation_instr",
    "mask_instr",
    "permutaciones_por_1k_vec",
    "config_por_1k_vec",
    "loadstore_por_1k_vec",
    # Comprobacion del arbol
    "instr_tree_total",
    "instr_tree_esperado",
    "instr_tree_delta",
    "instr_tree_ok",
)

# Metricas que se grafican por defecto. Si alguna no existe en los datos, se
# omite con un aviso.
METRICAS_POR_DEFECTO = (
    "instr_vector",
    "elems_total",
    "bytes_total",
    "flops_total",
    "oi_isa",
    "oi_isa_vector",
    "flops_por_elemento",
    "bytes_por_elemento",
    "ocupacion_media",
    "vl_medio",
    "lmul_medio",
    "registros_vectoriales_unicos",
    "dep_raw_dist_media",
    "dep_waw_dist_media",
    "dep_war_dist_media",
    "raw_fraccion_le4",
    "war_fraccion_le8",
    "waw_fraccion_le8",
    "masked_fraccion",
    "masked_densidad_media",
    "masked_elementos_activos",
    "sv_eventos_por_1k_vec",
    "sv_broadcast_vx",
    "sv_broadcast_vf",
    "sv_escalar_a_vector",
    "sv_vector_a_escalar",
    "mov_fraccion",
    "mov_bytes_vrf_total",
    "mov_bytes_vrf_por_op_aritmetica",
    "mov_slides_instr",
    "mov_gathers_instr",
    "mov_compress_instr",
    "mov_reducciones_instr",
    "tu_fraccion",
    "mu_fraccion",
    "presion_preservacion",
    "mem_unit_fraccion",
    "mem_strided_fraccion",
    "mem_indexed_fraccion",
    "mem_irregular_fraccion",
    "permutaciones_por_1k_vec",
    "config_por_1k_vec",
)

ETIQUETAS: dict[str, tuple[str, str]] = {
    "instr_total": ("Instrucciones totales", "instrucciones"),
    "instr_escalar": ("Instrucciones escalares", "instrucciones"),
    "instr_vector": ("Instrucciones vectoriales", "instrucciones"),
    "instr_vsetvl": ("Instrucciones vset*", "instrucciones"),
    "elems_total": ("Elementos procesados", "elementos"),
    "bytes_total": ("Bytes arquitectonicos totales", "bytes"),
    "bytes_escalar": ("Bytes escalares", "bytes"),
    "bytes_vector": ("Bytes vectoriales", "bytes"),
    "flops_total": ("FLOPs totales", "FLOPs"),
    "flops_escalar": ("FLOPs escalares", "FLOPs"),
    "flops_vector": ("FLOPs vectoriales", "FLOPs"),
    "oi_isa": ("Intensidad operacional ISA", "FLOPs/byte"),
    "oi_isa_vector": ("Intensidad operacional vectorial", "FLOPs/byte"),
    "flops_por_elemento": ("FLOPs por elemento", "FLOPs/elemento"),
    "bytes_por_elemento": ("Bytes por elemento", "bytes/elemento"),
    "ocupacion_media": ("Ocupacion media VL/VLMAX", "fraccion"),
    "vl_medio": ("VL medio", "elementos"),
    "vlmax_medio": ("VLMAX medio", "elementos"),
    "lmul_medio": ("LMUL medio", "LMUL"),
    "registros_vectoriales_unicos": ("Registros vectoriales unicos", "registros"),
    "dep_scalar_total": ("Dependencias escalares", "dependencias"),
    "dep_vector_total": ("Dependencias vectoriales", "dependencias"),
    "dep_raw_total": ("Dependencias RAW vectoriales", "dependencias"),
    "dep_waw_total": ("Dependencias WAW vectoriales", "dependencias"),
    "dep_war_total": ("Dependencias WAR vectoriales", "dependencias"),
    "dep_raw_dist_media": ("Distancia media RAW", "instrucciones"),
    "dep_waw_dist_media": ("Distancia media WAW", "instrucciones"),
    "dep_war_dist_media": ("Distancia media WAR", "instrucciones"),
    "raw_fraccion_le4": ("Fraccion RAW a distancia <= 4", "fraccion"),
    "war_fraccion_le8": ("Fraccion WAR a distancia <= 8", "fraccion"),
    "waw_fraccion_le8": ("Fraccion WAW a distancia <= 8", "fraccion"),
    "masked_instr": ("Instrucciones enmascaradas", "instrucciones"),
    "masked_arith_instr": ("Instrucciones enmascaradas aritmeticas", "instrucciones"),
    "masked_memory_instr": ("Instrucciones enmascaradas de memoria", "instrucciones"),
    "masked_fraccion": ("Fraccion de instrucciones enmascaradas", "fraccion"),
    "masked_densidad_media": ("Densidad media de mascara", "fraccion"),
    "masked_elementos_activos": ("Elementos activos enmascarados", "elementos"),
    "sv_eventos_total": ("Eventos escalar-vector", "eventos"),
    "sv_eventos_por_1k_vec": ("Eventos escalar-vector por 1k instr. vectoriales", "eventos/1k"),
    "sv_broadcast_vx": ("Broadcast escalar .vx", "instrucciones"),
    "sv_broadcast_vf": ("Broadcast escalar .vf", "instrucciones"),
    "sv_escalar_a_vector": ("Transferencias escalar -> vector", "instrucciones"),
    "sv_vector_a_escalar": ("Transferencias vector -> escalar", "instrucciones"),
    "sv_resultado_escalar": ("Instrucciones con resultado escalar", "instrucciones"),
    "sv_vsetvl": ("Configuracion vset*", "instrucciones"),
    "sv_elementos_broadcast_vx": ("Elementos consumidos por broadcast .vx", "elementos"),
    "sv_elementos_broadcast_vf": ("Elementos consumidos por broadcast .vf", "elementos"),
    "sv_elementos_activos_totales": ("Elementos activos procesados", "elementos"),
    "mov_instr_total": ("Instrucciones de movimiento en VRF", "instrucciones"),
    "mov_fraccion": ("Fraccion de movimiento en VRF", "fraccion"),
    "mov_bytes_vrf_total": ("Bytes estimados leidos/escritos en VRF", "bytes"),
    "mov_bytes_vrf_por_op_aritmetica": ("Bytes VRF por operacion aritmetica", "bytes/op"),
    "mov_slides_instr": ("Slides", "instrucciones"),
    "mov_gathers_instr": ("Gathers", "instrucciones"),
    "mov_compress_instr": ("Compress", "instrucciones"),
    "mov_reducciones_instr": ("Reducciones", "instrucciones"),
    "mov_whole_register_instr": ("Movimientos whole-register", "instrucciones"),
    "mov_mask_ops_scans_instr": ("Operaciones de mascara/scans", "instrucciones"),
    "mov_layout_conversions_instr": ("Conversiones de layout", "instrucciones"),
    "mov_slides_bytes_vrf": ("Bytes VRF de slides", "bytes"),
    "mov_gathers_bytes_vrf": ("Bytes VRF de gathers", "bytes"),
    "mov_compress_bytes_vrf": ("Bytes VRF de compress", "bytes"),
    "mov_reducciones_bytes_vrf": ("Bytes VRF de reducciones", "bytes"),
    "mov_whole_register_bytes_vrf": ("Bytes VRF de whole-register", "bytes"),
    "mov_mask_ops_scans_bytes_vrf": ("Bytes VRF de mascara/scans", "bytes"),
    "mov_layout_conversions_bytes_vrf": ("Bytes VRF de conversiones de layout", "bytes"),
    "politica_tu": ("Politica tail-undisturbed", "instrucciones"),
    "politica_ta": ("Politica tail-agnostic", "instrucciones"),
    "politica_mu": ("Politica mask-undisturbed", "instrucciones"),
    "politica_ma": ("Politica mask-agnostic", "instrucciones"),
    "tu_fraccion": ("Fraccion TU frente a TA", "fraccion"),
    "mu_fraccion": ("Fraccion MU frente a MA", "fraccion"),
    "tail_preservados": ("Elementos de tail preservados", "elementos"),
    "mask_preservados": ("Elementos de mascara preservados", "elementos"),
    "elementos_activos_escritos": ("Elementos activos escritos", "elementos"),
    "elementos_destino_totales": ("Elementos destino totales", "elementos"),
    "presion_preservacion": ("Presion de preservacion", "fraccion"),
    "presion_tail": ("Presion de tail", "fraccion"),
    "presion_mask": ("Presion de mascara", "fraccion"),
    "mem_unit_elems": ("Elementos de memoria unit-stride", "elementos"),
    "mem_strided_elems": ("Elementos de memoria strided", "elementos"),
    "mem_indexed_elems": ("Elementos de memoria indexada", "elementos"),
    "mem_total_elems": ("Elementos de memoria totales", "elementos"),
    "mem_unit_fraccion": ("Fraccion unit-stride", "fraccion"),
    "mem_strided_fraccion": ("Fraccion strided", "fraccion"),
    "mem_indexed_fraccion": ("Fraccion indexada", "fraccion"),
    "mem_irregular_fraccion": ("Fraccion de memoria irregular", "fraccion"),
    "config_instr": ("Instrucciones de configuracion", "instrucciones"),
    "loadstore_instr": ("Instrucciones load/store", "instrucciones"),
    "arith_int_instr": ("Instrucciones aritmeticas enteras", "instrucciones"),
    "arith_fp_instr": ("Instrucciones aritmeticas FP", "instrucciones"),
    "reduction_instr": ("Instrucciones de reduccion", "instrucciones"),
    "permutation_instr": ("Instrucciones de permutacion", "instrucciones"),
    "mask_instr": ("Instrucciones de mascara", "instrucciones"),
    "permutaciones_por_1k_vec": ("Permutaciones por 1k instr. vectoriales", "instrucciones/1k"),
    "config_por_1k_vec": ("Configuracion por 1k instr. vectoriales", "instrucciones/1k"),
    "loadstore_por_1k_vec": ("Load/store por 1k instr. vectoriales", "instrucciones/1k"),
    "vsetvl_por_1k_vec": ("vset* por 1k instr. vectoriales", "instrucciones/1k"),
    "instr_tree_total": ("Suma del arbol de instrucciones", "instrucciones"),
    "instr_tree_esperado": ("Instrucciones esperadas en el arbol", "instrucciones"),
    "instr_tree_delta": ("Diferencia arbol - esperado", "instrucciones"),
    "instr_tree_ok": ("Arbol coherente con los totales", "0/1"),
}

# Metricas aditivas: tienen sentido sumarlas entre benchmarks o ejecuciones.
METRICAS_ADITIVAS = (
    "instr_total",
    "instr_escalar",
    "instr_vector",
    "instr_vsetvl",
    "elems_total",
    "bytes_total",
    "bytes_escalar",
    "bytes_vector",
    "flops_total",
    "flops_escalar",
    "flops_vector",
    "elems_arith",
    "elems_reduction",
    "elems_mask",
    "dep_scalar_total",
    "dep_vector_total",
    "dep_raw_total",
    "dep_waw_total",
    "dep_war_total",
    "masked_instr",
    "masked_arith_instr",
    "masked_memory_instr",
    "masked_elementos_activos",
    "sv_eventos_total",
    "sv_broadcast_vx",
    "sv_broadcast_vf",
    "sv_escalar_a_vector",
    "sv_vector_a_escalar",
    "sv_resultado_escalar",
    "sv_vsetvl",
    "sv_elementos_broadcast_vx",
    "sv_elementos_broadcast_vf",
    "sv_elementos_activos_totales",
    "mov_instr_total",
    "mov_bytes_vrf_total",
    "mov_slides_instr",
    "mov_gathers_instr",
    "mov_compress_instr",
    "mov_reducciones_instr",
    "mov_whole_register_instr",
    "mov_mask_ops_scans_instr",
    "mov_layout_conversions_instr",
    "mov_slides_bytes_vrf",
    "mov_gathers_bytes_vrf",
    "mov_compress_bytes_vrf",
    "mov_reducciones_bytes_vrf",
    "mov_whole_register_bytes_vrf",
    "mov_mask_ops_scans_bytes_vrf",
    "mov_layout_conversions_bytes_vrf",
    "politica_tu",
    "politica_ta",
    "politica_mu",
    "politica_ma",
    "tail_preservados",
    "mask_preservados",
    "elementos_activos_escritos",
    "elementos_destino_totales",
    "mem_unit_elems",
    "mem_strided_elems",
    "mem_indexed_elems",
    "mem_total_elems",
    "config_instr",
    "loadstore_instr",
    "arith_int_instr",
    "arith_fp_instr",
    "reduction_instr",
    "permutation_instr",
    "mask_instr",
    "instr_tree_total",
    "instr_tree_esperado",
)


# ---------------------------------------------------------------------------
# Utilidades de lectura y calculo
# ---------------------------------------------------------------------------

def numero(valor: Any) -> float | None:
    """Devuelve un float finito o None."""
    if valor is None or isinstance(valor, bool):
        return None
    if isinstance(valor, (int, float)):
        v = float(valor)
        return v if math.isfinite(v) else None
    return None


def suma(valores: Iterable[float | None]) -> float | None:
    """Suma los valores no nulos; None si no hay ninguno."""
    validos = [v for v in valores if v is not None]
    return math.fsum(validos) if validos else None


def ratio(numerador: float | None, denominador: float | None) -> float | None:
    if numerador is None or denominador is None or denominador == 0:
        return None
    return numerador / denominador


def por_mil(numerador: float | None, denominador: float | None) -> float | None:
    if numerador is None:
        return None
    return ratio(1000.0 * numerador, denominador)


def obtener(obj: Any, *claves: str, default: Any = None) -> Any:
    actual = obj
    for clave in claves:
        if not isinstance(actual, dict) or clave not in actual:
            return default
        actual = actual[clave]
    return actual


def suma_arbol(nodo: Any) -> float | None:
    """Suma todas las hojas numericas de un arbol de categorias."""
    if isinstance(nodo, dict):
        return suma(suma_arbol(v) for v in nodo.values())
    return numero(nodo)


def suma_claves(obj: Any, claves: Iterable[str]) -> float | None:
    if not isinstance(obj, dict):
        return None
    return suma(numero(obj.get(c)) for c in claves)


def memoria_desglosada(bloque: dict) -> tuple[float | None, float | None, float | None]:
    mem = obtener(bloque, "elems_by_kind", "memory")
    if isinstance(mem, dict):
        return numero(mem.get("unit_stride")), numero(mem.get("strided")), numero(mem.get("indexed"))
    # Compatibilidad con resultados antiguos, donde memory era un entero.
    valor = numero(mem)
    if valor is None:
        return None, None, None
    return valor, 0.0, 0.0


def fraccion_histograma(dep: dict, bins: Iterable[str]) -> float | None:
    hist = dep.get("histogram")
    if not isinstance(hist, dict):
        return None
    total = numero(dep.get("count"))
    if total is None or total <= 0:
        total = suma(numero(v) for v in hist.values())
    parte = suma_claves(hist, bins)
    return ratio(parte, total)


def extraer_metricas(doc: dict, region: dict) -> dict[str, float | None]:
    counters = region.get("counters") or {}
    prev = counters.get("instructions_previous_version") or {}
    bloques = prev.get("sew") or []
    if not isinstance(bloques, list):
        bloques = []

    m: dict[str, float | None] = {}

    # Totales basicos
    m["instr_total"] = numero(prev.get("total"))
    m["instr_escalar"] = numero(prev.get("scalar"))
    m["instr_vsetvl"] = numero(prev.get("vsetvl"))
    m["instr_vector"] = numero(prev.get("vector"))

    instr_sew = suma(numero(b.get("instr")) for b in bloques if isinstance(b, dict))
    if m["instr_vector"] is None:
        m["instr_vector"] = instr_sew
    m["elems_total"] = suma(numero(b.get("elems")) for b in bloques if isinstance(b, dict))
    m["elems_arith"] = suma(numero(obtener(b, "elems_by_kind", "arith")) for b in bloques if isinstance(b, dict))
    m["elems_reduction"] = suma(numero(obtener(b, "elems_by_kind", "reduction")) for b in bloques if isinstance(b, dict))
    m["elems_mask"] = suma(numero(obtener(b, "elems_by_kind", "mask")) for b in bloques if isinstance(b, dict))

    # Memoria
    unidades = []
    strided = []
    indexadas = []
    for b in bloques:
        if not isinstance(b, dict):
            continue
        u, s, i = memoria_desglosada(b)
        unidades.append(u)
        strided.append(s)
        indexadas.append(i)
    m["mem_unit_elems"] = suma(unidades)
    m["mem_strided_elems"] = suma(strided)
    m["mem_indexed_elems"] = suma(indexadas)
    m["mem_total_elems"] = suma((m["mem_unit_elems"], m["mem_strided_elems"], m["mem_indexed_elems"]))
    m["mem_unit_fraccion"] = ratio(m["mem_unit_elems"], m["mem_total_elems"])
    m["mem_strided_fraccion"] = ratio(m["mem_strided_elems"], m["mem_total_elems"])
    m["mem_indexed_fraccion"] = ratio(m["mem_indexed_elems"], m["mem_total_elems"])
    m["mem_irregular_fraccion"] = ratio(
        suma((m["mem_strided_elems"], m["mem_indexed_elems"])), m["mem_total_elems"]
    )

    # Bytes y FLOPs
    mb = counters.get("moved_bytes") or {}
    fl = counters.get("flops") or {}
    m["bytes_total"] = numero(mb.get("total"))
    m["bytes_escalar"] = numero(mb.get("scalar"))
    m["bytes_vector"] = numero(mb.get("vector"))
    m["flops_total"] = numero(fl.get("total"))
    m["flops_escalar"] = numero(fl.get("scalar"))
    m["flops_vector"] = numero(fl.get("vector"))
    m["oi_isa"] = ratio(m["flops_total"], m["bytes_total"])
    m["oi_isa_vector"] = ratio(m["flops_vector"], m["bytes_vector"])
    m["flops_por_elemento"] = ratio(m["flops_total"], m["elems_total"])
    m["bytes_por_elemento"] = ratio(m["bytes_total"], m["elems_total"])

    # Estadisticas globales
    gs = counters.get("global_stats") or {}
    m["ocupacion_media"] = numero(gs.get("avg_occupancy"))
    m["vl_medio"] = numero(gs.get("avg_vl_elems"))
    m["vlmax_medio"] = numero(gs.get("avg_vlmax_elems"))
    m["lmul_medio"] = numero(gs.get("avg_lmul"))
    m["registros_vectoriales_unicos"] = numero(gs.get("unique_vector_registers"))
    m["vsetvl_por_1k_vec"] = por_mil(m["instr_vsetvl"], m["instr_vector"])

    # Dependencias
    dep = counters.get("dependencies") or {}
    dep_vec = dep.get("vector") or {}
    dep_esc = dep.get("scalar") or {}
    m["dep_scalar_total"] = numero(dep_esc.get("total"))
    m["dep_vector_total"] = numero(dep_vec.get("total"))
    for clave in ("raw", "waw", "war"):
        d = dep_vec.get(clave) or {}
        m[f"dep_{clave}_total"] = numero(d.get("count"))
        m[f"dep_{clave}_dist_media"] = numero(d.get("avg_dist"))
    m["raw_fraccion_le4"] = fraccion_histograma(dep_vec.get("raw") or {}, ("1", "2", "3", "4"))
    m["war_fraccion_le8"] = fraccion_histograma(dep_vec.get("war") or {}, ("1", "2", "3", "4", "5-8"))
    m["waw_fraccion_le8"] = fraccion_histograma(dep_vec.get("waw") or {}, ("1", "2", "3", "4", "5-8"))

    # Mascaras
    masked = counters.get("masked") or {}
    masked_arith = masked.get("arith") or {}
    masked_mem = masked.get("memory") or {}
    m["masked_arith_instr"] = numero(masked_arith.get("instr"))
    m["masked_memory_instr"] = numero(masked_mem.get("instr"))
    m["masked_instr"] = suma((m["masked_arith_instr"], m["masked_memory_instr"]))
    m["masked_elementos_activos"] = numero(masked.get("masked_active_elements"))
    m["masked_densidad_media"] = numero(masked.get("avg_density"))
    m["masked_fraccion"] = ratio(m["masked_instr"], m["instr_vector"])

    # Arbol de instrucciones
    instructions = region.get("instructions") or {}
    totales_categoria: dict[str, float | None] = {}
    if isinstance(instructions, dict):
        for nombre, nodo in instructions.items():
            totales_categoria[str(nombre)] = suma_arbol(nodo)
    m["instr_tree_total"] = suma(totales_categoria.values())
    if m["instr_total"] is not None and m["instr_escalar"] is not None:
        esperado = m["instr_total"] - m["instr_escalar"]
        m["instr_tree_esperado"] = esperado
        if m["instr_tree_total"] is not None:
            delta = m["instr_tree_total"] - esperado
            m["instr_tree_delta"] = delta
            m["instr_tree_ok"] = 1.0 if abs(delta) < 1e-6 else 0.0
    m["config_instr"] = totales_categoria.get("configuration_setting")
    m["loadstore_instr"] = totales_categoria.get("vector_loads_and_stores")
    m["arith_int_instr"] = totales_categoria.get("vector_integer_arithmetic")
    m["arith_fp_instr"] = totales_categoria.get("vector_floating_point")
    m["reduction_instr"] = totales_categoria.get("vector_reduction")
    m["permutation_instr"] = totales_categoria.get("vector_permutation")
    m["mask_instr"] = totales_categoria.get("vector_mask")
    m["permutaciones_por_1k_vec"] = por_mil(m["permutation_instr"], m["instr_vector"])
    m["config_por_1k_vec"] = por_mil(m["config_instr"], m["instr_vector"])
    m["loadstore_por_1k_vec"] = por_mil(m["loadstore_instr"], m["instr_vector"])

    # Interfaz escalar-vector, movimiento y politicas por SEW.
    sv_eventos: dict[str, list[float | None]] = {k: [] for k in EVENTOS_SV}
    sv_elementos = {
        "broadcast_vx_consumed_elements": [],
        "broadcast_vf_consumed_elements": [],
        "total_active_elements_processed": [],
    }
    movimiento = {
        c: {"instr": [], "bytes_read": [], "bytes_written": []}
        for c in CATEGORIAS_MOV
    }
    politicas = {
        "tu": [],
        "ta": [],
        "mu": [],
        "ma": [],
        "tail": [],
        "mask": [],
        "activos": [],
        "destino": [],
    }

    for b in bloques:
        if not isinstance(b, dict):
            continue
        sv = b.get("scalar_vector_interface") or {}
        ev = sv.get("events_count") or {}
        el = sv.get("elements_affected") or {}
        for clave in EVENTOS_SV:
            sv_eventos[clave].append(numero(ev.get(clave)))
        for clave in sv_elementos:
            sv_elementos[clave].append(numero(el.get(clave)))

        mp = b.get("movement_profile") or {}
        cats = mp.get("categories") or {}
        for cat in CATEGORIAS_MOV:
            c = cats.get(cat) or {}
            movimiento[cat]["instr"].append(numero(c.get("instr")))
            movimiento[cat]["bytes_read"].append(numero(c.get("vrf_bytes_read")))
            movimiento[cat]["bytes_written"].append(numero(c.get("vrf_bytes_written")))

        pol = b.get("policies") or {}
        ps = pol.get("policy_selection") or {}
        pp = pol.get("preservation_pressure") or {}
        politicas["tu"].append(numero(ps.get("tu_instructions")))
        politicas["ta"].append(numero(ps.get("ta_instructions")))
        politicas["mu"].append(numero(ps.get("mu_masked_instructions")))
        politicas["ma"].append(numero(ps.get("ma_masked_instructions")))
        politicas["tail"].append(numero(pp.get("tail_preserved_elements")))
        politicas["mask"].append(numero(pp.get("mask_preserved_elements")))
        politicas["activos"].append(numero(pp.get("active_written_elements")))
        politicas["destino"].append(numero(pp.get("total_destination_elements")))

    for clave in EVENTOS_SV:
        m[f"sv_{clave}"] = suma(sv_eventos[clave])
    m["sv_escalar_a_vector"] = m["sv_scalar_to_vector"]
    m["sv_vector_a_escalar"] = m["sv_vector_to_scalar"]
    m["sv_resultado_escalar"] = m["sv_scalar_result"]
    m["sv_vsetvl"] = m["sv_vsetvl_config"]
    m["sv_elementos_broadcast_vx"] = suma(sv_elementos["broadcast_vx_consumed_elements"])
    m["sv_elementos_broadcast_vf"] = suma(sv_elementos["broadcast_vf_consumed_elements"])
    m["sv_elementos_activos_totales"] = suma(sv_elementos["total_active_elements_processed"])
    m["sv_eventos_total"] = suma(m[f"sv_{k}"] for k in EVENTOS_SV)
    m["sv_eventos_por_1k_vec"] = por_mil(m["sv_eventos_total"], m["instr_vector"])

    for cat in CATEGORIAS_MOV:
        m[f"mov_{cat}_instr"] = suma(movimiento[cat]["instr"])
        leidos = suma(movimiento[cat]["bytes_read"])
        escritos = suma(movimiento[cat]["bytes_written"])
        m[f"mov_{cat}_bytes_vrf"] = suma((leidos, escritos))
    m["mov_instr_total"] = suma(m[f"mov_{c}_instr"] for c in CATEGORIAS_MOV)
    m["mov_bytes_vrf_total"] = suma(m[f"mov_{c}_bytes_vrf"] for c in CATEGORIAS_MOV)
    m["mov_fraccion"] = ratio(m["mov_instr_total"], m["instr_vector"])
    m["mov_bytes_vrf_por_op_aritmetica"] = ratio(
        m["mov_bytes_vrf_total"],
        suma((m["arith_int_instr"], m["arith_fp_instr"])),
    )

    m["politica_tu"] = suma(politicas["tu"])
    m["politica_ta"] = suma(politicas["ta"])
    m["politica_mu"] = suma(politicas["mu"])
    m["politica_ma"] = suma(politicas["ma"])
    m["tu_fraccion"] = ratio(m["politica_tu"], suma((m["politica_tu"], m["politica_ta"])))
    m["mu_fraccion"] = ratio(m["politica_mu"], suma((m["politica_mu"], m["politica_ma"])))
    m["tail_preservados"] = suma(politicas["tail"])
    m["mask_preservados"] = suma(politicas["mask"])
    m["elementos_activos_escritos"] = suma(politicas["activos"])
    m["elementos_destino_totales"] = suma(politicas["destino"])
    m["presion_preservacion"] = ratio(
        suma((m["tail_preservados"], m["mask_preservados"])),
        m["elementos_destino_totales"],
    )
    m["presion_tail"] = ratio(m["tail_preservados"], m["elementos_destino_totales"])
    m["presion_mask"] = ratio(m["mask_preservados"], m["elementos_destino_totales"])

    return m


# ---------------------------------------------------------------------------
# Lectura de ficheros
# ---------------------------------------------------------------------------

def detectar_metadatos(ruta: Path, raiz: Path) -> dict[str, str]:
    """Separa conjunto (RiVEC, apps_bench, ...), tamano y familia."""
    rel = ruta.relative_to(raiz)
    partes = rel.parts[:-1]
    if not partes:
        if raiz.name.lower() in TAMANOS:
            return {"conjunto": "rivec", "tamano": raiz.name.lower(), "familia": "rivec"}
        conjunto = raiz.name or "resultados"
        return {"conjunto": conjunto, "tamano": "no_aplica", "familia": conjunto}
    if partes[0].lower() in TAMANOS:
        return {"conjunto": "rivec", "tamano": partes[0].lower(), "familia": "rivec"}
    conjunto = partes[0]
    tamano = next((p.lower() for p in partes if p.lower() in TAMANOS), "no_aplica")
    familia = partes[1] if len(partes) >= 2 else conjunto
    return {"conjunto": conjunto, "tamano": tamano, "familia": familia}


def coincide_benchmark(nombre: str, patrones: list[str] | None) -> bool:
    if not patrones:
        return True
    for patron in patrones:
        if any(c in patron for c in "*?["):
            if fnmatch.fnmatchcase(nombre, patron):
                return True
        elif nombre == patron:
            return True
    return False


def cargar_filas(
    raiz: Path,
    tamanos: list[str] | None,
    conjuntos: list[str] | None,
    familias: list[str] | None,
    benchmarks: list[str] | None,
    regiones: list[str] | None,
) -> tuple[list[dict], list[dict], list[str]]:
    filas: list[dict] = []
    errores: list[dict] = []
    avisos: list[str] = []

    if not raiz.is_dir():
        raise SystemExit(f"No existe el directorio de resultados: {raiz}")

    archivos = sorted(p for p in raiz.rglob("*.json") if p.is_file())
    if not archivos:
        raise SystemExit(f"No hay ficheros .json en {raiz}")

    for ruta in archivos:
        meta = detectar_metadatos(ruta, raiz)
        if tamanos and meta["tamano"] not in tamanos:
            continue
        if conjuntos and meta["conjunto"] not in conjuntos:
            continue
        if familias and meta["familia"] not in familias:
            continue
        run = ruta.stem
        benchmark = run
        if not coincide_benchmark(benchmark, benchmarks):
            continue
        try:
            doc = json.loads(ruta.read_text(encoding="utf-8"))
        except Exception as exc:
            errores.append({"archivo": str(ruta), "error": str(exc)})
            continue
        if not isinstance(doc, dict):
            errores.append({"archivo": str(ruta), "error": "el JSON raiz no es un objeto"})
            continue
        lista_regiones = doc.get("regions") or []
        if not isinstance(lista_regiones, list) or not lista_regiones:
            avisos.append(f"{ruta.relative_to(raiz)}: sin regiones")
            continue
        for idx, region in enumerate(lista_regiones):
            if not isinstance(region, dict):
                avisos.append(f"{ruta.relative_to(raiz)}: region {idx} no es un objeto")
                continue
            nombre_region = region.get("name") or f"region_{idx}"
            if regiones and nombre_region not in regiones:
                continue
            metricas = extraer_metricas(doc, region)
            rel = ruta.relative_to(raiz)
            carpeta = rel.parent.as_posix()
            if carpeta == ".":
                carpeta = "raiz"
            filas.append(
                {
                    "archivo": rel.as_posix(),
                    "carpeta": carpeta,
                    "conjunto": meta["conjunto"],
                    "tamano": meta["tamano"],
                    "familia": meta["familia"],
                    "benchmark": benchmark,
                    "run": run,
                    "region": nombre_region,
                    "region_idx": idx,
                    "esquema": "nuevo" if "RAW_DIST" in doc else "antiguo",
                    "trace_extended": doc.get("trace_extended"),
                    "vlen_bits": doc.get("vlen_bits"),
                    "generador": doc.get("generator"),
                    "binario": doc.get("binary"),
                    "metricas": metricas,
                }
            )
    return filas, errores, avisos


# ---------------------------------------------------------------------------
# Estadisticas
# ---------------------------------------------------------------------------

def percentil(valores: list[float], p: float) -> float:
    if len(valores) == 1:
        return valores[0]
    if np is not None:
        return float(np.percentile(valores, p, method="linear"))
    k = (len(valores) - 1) * p / 100.0
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return valores[int(k)]
    return valores[f] * (c - k) + valores[c] * (k - f)


def estadisticas(valores: Iterable[float | None]) -> dict[str, float | int] | None:
    validos = sorted(v for v in valores if v is not None)
    n = len(validos)
    if n == 0:
        return None
    q1 = percentil(validos, 25.0)
    mediana = percentil(validos, 50.0)
    q3 = percentil(validos, 75.0)
    return {
        "n": n,
        "media": statistics.fmean(validos),
        "desviacion": statistics.stdev(validos) if n > 1 else 0.0,
        "minimo": validos[0],
        "q1": q1,
        "mediana": mediana,
        "q3": q3,
        "maximo": validos[-1],
        "iqr": q3 - q1,
        "p10": percentil(validos, 10.0),
        "p90": percentil(validos, 90.0),
    }


def clave_carpeta(fila: dict) -> str:
    return str(fila["carpeta"])


def clave_tamano(fila: dict) -> str:
    return str(fila["tamano"])


def clave_conjunto(fila: dict) -> str:
    return str(fila["conjunto"])


def clave_familia(fila: dict) -> str:
    return str(fila["familia"])


def clave_conjunto_familia(fila: dict) -> str:
    return f"{fila['conjunto']}/{fila['familia']}"


def clave_benchmark(fila: dict) -> str:
    return str(fila["benchmark"])


def clave_region(fila: dict) -> str:
    return str(fila["region"])


def clave_benchmark_tamano(fila: dict) -> str:
    return f"{fila['benchmark']} [{fila['tamano']}]"


CLAVES: dict[str, Callable[[dict], str]] = {
    "carpeta": clave_carpeta,
    "conjunto": clave_conjunto,
    "tamano": clave_tamano,
    "familia": clave_familia,
    "conjunto_familia": clave_conjunto_familia,
    "benchmark": clave_benchmark,
    "region": clave_region,
    "benchmark_tamano": clave_benchmark_tamano,
}


def ordenar_grupo(grupo: str, eje: str) -> tuple:
    if eje == "carpeta":
        return (grupo.count("/"), grupo)
    if eje == "tamano":
        try:
            return (TAMANOS.index(grupo), grupo)
        except ValueError:
            return (len(TAMANOS), grupo)
    if eje == "conjunto":
        orden = ("rivec", "apps_bench", "assembly_microbench")
        try:
            return (orden.index(grupo), grupo)
        except ValueError:
            return (len(orden), grupo)
    if eje == "familia":
        orden = ("rivec", "qsim_rvv", "arith_instr", "ldst_instr")
        try:
            return (orden.index(grupo), grupo)
        except ValueError:
            return (len(orden), grupo)
    if eje == "conjunto_familia":
        conjunto, _, familia = grupo.partition("/")
        return (ordenar_grupo(conjunto, "conjunto"), ordenar_grupo(familia, "familia"))
    if eje == "benchmark_tamano":
        benchmark, _, tamano = grupo.partition(" [")
        tamano = tamano.rstrip("]")
        try:
            pos = TAMANOS.index(tamano)
        except ValueError:
            pos = len(TAMANOS)
        return (benchmark, pos, tamano)
    return (grupo,)


def resolver_ejes_auto(filas: list[dict]) -> list[str]:
    """Deduce el eje de comparacion a partir de la estructura de resultados.

    Prioriza la carpeta que contiene cada JSON (por ejemplo
    assembly_microbench/arith_instr). Si todas las ejecuciones estan en la
    misma carpeta, usa familia, conjunto, tamano o benchmark segun lo que
    realmente tenga varias muestras.
    """
    def grupos(eje: str) -> dict[str, int]:
        cuenta: dict[str, int] = defaultdict(int)
        for fila in filas:
            cuenta[CLAVES[eje](fila)] += 1
        return dict(cuenta)

    def tiene_varias_muestras(eje: str) -> bool:
        cuenta = grupos(eje)
        return len(cuenta) >= 2 and max(cuenta.values(), default=0) >= 2

    if tiene_varias_muestras("carpeta"):
        return ["carpeta"]
    if tiene_varias_muestras("familia"):
        return ["familia"]
    if tiene_varias_muestras("conjunto"):
        return ["conjunto"]

    tamanos = grupos("tamano")
    tamanos_reales = {k: v for k, v in tamanos.items() if k != "no_aplica"}
    if len(tamanos_reales) >= 2:
        return ["tamano"]

    benchmarks = grupos("benchmark")
    if max(benchmarks.values(), default=0) >= 2:
        return ["benchmark"]
    if len(benchmarks) >= 2:
        return ["benchmark"]
    return ["carpeta"]


def columnas_metricas(filas: list[dict]) -> list[str]:
    presentes: set[str] = set()
    for fila in filas:
        presentes.update(fila["metricas"].keys())
    columnas = [m for m in ORDEN_METRICAS if m in presentes]
    columnas.extend(sorted(presentes - set(columnas)))
    return columnas


def etiqueta_metrica(metrica: str) -> tuple[str, str]:
    return ETIQUETAS.get(metrica, (metrica, ""))


def escribir_csv(ruta: Path, campos: list[str], filas: Iterable[dict]) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=campos, extrasaction="ignore")
        writer.writeheader()
        for fila in filas:
            salida = {}
            for campo in campos:
                valor = fila.get(campo)
                if valor is None:
                    salida[campo] = ""
                elif isinstance(valor, bool):
                    salida[campo] = "1" if valor else "0"
                elif isinstance(valor, float):
                    salida[campo] = f"{valor:.10g}"
                else:
                    salida[campo] = valor
            writer.writerow(salida)


def generar_estadisticas(filas: list[dict], eje: str, metricas: list[str]) -> list[dict]:
    grupos: dict[str, list[float | None]] = defaultdict(list)
    clave = CLAVES[eje]
    for fila in filas:
        grupos[clave(fila)].append(fila)
    resultados: list[dict] = []
    for metrica in metricas:
        for grupo in sorted(grupos, key=lambda g: ordenar_grupo(g, eje)):
            valores = [f["metricas"].get(metrica) for f in grupos[grupo]]
            est = estadisticas(valores)
            if est is None:
                continue
            resultados.append({"metrica": metrica, "grupo": grupo, **est})
    return resultados


def agregar(filas: list[dict], eje: str) -> list[dict]:
    grupos: dict[str, list[dict]] = defaultdict(list)
    clave = CLAVES[eje]
    for fila in filas:
        grupos[clave(fila)].append(fila)
    salida: list[dict] = []
    for grupo in sorted(grupos, key=lambda g: ordenar_grupo(g, eje)):
        fs = grupos[grupo]
        sums: dict[str, Any] = {
            "grupo": grupo,
            "n_registros": len(fs),
            "n_archivos": len({f["archivo"] for f in fs}),
            "n_benchmarks": len({f["benchmark"] for f in fs}),
            "n_tamanos": len({f["tamano"] for f in fs}),
        }
        for metrica in METRICAS_ADITIVAS:
            sums[metrica] = suma(f["metricas"].get(metrica) for f in fs)

        # Ratios recalculados a partir de los totales, no media de ratios.
        sums["oi_isa"] = ratio(sums["flops_total"], sums["bytes_total"])
        sums["oi_isa_vector"] = ratio(sums["flops_vector"], sums["bytes_vector"])
        sums["flops_por_elemento"] = ratio(sums["flops_total"], sums["elems_total"])
        sums["bytes_por_elemento"] = ratio(sums["bytes_total"], sums["elems_total"])
        sums["masked_fraccion"] = ratio(sums["masked_instr"], sums["instr_vector"])
        sums["sv_eventos_por_1k_vec"] = por_mil(sums["sv_eventos_total"], sums["instr_vector"])
        sums["mov_fraccion"] = ratio(sums["mov_instr_total"], sums["instr_vector"])
        sums["mov_bytes_vrf_por_op_aritmetica"] = ratio(
            sums["mov_bytes_vrf_total"],
            suma((sums["arith_int_instr"], sums["arith_fp_instr"])),
        )
        sums["tu_fraccion"] = ratio(
            sums["politica_tu"], suma((sums["politica_tu"], sums["politica_ta"]))
        )
        sums["mu_fraccion"] = ratio(
            sums["politica_mu"], suma((sums["politica_mu"], sums["politica_ma"]))
        )
        sums["presion_preservacion"] = ratio(
            suma((sums["tail_preservados"], sums["mask_preservados"])),
            sums["elementos_destino_totales"],
        )
        sums["presion_tail"] = ratio(sums["tail_preservados"], sums["elementos_destino_totales"])
        sums["presion_mask"] = ratio(sums["mask_preservados"], sums["elementos_destino_totales"])
        sums["mem_unit_fraccion"] = ratio(sums["mem_unit_elems"], sums["mem_total_elems"])
        sums["mem_strided_fraccion"] = ratio(sums["mem_strided_elems"], sums["mem_total_elems"])
        sums["mem_indexed_fraccion"] = ratio(sums["mem_indexed_elems"], sums["mem_total_elems"])
        sums["mem_irregular_fraccion"] = ratio(
            suma((sums["mem_strided_elems"], sums["mem_indexed_elems"])),
            sums["mem_total_elems"],
        )
        sums["permutaciones_por_1k_vec"] = por_mil(sums["permutation_instr"], sums["instr_vector"])
        sums["config_por_1k_vec"] = por_mil(sums["config_instr"], sums["instr_vector"])
        sums["loadstore_por_1k_vec"] = por_mil(sums["loadstore_instr"], sums["instr_vector"])
        sums["vsetvl_por_1k_vec"] = por_mil(sums["instr_vsetvl"], sums["instr_vector"])

        # Medias simples de las metricas no aditivas (se indican con prefijo media_).
        no_aditivas = (
            "ocupacion_media",
            "vl_medio",
            "vlmax_medio",
            "lmul_medio",
            "registros_vectoriales_unicos",
            "dep_raw_dist_media",
            "dep_waw_dist_media",
            "dep_war_dist_media",
            "raw_fraccion_le4",
            "war_fraccion_le8",
            "waw_fraccion_le8",
            "masked_densidad_media",
        )
        for metrica in no_aditivas:
            valores = [f["metricas"].get(metrica) for f in fs]
            est = estadisticas(valores)
            sums[f"media_{metrica}"] = est["media"] if est else None

        salida.append(sums)
    return salida


# ---------------------------------------------------------------------------
# Diagramas de cajas
# ---------------------------------------------------------------------------

def datos_grafica(
    filas: list[dict], metrica: str, eje: str, min_muestras: int
) -> tuple[list[str], list[list[float]]]:
    clave = CLAVES[eje]
    grupos: dict[str, list[float]] = defaultdict(list)
    for fila in filas:
        valor = fila["metricas"].get(metrica)
        if valor is not None:
            grupos[clave(fila)].append(valor)
    etiquetas: list[str] = []
    datos: list[list[float]] = []
    for grupo in sorted(grupos, key=lambda g: ordenar_grupo(g, eje)):
        valores = grupos[grupo]
        if len(valores) >= min_muestras:
            etiquetas.append(grupo)
            datos.append(valores)
    return etiquetas, datos


def generar_boxplots(
    filas: list[dict],
    salida: Path,
    ejes: list[str],
    metricas: list[str],
    min_muestras: int,
    dpi: int,
    formato: str,
    mostrar_puntos: bool,
) -> tuple[list[str], list[dict]]:
    if np is None:
        return [], [{"error": f"numpy no disponible: {_NUMPY_ERROR}"}]
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as exc:
        return [], [{"error": f"matplotlib no disponible: {exc}"}]

    plt.rcParams.update(
        {
            "font.size": 9,
            "axes.titlesize": 11,
            "axes.labelsize": 9,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
        }
    )
    generados: list[str] = []
    omitidos: list[dict] = []
    rng = np.random.default_rng(12345)

    for eje in ejes:
        for metrica in metricas:
            etiquetas, datos = datos_grafica(filas, metrica, eje, min_muestras)
            if not etiquetas:
                omitidos.append(
                    {
                        "metrica": metrica,
                        "eje": eje,
                        "motivo": f"sin grupos con n >= {min_muestras}",
                    }
                )
                continue
            nombre, unidad = etiqueta_metrica(metrica)
            etiquetas_con_n = [f"{e}\n(n={len(d)})" for e, d in zip(etiquetas, datos)]

            ancho = min(30.0, max(7.0, 0.55 * len(datos) + 3.0))
            fig, ax = plt.subplots(figsize=(ancho, 4.8))
            bp = ax.boxplot(
                datos,
                tick_labels=etiquetas_con_n,
                patch_artist=True,
                showmeans=True,
                widths=0.55,
                whis=1.5,
                medianprops={"color": "#1a1a1a", "linewidth": 1.6},
                meanprops={
                    "marker": "D",
                    "markerfacecolor": "white",
                    "markeredgecolor": "#1a1a1a",
                    "markersize": 4,
                },
                flierprops={
                    "marker": "o",
                    "markerfacecolor": "none",
                    "markeredgecolor": "#666666",
                    "markersize": 3,
                },
            )
            colores = plt.get_cmap("tab20").colors
            for idx, caja in enumerate(bp["boxes"]):
                caja.set_facecolor(colores[idx % len(colores)])
                caja.set_alpha(0.72)
                caja.set_edgecolor("#333333")
                caja.set_linewidth(0.8)

            if mostrar_puntos:
                for idx, valores in enumerate(datos, start=1):
                    if not valores:
                        continue
                    jitter = rng.uniform(-0.13, 0.13, size=len(valores))
                    ax.scatter(
                        np.full(len(valores), idx, dtype=float) + jitter,
                        valores,
                        s=12,
                        color="#111111",
                        alpha=0.55,
                        linewidths=0,
                        zorder=3,
                    )

            ax.set_title(nombre)
            ax.set_ylabel(f"{nombre} [{unidad}]" if unidad else nombre)
            ax.set_xlabel(
                {
                    "carpeta": "Carpeta de resultados",
                    "conjunto": "Conjunto de resultados",
                    "tamano": "Tamano del problema",
                    "familia": "Familia de benchmark",
                    "conjunto_familia": "Conjunto y familia",
                    "benchmark": "Benchmark",
                    "region": "Region",
                    "benchmark_tamano": "Benchmark y tamano",
                }.get(eje, eje)
            )
            ax.grid(axis="y", alpha=0.28)
            ax.set_axisbelow(True)
            rotar = eje in (
                "carpeta", "benchmark", "benchmark_tamano", "familia", "conjunto_familia"
            )
            for label in ax.get_xticklabels():
                label.set_rotation(35 if rotar else 0)
                label.set_horizontalalignment("right" if rotar else "center")
            fig.tight_layout()

            destino = salida / "boxplots" / f"por_{eje}" / f"{metrica}.{formato}"
            destino.parent.mkdir(parents=True, exist_ok=True)
            fig.savefig(destino, dpi=dpi, bbox_inches="tight")
            plt.close(fig)
            generados.append(destino.as_posix())
            print(f"[boxplot] {destino.relative_to(salida)}")

    return generados, omitidos


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parsear_lista(valor: str | None) -> list[str] | None:
    if not valor:
        return None
    return [x.strip() for x in valor.split(",") if x.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Calcula totales/estadisticas y diagramas de cajas de resultados RAVE.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--resultados",
        type=Path,
        default=BASE.parent / "resultados",
        help="Directorio raiz de los JSON de resultados (por defecto ../resultados).",
    )
    parser.add_argument(
        "--salida",
        type=Path,
        default=BASE / "salida",
        help="Directorio donde escribir CSV y graficas.",
    )
    parser.add_argument(
        "--tamano",
        action="append",
        help="Filtrar por tamano (tiny/small/medium/large/no_aplica). Se puede repetir.",
    )
    parser.add_argument(
        "--conjunto",
        action="append",
        help="Filtrar por conjunto (rivec, apps_bench, assembly_microbench, ...).",
    )
    parser.add_argument(
        "--familia",
        action="append",
        help="Filtrar por familia (rivec, qsim_rvv, arith_instr, ldst_instr, ...).",
    )
    parser.add_argument(
        "--benchmark",
        action="append",
        help="Filtrar por benchmark exacto o patron glob (ej. spmv, 'mat*').",
    )
    parser.add_argument(
        "--region",
        action="append",
        help="Filtrar por nombre de region. Se puede repetir.",
    )
    parser.add_argument(
        "--ejes",
        default="auto",
        help=(
            "Ejes de agrupacion para cajas y estadisticas. 'auto' (por defecto) "
            "deduce la agrupacion de la estructura de resultados; tambien admite "
            "carpeta, conjunto, tamano, familia, conjunto_familia, benchmark, "
            "region o benchmark_tamano."
        ),
    )
    parser.add_argument(
        "--metricas",
        help="Lista separada por comas de metricas a graficar. 'todas' para todas.",
    )
    parser.add_argument(
        "--min-muestras",
        type=int,
        default=1,
        help="Minimo de valores por caja para dibujarla.",
    )
    parser.add_argument(
        "--sin-graficas",
        action="store_true",
        help="No generar diagramas de cajas.",
    )
    parser.add_argument(
        "--sin-puntos",
        action="store_true",
        help="No superponer los puntos individuales sobre las cajas.",
    )
    parser.add_argument(
        "--formato",
        choices=("png", "svg", "pdf"),
        default="png",
        help="Formato de las graficas.",
    )
    parser.add_argument("--dpi", type=int, default=150, help="Resolucion de las graficas.")
    parser.add_argument(
        "--listar-metricas",
        action="store_true",
        help="Muestra las metricas disponibles y termina.",
    )
    args = parser.parse_args()

    if args.min_muestras < 1:
        parser.error("--min-muestras debe ser >= 1")

    ejes_solicitados = (args.ejes or "").strip()
    modo_auto = ejes_solicitados.lower() == "auto"
    if modo_auto:
        ejes = []
    else:
        ejes = parsear_lista(ejes_solicitados) or []
        if not ejes:
            parser.error("--ejes no puede estar vacio")
        ejes_desconocidos = [e for e in ejes if e not in CLAVES]
        if ejes_desconocidos:
            parser.error(f"Ejes no validos: {', '.join(ejes_desconocidos)}")

    print(f"Resultados: {args.resultados}")
    filas, errores, avisos = cargar_filas(
        args.resultados,
        parsear_lista(",".join(args.tamano)) if args.tamano else None,
        parsear_lista(",".join(args.conjunto)) if args.conjunto else None,
        parsear_lista(",".join(args.familia)) if args.familia else None,
        args.benchmark,
        args.region,
    )
    if not filas:
        print("No se han encontrado filas validas.", file=sys.stderr)
        for error in errores:
            print(f"  ERROR {error['archivo']}: {error['error']}", file=sys.stderr)
        return 1

    metricas_disponibles = columnas_metricas(filas)
    if args.listar_metricas:
        for metrica in metricas_disponibles:
            nombre, unidad = etiqueta_metrica(metrica)
            print(f"{metrica:38s} {nombre}" + (f" [{unidad}]" if unidad else ""))
        return 0

    if modo_auto:
        ejes = resolver_ejes_auto(filas)
        print(f"Ejes automaticos: {', '.join(ejes)}")
    else:
        print(f"Ejes: {', '.join(ejes)}")
    ejes_unicos = list(dict.fromkeys(ejes))

    if args.metricas:
        if args.metricas.strip().lower() == "todas":
            metricas_graficar = metricas_disponibles
        else:
            solicitadas = parsear_lista(args.metricas) or []
            metricas_graficar = [m for m in solicitadas if m in metricas_disponibles]
            faltantes = [m for m in solicitadas if m not in metricas_disponibles]
            if faltantes:
                print(f"Aviso: metricas no disponibles: {', '.join(faltantes)}")
    else:
        metricas_graficar = [m for m in METRICAS_POR_DEFECTO if m in metricas_disponibles]

    args.salida.mkdir(parents=True, exist_ok=True)

    # Totales por fichero/region.
    columnas = list(METADATOS) + metricas_disponibles
    filas_csv = []
    for fila in filas:
        salida = {k: fila.get(k) for k in METADATOS}
        salida.update(fila["metricas"])
        filas_csv.append(salida)
    ruta_totales = args.salida / "totales.csv"
    escribir_csv(ruta_totales, columnas, filas_csv)
    print(f"[csv] {ruta_totales} ({len(filas_csv)} filas)")

    # Agregados por cada eje solicitado.
    for eje in ejes_unicos:
        agregados = agregar(filas, eje)
        campos = ["grupo", "n_registros", "n_archivos", "n_benchmarks", "n_tamanos"]
        campos += [m for m in METRICAS_ADITIVAS if any(m in f for f in agregados)]
        campos += [
            "oi_isa",
            "oi_isa_vector",
            "flops_por_elemento",
            "bytes_por_elemento",
            "masked_fraccion",
            "sv_eventos_por_1k_vec",
            "mov_fraccion",
            "mov_bytes_vrf_por_op_aritmetica",
            "tu_fraccion",
            "mu_fraccion",
            "presion_preservacion",
            "presion_tail",
            "presion_mask",
            "mem_unit_fraccion",
            "mem_strided_fraccion",
            "mem_indexed_fraccion",
            "mem_irregular_fraccion",
            "permutaciones_por_1k_vec",
            "config_por_1k_vec",
            "loadstore_por_1k_vec",
            "vsetvl_por_1k_vec",
        ]
        campos += [f"media_{m}" for m in (
            "ocupacion_media",
            "vl_medio",
            "vlmax_medio",
            "lmul_medio",
            "registros_vectoriales_unicos",
            "dep_raw_dist_media",
            "dep_waw_dist_media",
            "dep_war_dist_media",
            "raw_fraccion_le4",
            "war_fraccion_le8",
            "waw_fraccion_le8",
            "masked_densidad_media",
        )]
        ruta = args.salida / f"agregados_por_{eje}.csv"
        escribir_csv(ruta, campos, agregados)
        print(f"[csv] {ruta} ({len(agregados)} grupos)")

    # Estadisticas por cada eje solicitado.
    for eje in ejes_unicos:
        est = generar_estadisticas(filas, eje, metricas_disponibles)
        ruta = args.salida / f"estadisticas_por_{eje}.csv"
        escribir_csv(
            ruta,
            ["metrica", "grupo", "n", "media", "desviacion", "minimo", "q1",
             "mediana", "q3", "maximo", "iqr", "p10", "p90"],
            est,
        )
        print(f"[csv] {ruta} ({len(est)} filas)")

    generados: list[str] = []
    omitidos: list[dict] = []
    if not args.sin_graficas:
        generados, omitidos = generar_boxplots(
            filas,
            args.salida,
            ejes,
            metricas_graficar,
            args.min_muestras,
            args.dpi,
            args.formato,
            not args.sin_puntos,
        )
        if omitidos:
            print(f"Aviso: {len(omitidos)} graficas omitidas (sin datos suficientes).")
            for item in omitidos[:8]:
                print(f"  - {item['metrica']} / {item['eje']}: {item['motivo']}")
            if len(omitidos) > 8:
                print(f"  ... y {len(omitidos) - 8} mas")

    resumen = {
        "resultados": str(args.resultados.resolve()),
        "salida": str(args.salida.resolve()),
        "archivos_json": len({f["archivo"] for f in filas}),
        "filas": len(filas),
        "errores": errores,
        "avisos": avisos,
        "tamanos": sorted({f["tamano"] for f in filas}),
        "conjuntos": sorted({f["conjunto"] for f in filas}),
        "familias": sorted({f["familia"] for f in filas}),
        "carpetas": sorted({f["carpeta"] for f in filas}),
        "benchmarks": sorted({f["benchmark"] for f in filas}),
        "metricas": metricas_disponibles,
        "metricas_graficadas": metricas_graficar,
        "ejes_solicitados": ejes_solicitados,
        "modo_auto": modo_auto,
        "ejes": ejes,
        "min_muestras": args.min_muestras,
        "graficas_generadas": generados,
        "graficas_omitidas": omitidos,
    }
    ruta_resumen = args.salida / "resumen.json"
    ruta_resumen.write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[json] {ruta_resumen}")
    print(
        f"Listo: {len(filas)} filas, {len({f['benchmark'] for f in filas})} benchmarks, "
        f"{len(generados)} graficas."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
