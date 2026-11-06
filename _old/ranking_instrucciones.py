#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ranking de instrucciones RVV a partir de los JSON de RAVE.

Genera, para el punto 2 de docs/tareas actuales.md:
  * prevalencia por aplicacion (una aplicacion cuenta una sola vez, aunque
    tenga varios tamanos o ejecuciones);
  * importancia dinamica normalizada por aplicacion;
  * media, mediana, cuartiles y percentiles de esa frecuencia;
  * rankings separados por seccion (configuracion/vset*, memoria, aritmetica
    entera, aritmetica FP, permutacion, reduccion y mascaras);
  * ranking por instruccion exacta y por familia funcional;
  * evolucion con el tamano del problema para RiVEC;
  * heatmap de presencia por aplicacion.

Los datos se leen de ../resultados. Las figuras y CSV se escriben en
salida_ranking/.
"""

from __future__ import annotations

import argparse
import csv
import fnmatch
import json
import math
import os
import re
import statistics
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

BASE = Path(__file__).resolve().parent
LIBS = BASE / "python_libs"
if LIBS.is_dir():
    sys.path.insert(0, str(LIBS))

os.environ.setdefault("MPLCONFIGDIR", str(BASE / ".matplotlib"))
os.environ.setdefault("MPLBACKEND", "Agg")

try:
    import numpy as np
except Exception as exc:  # pragma: no cover
    np = None
    _NUMPY_ERROR = exc

TAMANOS = ("tiny", "small", "medium", "large")

SECCIONES: dict[str, tuple[str, str]] = {
    "configuration_setting": ("Configuración (vset*)", "#4C72B0"),
    "vector_loads_and_stores": ("Memoria", "#DD8452"),
    "vector_integer_arithmetic": ("Aritmética entera", "#55A868"),
    "vector_floating_point": ("Aritmética FP", "#C44E52"),
    "vector_permutation": ("Permutación", "#8172B3"),
    "vector_reduction": ("Reducción", "#937860"),
    "vector_mask": ("Máscaras", "#DA8BC3"),
}
ORDEN_SECCIONES = tuple(SECCIONES)
ORDEN_CONJUNTOS = ("rivec", "apps_bench", "assembly_microbench", "proxy_bench")


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------

def numero(valor: Any) -> float | None:
    if valor is None or isinstance(valor, bool):
        return None
    if isinstance(valor, (int, float)):
        v = float(valor)
        return v if math.isfinite(v) else None
    return None


def media(valores: Iterable[float]) -> float:
    vals = list(valores)
    return statistics.fmean(vals) if vals else 0.0


def mediana(valores: Iterable[float]) -> float:
    vals = list(valores)
    return statistics.median(vals) if vals else 0.0


def percentil(valores: Iterable[float], p: float) -> float:
    vals = sorted(valores)
    if not vals:
        return 0.0
    if len(vals) == 1:
        return vals[0]
    if np is not None:
        return float(np.percentile(vals, p, method="linear"))
    k = (len(vals) - 1) * p / 100.0
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return vals[int(k)]
    return vals[f] * (c - k) + vals[c] * (k - f)


def etiqueta_seccion(seccion: str) -> str:
    return SECCIONES.get(seccion, (seccion.replace("_", " "), "#999999"))[0]


def color_seccion(seccion: str) -> str:
    return SECCIONES.get(seccion, (seccion, "#999999"))[1]


def etiqueta_familia(familia: str) -> str:
    return familia.replace("_", " ")


def nombre_instruccion(hoja: str) -> str:
    if hoja.endswith("_counter"):
        hoja = hoja[: -len("_counter")]
    return hoja.replace("_", ".")


def orden_conjunto(conjunto: str) -> tuple:
    try:
        return (ORDEN_CONJUNTOS.index(conjunto), conjunto)
    except ValueError:
        return (len(ORDEN_CONJUNTOS), conjunto)


def slug(texto: str) -> str:
    texto = texto.replace("/", "_").replace(" ", "_")
    return re.sub(r"[^A-Za-z0-9_.-]", "_", texto)


# ---------------------------------------------------------------------------
# Lectura de resultados
# ---------------------------------------------------------------------------

@dataclass
class Config:
    archivo: str
    conjunto: str
    tamano: str
    familia: str
    benchmark: str
    run: str
    aplicacion: str
    configuracion: str
    counts: dict[tuple[str, str, str], float]
    total: float = 0.0
    seccion_total: dict[str, float] = field(default_factory=dict)
    familia_counts: dict[tuple[str, str], float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.total = math.fsum(self.counts.values())
        seccion: dict[str, float] = defaultdict(float)
        familias: dict[tuple[str, str], float] = defaultdict(float)
        for (sec, fam, _inst), cuenta in self.counts.items():
            seccion[sec] += cuenta
            familias[(sec, fam)] += cuenta
        self.seccion_total = dict(seccion)
        self.familia_counts = dict(familias)


@dataclass
class AppStats:
    aplicacion: str
    conjunto: str
    familia: str
    configs: list[Config]
    inst_global: dict[tuple[str, str, str], float] = field(default_factory=dict)
    inst_section: dict[tuple[str, str, str], float] = field(default_factory=dict)
    inst_present: dict[tuple[str, str, str], bool] = field(default_factory=dict)
    fam_global: dict[tuple[str, str], float] = field(default_factory=dict)
    fam_section: dict[tuple[str, str], float] = field(default_factory=dict)
    fam_present: dict[tuple[str, str], bool] = field(default_factory=dict)
    tiene_datos: bool = False


def recorrer_arbol(
    nodo: Any,
    ruta: list[str],
    salida: dict[tuple[str, str, str], float],
) -> None:
    """Recorre el arbol de categorias y acumula las hojas numericas."""
    if isinstance(nodo, dict):
        for clave, valor in nodo.items():
            recorrer_arbol(valor, ruta + [str(clave)], salida)
        return
    valor = numero(nodo)
    if valor is None or not ruta:
        return
    seccion = ruta[0]
    familia = ruta[-2] if len(ruta) >= 2 else seccion
    instruccion = nombre_instruccion(ruta[-1])
    if not instruccion:
        return
    salida[(seccion, familia, instruccion)] += valor


def metadatos(ruta: Path, raiz: Path) -> dict[str, str]:
    rel = ruta.relative_to(raiz)
    partes = rel.parts[:-1]
    if partes and partes[0].lower() in TAMANOS:
        return {"conjunto": "rivec", "tamano": partes[0].lower(), "familia": "rivec"}
    if partes:
        conjunto = partes[0]
        tamano = next((p.lower() for p in partes if p.lower() in TAMANOS), "no_aplica")
        familia = partes[1] if len(partes) >= 2 else conjunto
        return {"conjunto": conjunto, "tamano": tamano, "familia": familia}
    if raiz.name.lower() in TAMANOS:
        return {"conjunto": "rivec", "tamano": raiz.name.lower(), "familia": "rivec"}
    conjunto = raiz.name or "resultados"
    return {"conjunto": conjunto, "tamano": "no_aplica", "familia": conjunto}


def aplicacion_y_configuracion(meta: dict[str, str], benchmark: str, run: str) -> tuple[str, str]:
    conjunto = meta["conjunto"]
    familia = meta["familia"]
    if conjunto == "proxy_bench":
        base = re.sub(r"_\d+$", "", benchmark)
        aplicacion = f"proxy_bench/{familia}/{base}"
        configuracion = f"{aplicacion} [{run}]"
    elif conjunto == "rivec":
        aplicacion = f"rivec/{benchmark}"
        configuracion = f"{aplicacion} [{meta['tamano']}]"
        if run != benchmark:
            configuracion += f" {run}"
    else:
        aplicacion = f"{conjunto}/{familia}/{benchmark}"
        configuracion = f"{aplicacion} [{run}]"
    return aplicacion, configuracion


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


def cargar_configuraciones(
    raiz: Path,
    tamanos: list[str] | None,
    conjuntos: list[str] | None,
    familias: list[str] | None,
    benchmarks: list[str] | None,
) -> tuple[list[Config], list[dict], list[str]]:
    configs: list[Config] = []
    errores: list[dict] = []
    avisos: list[str] = []

    if not raiz.is_dir():
        raise SystemExit(f"No existe el directorio de resultados: {raiz}")

    archivos = sorted(p for p in raiz.rglob("*.json") if p.is_file())
    if not archivos:
        raise SystemExit(f"No hay ficheros .json en {raiz}")

    for ruta in archivos:
        meta = metadatos(ruta, raiz)
        if tamanos and meta["tamano"] not in tamanos:
            continue
        if conjuntos and meta["conjunto"] not in conjuntos:
            continue
        if familias and meta["familia"] not in familias:
            continue
        benchmark = ruta.stem
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

        counts: dict[tuple[str, str, str], float] = defaultdict(float)
        regiones = doc.get("regions") or []
        for region in regiones:
            if isinstance(region, dict):
                recorrer_arbol(region.get("instructions") or {}, [], counts)
        if not counts:
            avisos.append(f"{ruta.relative_to(raiz)}: sin contadores de instrucciones")

        aplicacion, configuracion = aplicacion_y_configuracion(meta, benchmark, benchmark)
        configs.append(
            Config(
                archivo=ruta.relative_to(raiz).as_posix(),
                conjunto=meta["conjunto"],
                tamano=meta["tamano"],
                familia=meta["familia"],
                benchmark=benchmark,
                run=benchmark,
                aplicacion=aplicacion,
                configuracion=configuracion,
                counts=dict(counts),
            )
        )
    return configs, errores, avisos


# ---------------------------------------------------------------------------
# Estadisticas por aplicacion
# ---------------------------------------------------------------------------

def construir_apps(
    configs: list[Config],
) -> tuple[dict[str, AppStats], list[tuple[str, str, str]], list[tuple[str, str]]]:
    por_app: dict[str, list[Config]] = defaultdict(list)
    for cfg in configs:
        por_app[cfg.aplicacion].append(cfg)

    inst_keys: set[tuple[str, str, str]] = set()
    fam_keys: set[tuple[str, str]] = set()
    for cfg in configs:
        inst_keys.update(cfg.counts.keys())
        fam_keys.update(cfg.familia_counts.keys())

    apps: dict[str, AppStats] = {}
    for aplicacion, cfgs in por_app.items():
        primero = cfgs[0]
        stats = AppStats(
            aplicacion=aplicacion,
            conjunto=primero.conjunto,
            familia=primero.familia,
            configs=cfgs,
            tiene_datos=any(c.total > 0 for c in cfgs),
        )
        for key in inst_keys:
            sec = key[0]
            vals_g: list[float] = []
            vals_s: list[float] = []
            presente = False
            for cfg in cfgs:
                cuenta = cfg.counts.get(key, 0.0)
                if cuenta > 0:
                    presente = True
                if cfg.total > 0:
                    vals_g.append(cuenta / cfg.total)
                sec_total = cfg.seccion_total.get(sec, 0.0)
                if sec_total > 0:
                    vals_s.append(cuenta / sec_total)
            stats.inst_global[key] = media(vals_g)
            stats.inst_section[key] = media(vals_s)
            stats.inst_present[key] = presente

        for key in fam_keys:
            sec = key[0]
            vals_g = []
            vals_s = []
            presente = False
            for cfg in cfgs:
                cuenta = cfg.familia_counts.get(key, 0.0)
                if cuenta > 0:
                    presente = True
                if cfg.total > 0:
                    vals_g.append(cuenta / cfg.total)
                sec_total = cfg.seccion_total.get(sec, 0.0)
                if sec_total > 0:
                    vals_s.append(cuenta / sec_total)
            stats.fam_global[key] = media(vals_g)
            stats.fam_section[key] = media(vals_s)
            stats.fam_present[key] = presente
        apps[aplicacion] = stats

    return apps, sorted(inst_keys), sorted(fam_keys)


def resumir_ranking(
    tipo: str,
    keys: Iterable[tuple],
    apps: dict[str, AppStats],
    apps_ordenadas: list[str],
    configs: list[Config],
    total_global: float,
    totales_seccion: dict[str, float],
) -> list[dict]:
    filas: list[dict] = []
    n_apps = len(apps_ordenadas)
    n_configs = len(configs)

    for key in keys:
        seccion = key[0]
        if tipo == "instruccion":
            familia = key[1]
            nombre = key[2]
            clave = f"{seccion}/{familia}/{nombre}"
            get_g = lambda s: s.inst_global.get(key, 0.0)  # noqa: E731
            get_s = lambda s: s.inst_section.get(key, 0.0)  # noqa: E731
            get_p = lambda s: s.inst_present.get(key, False)  # noqa: E731
            get_count = lambda c: c.counts.get(key, 0.0)  # noqa: E731
        else:
            familia = key[1]
            nombre = etiqueta_familia(familia)
            clave = f"{seccion}/{familia}"
            get_g = lambda s: s.fam_global.get(key, 0.0)  # noqa: E731
            get_s = lambda s: s.fam_section.get(key, 0.0)  # noqa: E731
            get_p = lambda s: s.fam_present.get(key, False)  # noqa: E731
            get_count = lambda c: c.familia_counts.get(key, 0.0)  # noqa: E731

        valores = [get_g(apps[a]) for a in apps_ordenadas]
        valores_sec = [get_s(apps[a]) for a in apps_ordenadas]
        presentes = [get_p(apps[a]) for a in apps_ordenadas]
        con_datos = [apps[a].tiene_datos for a in apps_ordenadas]

        n_datos = sum(con_datos)
        n_presentes = sum(presentes)
        vals_datos = [v for v, d in zip(valores, con_datos) if d]
        vals_sec_datos = [v for v, d in zip(valores_sec, con_datos) if d]
        vals_presentes = [
            v for v, p, d in zip(valores, presentes, con_datos) if p and d
        ]

        n_configs_presentes = sum(1 for c in configs if get_count(c) > 0)
        cuenta_total = math.fsum(get_count(c) for c in configs)

        filas.append(
            {
                "tipo": tipo,
                "seccion": seccion,
                "familia": familia,
                "nombre": nombre,
                "clave": clave,
                "_key": key,
                "n_aplicaciones": n_apps,
                "n_aplicaciones_con_datos": n_datos,
                "n_aplicaciones_presentes": n_presentes,
                "prevalencia_pct": 100.0 * n_presentes / n_apps if n_apps else 0.0,
                "prevalencia_datos_pct": 100.0 * n_presentes / n_datos if n_datos else 0.0,
                "n_configuraciones": n_configs,
                "n_configuraciones_presentes": n_configs_presentes,
                "prevalencia_config_pct": 100.0 * n_configs_presentes / n_configs if n_configs else 0.0,
                "frecuencia_media_pct": 100.0 * media(vals_datos),
                "frecuencia_mediana_pct": 100.0 * mediana(vals_datos),
                "frecuencia_mediana_presentes_pct": 100.0 * mediana(vals_presentes),
                "q25_pct": 100.0 * percentil(vals_datos, 25.0),
                "q75_pct": 100.0 * percentil(vals_datos, 75.0),
                "p90_pct": 100.0 * percentil(vals_datos, 90.0),
                "frecuencia_seccion_media_pct": 100.0 * media(vals_sec_datos),
                "frecuencia_seccion_mediana_pct": 100.0 * mediana(vals_sec_datos),
                "participacion_global_pct": 100.0 * cuenta_total / total_global if total_global else 0.0,
                "participacion_seccion_pct": (
                    100.0 * cuenta_total / totales_seccion.get(seccion, 0.0)
                    if totales_seccion.get(seccion, 0.0)
                    else 0.0
                ),
                "cuenta_total": cuenta_total,
            }
        )
    return filas


def calcular_evolucion(
    tipo: str,
    keys: Iterable[tuple],
    apps: dict[str, AppStats],
    configs: list[Config],
) -> list[dict]:
    rivec = [c for c in configs if c.conjunto == "rivec" and c.tamano in TAMANOS]
    if not rivec:
        return []
    por_app_tamano: dict[tuple[str, str], list[Config]] = defaultdict(list)
    for cfg in rivec:
        por_app_tamano[(cfg.aplicacion, cfg.tamano)].append(cfg)
    apps_por_tamano: dict[str, set[str]] = defaultdict(set)
    for (app, tamano) in por_app_tamano:
        apps_por_tamano[tamano].add(app)
    tamanos = [t for t in TAMANOS if apps_por_tamano.get(t)]

    filas: list[dict] = []
    for key in keys:
        seccion = key[0]
        if tipo == "instruccion":
            familia = key[1]
            nombre = key[2]
            clave = f"{seccion}/{familia}/{nombre}"
            campo = "counts"
        else:
            familia = key[1]
            nombre = etiqueta_familia(familia)
            clave = f"{seccion}/{familia}"
            campo = "familia_counts"

        for tamano in tamanos:
            valores: list[float] = []
            presentes: list[bool] = []
            for app in sorted(apps_por_tamano[tamano]):
                cfgs = por_app_tamano[(app, tamano)]
                validos = [c for c in cfgs if c.total > 0]
                if campo == "counts":
                    cuentas = [c.counts.get(key, 0.0) for c in validos]
                    seccion_totales = [c.seccion_total.get(seccion, 0.0) for c in validos]
                else:
                    cuentas = [c.familia_counts.get(key, 0.0) for c in validos]
                    seccion_totales = [c.seccion_total.get(seccion, 0.0) for c in validos]
                freq = media(
                    cuenta / c.total
                    for cuenta, c in zip(cuentas, validos)
                    if c.total > 0
                )
                valores.append(freq)
                presentes.append(any(cuenta > 0 for cuenta in cuentas))
            n_apps = len(valores)
            n_presentes = sum(presentes)
            filas.append(
                {
                    "tipo": tipo,
                    "seccion": seccion,
                    "familia": familia,
                    "nombre": nombre,
                    "clave": clave,
                    "_key": key,
                    "tamano": tamano,
                    "n_aplicaciones": n_apps,
                    "n_aplicaciones_presentes": n_presentes,
                    "prevalencia_pct": 100.0 * n_presentes / n_apps if n_apps else 0.0,
                    "frecuencia_media_pct": 100.0 * media(valores),
                    "frecuencia_mediana_pct": 100.0 * mediana(valores),
                }
            )
    return filas


# ---------------------------------------------------------------------------
# CSV
# ---------------------------------------------------------------------------

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
                elif isinstance(valor, float):
                    if campo.endswith("_pct"):
                        salida[campo] = f"{valor:.4f}"
                    else:
                        salida[campo] = f"{valor:.6g}"
                else:
                    salida[campo] = valor
            writer.writerow(salida)


CAMPOS_RANKING = [
    "tipo", "seccion", "familia", "nombre", "clave",
    "n_aplicaciones", "n_aplicaciones_con_datos", "n_aplicaciones_presentes",
    "prevalencia_pct", "prevalencia_datos_pct",
    "n_configuraciones", "n_configuraciones_presentes", "prevalencia_config_pct",
    "frecuencia_media_pct", "frecuencia_mediana_pct",
    "frecuencia_mediana_presentes_pct",
    "q25_pct", "q75_pct", "p90_pct",
    "frecuencia_seccion_media_pct", "frecuencia_seccion_mediana_pct",
    "participacion_global_pct", "participacion_seccion_pct", "cuenta_total",
]

CAMPOS_EVOLUCION = [
    "tipo", "seccion", "familia", "nombre", "clave", "tamano",
    "n_aplicaciones", "n_aplicaciones_presentes",
    "prevalencia_pct", "frecuencia_media_pct", "frecuencia_mediana_pct",
]

CAMPOS_POR_APLICACION = [
    "aplicacion", "conjunto", "familia", "configuraciones",
    "seccion", "familia_categoria", "instruccion",
    "cuenta_total", "frecuencia_global_pct", "frecuencia_seccion_pct", "presente",
]


# ---------------------------------------------------------------------------
# Figuras
# ---------------------------------------------------------------------------

def _importar_matplotlib():
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        from matplotlib.patches import Patch
    except Exception as exc:
        return None, None, None, exc
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
    return plt, Patch, matplotlib, None


def _guardar(fig, plt, ruta: Path, dpi: int) -> None:
    ruta.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(ruta, dpi=dpi, bbox_inches="tight")
    plt.close(fig)


def _leyenda_secciones(ax, filas: list[dict], Patch) -> None:
    secciones = []
    for fila in filas:
        if fila["seccion"] not in secciones:
            secciones.append(fila["seccion"])
    handles = [
        Patch(facecolor=color_seccion(sec), edgecolor="#333333", label=etiqueta_seccion(sec))
        for sec in secciones
    ]
    if handles:
        ax.legend(
            handles=handles,
            loc="lower right",
            fontsize=7,
            framealpha=0.9,
            ncol=1 if len(handles) <= 5 else 2,
        )


def figura_barras(
    filas: list[dict],
    valor: str,
    titulo: str,
    xlabel: str,
    ruta: Path,
    top: int,
    dpi: int,
    plt,
    Patch,
    error_inf: str | None = None,
    error_sup: str | None = None,
    mediana: str | None = None,
    xlim: float | None = None,
) -> None:
    seleccion = filas[:top][::-1]
    if not seleccion:
        return
    nombres = [f["nombre"] for f in seleccion]
    valores = [f[valor] for f in seleccion]
    colores = [color_seccion(f["seccion"]) for f in seleccion]

    fig, ax = plt.subplots(figsize=(10.5, max(4.5, 0.34 * len(seleccion) + 1.7)))
    barras = ax.barh(nombres, valores, color=colores, edgecolor="#333333", linewidth=0.6)

    if error_inf and error_sup:
        xerr = [
            [max(0.0, f[valor] - f[error_inf]) for f in seleccion],
            [max(0.0, f[error_sup] - f[valor]) for f in seleccion],
        ]
        ax.errorbar(
            valores,
            range(len(seleccion)),
            xerr=xerr,
            fmt="none",
            ecolor="#333333",
            elinewidth=0.8,
            capsize=2,
            alpha=0.8,
        )
    if mediana:
        ax.scatter(
            [f[mediana] for f in seleccion],
            range(len(seleccion)),
            marker="|",
            s=70,
            color="black",
            zorder=3,
            label="mediana",
        )

    maximos = list(valores)
    if error_sup:
        maximos.extend(f[error_sup] for f in seleccion)
    maximo = max(maximos) if maximos else 0.0
    limite = xlim if xlim is not None else max(1.0, maximo * 1.18)
    for i, (barra, valor_fila) in enumerate(zip(barras, valores)):
        ax.text(
            min(valor_fila + limite * 0.012, limite * 0.985),
            i,
            f"{valor_fila:.1f}%",
            va="center",
            ha="left" if valor_fila < limite * 0.85 else "right",
            fontsize=7,
            color="#111111",
        )
    ax.set_xlim(0.0, limite)
    ax.set_xlabel(xlabel)
    ax.set_title(titulo)
    ax.grid(axis="x", alpha=0.25)
    ax.set_axisbelow(True)
    _leyenda_secciones(ax, seleccion, Patch)
    fig.tight_layout()
    _guardar(fig, plt, ruta, dpi)


def figura_paneles_seccion(
    filas: list[dict],
    valor: str,
    titulo: str,
    xlabel: str,
    ruta: Path,
    top_seccion: int,
    dpi: int,
    plt,
) -> None:
    secciones = [s for s in ORDEN_SECCIONES if any(f["seccion"] == s for f in filas)]
    secciones += sorted(
        {f["seccion"] for f in filas} - set(secciones)
    )
    if not secciones:
        return
    ncols = 2
    nrows = math.ceil(len(secciones) / ncols)
    fig, axes = plt.subplots(
        nrows,
        ncols,
        figsize=(14.0, max(5.0, nrows * 3.5)),
        squeeze=False,
    )
    for idx, seccion in enumerate(secciones):
        ax = axes[idx // ncols][idx % ncols]
        sub = [f for f in filas if f["seccion"] == seccion]
        sub.sort(key=lambda f: (-f[valor], -f["prevalencia_pct"], f["nombre"]))
        sub = sub[:top_seccion][::-1]
        if not sub:
            ax.axis("off")
            continue
        nombres = [f["nombre"] for f in sub]
        valores = [f[valor] for f in sub]
        ax.barh(nombres, valores, color=color_seccion(seccion), edgecolor="#333333", linewidth=0.5)
        maximo = max(valores) if valores else 0.0
        limite = max(1.0, maximo * 1.25)
        for i, valor_fila in enumerate(valores):
            ax.text(
                min(valor_fila + limite * 0.015, limite * 0.98),
                i,
                f"{valor_fila:.1f}%",
                va="center",
                fontsize=6.5,
            )
        ax.set_xlim(0.0, limite)
        ax.set_title(etiqueta_seccion(seccion), fontsize=9)
        ax.set_xlabel(xlabel, fontsize=7)
        ax.grid(axis="x", alpha=0.25)
        ax.set_axisbelow(True)
        ax.tick_params(axis="y", labelsize=7)
    for idx in range(len(secciones), nrows * ncols):
        axes[idx // ncols][idx % ncols].axis("off")
    fig.suptitle(titulo)
    fig.tight_layout()
    _guardar(fig, plt, ruta, dpi)


def figura_boxplot(
    filas: list[dict],
    apps: dict[str, AppStats],
    apps_ordenadas: list[str],
    ruta: Path,
    top: int,
    dpi: int,
    plt,
) -> None:
    seleccion = filas[:top][::-1]
    if not seleccion:
        return
    datos: list[list[float]] = []
    etiquetas: list[str] = []
    colores: list[str] = []
    for fila in seleccion:
        key = fila["_key"]
        if fila["tipo"] == "instruccion":
            valores = [100.0 * apps[a].inst_global.get(key, 0.0) for a in apps_ordenadas]
        else:
            valores = [100.0 * apps[a].fam_global.get(key, 0.0) for a in apps_ordenadas]
        datos.append(valores)
        etiquetas.append(fila["nombre"])
        colores.append(color_seccion(fila["seccion"]))

    fig, ax = plt.subplots(figsize=(12.0, max(5.0, min(9.0, 0.25 * len(seleccion) + 3.5))))
    bp = ax.boxplot(
        datos,
        tick_labels=etiquetas,
        patch_artist=True,
        showmeans=True,
        medianprops={"color": "#111111", "linewidth": 1.4},
        meanprops={
            "marker": "D",
            "markerfacecolor": "white",
            "markeredgecolor": "#111111",
            "markersize": 3,
        },
        flierprops={"marker": "o", "markersize": 2, "markerfacecolor": "none"},
    )
    for caja, color in zip(bp["boxes"], colores):
        caja.set_facecolor(color)
        caja.set_alpha(0.75)
        caja.set_edgecolor("#333333")
    ax.set_ylabel("Frecuencia por aplicación [%]")
    ax.set_title(
        f"Distribución de la frecuencia por aplicación (top {len(seleccion)})",
        fontsize=10,
    )
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    ax.tick_params(axis="x", rotation=45, labelsize=7)
    for label in ax.get_xticklabels():
        label.set_horizontalalignment("right")
    fig.tight_layout()
    _guardar(fig, plt, ruta, dpi)


def figura_heatmap(
    filas: list[dict],
    apps: dict[str, AppStats],
    apps_ordenadas: list[str],
    ruta: Path,
    top: int,
    dpi: int,
    plt,
) -> None:
    seleccion = filas[:top]
    if not seleccion or not apps_ordenadas:
        return
    matriz: list[list[int]] = []
    for fila in seleccion:
        key = fila["_key"]
        if fila["tipo"] == "instruccion":
            matriz.append([1 if apps[a].inst_present.get(key, False) else 0 for a in apps_ordenadas])
        else:
            matriz.append([1 if apps[a].fam_present.get(key, False) else 0 for a in apps_ordenadas])

    ordenadas = sorted(
        apps_ordenadas,
        key=lambda a: (orden_conjunto(apps[a].conjunto), apps[a].familia, a),
    )
    # Reordenar columnas de la matriz.
    indice = {a: i for i, a in enumerate(apps_ordenadas)}
    matriz = [[fila[indice[a]] for a in ordenadas] for fila in matriz]

    grupos: list[tuple[int, int, str]] = []
    inicio = 0
    for i in range(1, len(ordenadas) + 1):
        if i == len(ordenadas) or (apps[ordenadas[i]].conjunto, apps[ordenadas[i]].familia) != (
            apps[ordenadas[inicio]].conjunto,
            apps[ordenadas[inicio]].familia,
        ):
            grupos.append((inicio, i, f"{apps[ordenadas[inicio]].conjunto}/{apps[ordenadas[inicio]].familia}"))
            inicio = i

    ancho = min(30.0, max(10.0, len(ordenadas) * 0.085))
    alto = max(5.0, 0.34 * len(seleccion) + 2.0)
    fig, ax = plt.subplots(figsize=(ancho, alto))
    im = ax.imshow(matriz, aspect="auto", interpolation="nearest", cmap="Blues", vmin=0, vmax=1)
    ax.set_yticks(range(len(seleccion)))
    ax.set_yticklabels([f["nombre"] for f in seleccion], fontsize=7)
    centros = [(a + b) / 2.0 for a, b, _ in grupos]
    etiquetas = [g[2] for g in grupos]
    ax.set_xticks(centros)
    ax.set_xticklabels(etiquetas, rotation=45, ha="right", fontsize=7)
    for a, b, _ in grupos[1:]:
        ax.axvline(b - 0.5, color="#333333", linewidth=0.8, alpha=0.7)
    ax.set_title(f"Presencia por aplicación (top {len(seleccion)} instrucciones)", fontsize=10)
    ax.set_xlabel("Aplicaciones agrupadas por conjunto/familia")
    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02, ticks=[0, 1])
    cbar.ax.set_yticklabels(["ausente", "presente"])
    fig.tight_layout()
    _guardar(fig, plt, ruta, dpi)


def figura_evolucion(
    filas: list[dict],
    valor: str,
    titulo: str,
    ylabel: str,
    ruta: Path,
    top: int,
    dpi: int,
    plt,
    ylim: tuple[float, float] | None = None,
) -> None:
    if not filas:
        return
    por_clave: dict[str, dict] = {}
    for fila in filas:
        item = por_clave.setdefault(
            fila["clave"],
            {
                "nombre": fila["nombre"],
                "seccion": fila["seccion"],
                "valores": {},
            },
        )
        item["valores"][fila["tamano"]] = fila[valor]
    tamanos = [t for t in TAMANOS if any(t in item["valores"] for item in por_clave.values())]
    if not tamanos:
        return

    def media_por_clave(item: dict) -> float:
        vals = [item["valores"].get(t, 0.0) for t in tamanos]
        return media(vals)

    claves = sorted(por_clave, key=lambda k: -media_por_clave(por_clave[k]))[:top]
    fig, ax = plt.subplots(figsize=(10.5, 6.0))
    for clave in claves:
        item = por_clave[clave]
        valores = [item["valores"].get(t, 0.0) for t in tamanos]
        ax.plot(
            range(len(tamanos)),
            valores,
            marker="o",
            linewidth=1.6,
            markersize=4,
            label=item["nombre"],
            color=color_seccion(item["seccion"]),
        )
    ax.set_xticks(range(len(tamanos)))
    ax.set_xticklabels(tamanos)
    ax.set_xlabel("Tamaño del problema")
    ax.set_ylabel(ylabel)
    ax.set_title(titulo)
    if ylim:
        ax.set_ylim(*ylim)
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    ax.legend(fontsize=7, loc="upper left", bbox_to_anchor=(1.01, 1.0), framealpha=0.9)
    fig.tight_layout()
    _guardar(fig, plt, ruta, dpi)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parsear_lista(valor: str | None) -> list[str] | None:
    if not valor:
        return None
    return [x.strip() for x in valor.split(",") if x.strip()]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Rankings de instrucciones RVV: prevalencia, frecuencia, familias y evolución.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--resultados",
        type=Path,
        default=BASE.parent / "resultados",
        help="Directorio raíz de los JSON de resultados.",
    )
    parser.add_argument(
        "--salida",
        type=Path,
        default=BASE / "salida_ranking",
        help="Directorio de salida para CSV y figuras.",
    )
    parser.add_argument("--top", type=int, default=20, help="Número de elementos en los rankings globales.")
    parser.add_argument(
        "--top-seccion",
        type=int,
        default=8,
        help="Número de elementos por sección en los paneles.",
    )
    parser.add_argument("--formato", choices=("png", "svg", "pdf"), default="png")
    parser.add_argument("--dpi", type=int, default=150)
    parser.add_argument("--sin-graficas", action="store_true", help="Solo generar CSV y resumen.")
    parser.add_argument("--conjunto", action="append", help="Filtrar por conjunto.")
    parser.add_argument("--familia", action="append", help="Filtrar por familia.")
    parser.add_argument("--tamano", action="append", help="Filtrar por tamaño.")
    parser.add_argument("--benchmark", action="append", help="Filtrar por benchmark o patrón glob.")
    parser.add_argument(
        "--listar-secciones",
        action="store_true",
        help="Muestra las secciones detectadas y termina.",
    )
    args = parser.parse_args()

    if args.top < 1 or args.top_seccion < 1:
        parser.error("--top y --top-seccion deben ser >= 1")

    print(f"Resultados: {args.resultados}")
    configs, errores, avisos = cargar_configuraciones(
        args.resultados,
        parsear_lista(",".join(args.tamano)) if args.tamano else None,
        parsear_lista(",".join(args.conjunto)) if args.conjunto else None,
        parsear_lista(",".join(args.familia)) if args.familia else None,
        args.benchmark,
    )
    if not configs:
        print("No se han encontrado resultados válidos.", file=sys.stderr)
        for error in errores:
            print(f"  ERROR {error['archivo']}: {error['error']}", file=sys.stderr)
        return 1

    apps, inst_keys, fam_keys = construir_apps(configs)
    apps_ordenadas = sorted(
        apps,
        key=lambda a: (orden_conjunto(apps[a].conjunto), apps[a].familia, a),
    )
    if not inst_keys:
        print("No hay contadores de instrucciones en los resultados.", file=sys.stderr)
        return 1

    secciones = sorted({k[0] for k in inst_keys}, key=lambda s: (
        ORDEN_SECCIONES.index(s) if s in ORDEN_SECCIONES else len(ORDEN_SECCIONES),
        s,
    ))
    if args.listar_secciones:
        for seccion in secciones:
            print(f"{seccion:34s} {etiqueta_seccion(seccion)}")
        return 0

    total_global = math.fsum(c.total for c in configs)
    totales_seccion: dict[str, float] = defaultdict(float)
    for cfg in configs:
        for seccion, total in cfg.seccion_total.items():
            totales_seccion[seccion] += total

    filas_inst = resumir_ranking(
        "instruccion", inst_keys, apps, apps_ordenadas, configs, total_global, totales_seccion
    )
    filas_fam = resumir_ranking(
        "familia", fam_keys, apps, apps_ordenadas, configs, total_global, totales_seccion
    )

    ranking_inst_prevalencia = sorted(
        filas_inst,
        key=lambda f: (-f["prevalencia_pct"], -f["frecuencia_media_pct"], f["nombre"]),
    )
    ranking_inst_frecuencia = sorted(
        filas_inst,
        key=lambda f: (-f["frecuencia_media_pct"], -f["prevalencia_pct"], f["nombre"]),
    )
    ranking_fam_prevalencia = sorted(
        filas_fam,
        key=lambda f: (-f["prevalencia_pct"], -f["frecuencia_media_pct"], f["nombre"]),
    )
    ranking_fam_frecuencia = sorted(
        filas_fam,
        key=lambda f: (-f["frecuencia_media_pct"], -f["prevalencia_pct"], f["nombre"]),
    )

    def _sin_configuracion(filas: list[dict]) -> list[dict]:
        # vset* no debe competir con aritmetica/memoria en el ranking global;
        # la seccion de configuracion tiene su propio panel.
        filtradas = [f for f in filas if f["seccion"] != "configuration_setting"]
        return filtradas or filas

    ranking_inst_prevalencia_global = _sin_configuracion(ranking_inst_prevalencia)
    ranking_inst_frecuencia_global = _sin_configuracion(ranking_inst_frecuencia)
    ranking_fam_prevalencia_global = _sin_configuracion(ranking_fam_prevalencia)
    ranking_fam_frecuencia_global = _sin_configuracion(ranking_fam_frecuencia)

    evolucion_inst = calcular_evolucion("instruccion", inst_keys, apps, configs)
    evolucion_fam = calcular_evolucion("familia", fam_keys, apps, configs)
    evolucion_inst_global = [f for f in evolucion_inst if f["seccion"] != "configuration_setting"]
    evolucion_fam_global = [f for f in evolucion_fam if f["seccion"] != "configuration_setting"]

    args.salida.mkdir(parents=True, exist_ok=True)
    figuras = args.salida / "figuras"

    escribir_csv(
        args.salida / "ranking_prevalencia_instrucciones.csv",
        CAMPOS_RANKING,
        ranking_inst_prevalencia,
    )
    escribir_csv(
        args.salida / "ranking_frecuencia_instrucciones.csv",
        CAMPOS_RANKING,
        ranking_inst_frecuencia,
    )
    escribir_csv(
        args.salida / "ranking_prevalencia_familias.csv",
        CAMPOS_RANKING,
        ranking_fam_prevalencia,
    )
    escribir_csv(
        args.salida / "ranking_frecuencia_familias.csv",
        CAMPOS_RANKING,
        ranking_fam_frecuencia,
    )
    escribir_csv(
        args.salida / "evolucion_instrucciones.csv",
        CAMPOS_EVOLUCION,
        evolucion_inst,
    )
    escribir_csv(
        args.salida / "evolucion_familias.csv",
        CAMPOS_EVOLUCION,
        evolucion_fam,
    )

    filas_app: list[dict] = []
    for app in apps_ordenadas:
        stats = apps[app]
        configuraciones = len(stats.configs)
        for key in inst_keys:
            if not stats.inst_present.get(key, False):
                continue
            filas_app.append(
                {
                    "aplicacion": app,
                    "conjunto": stats.conjunto,
                    "familia": stats.familia,
                    "configuraciones": configuraciones,
                    "seccion": key[0],
                    "familia_categoria": key[1],
                    "instruccion": key[2],
                    "cuenta_total": math.fsum(c.counts.get(key, 0.0) for c in stats.configs),
                    "frecuencia_global_pct": 100.0 * stats.inst_global.get(key, 0.0),
                    "frecuencia_seccion_pct": 100.0 * stats.inst_section.get(key, 0.0),
                    "presente": 1,
                }
            )
    escribir_csv(
        args.salida / "instrucciones_por_aplicacion.csv",
        CAMPOS_POR_APLICACION,
        filas_app,
    )

    print(
        f"Aplicaciones: {len(apps)} ({sum(1 for a in apps.values() if a.tiene_datos)} con datos); "
        f"configuraciones: {len(configs)}; instrucciones: {len(inst_keys)}; familias: {len(fam_keys)}"
    )

    generadas: list[str] = []
    if not args.sin_graficas:
        plt, Patch, _mpl, error = _importar_matplotlib()
        if error is not None:
            print(f"Aviso: no se pueden generar figuras: {error}")
        else:
            figura_barras(
                ranking_inst_prevalencia_global,
                "prevalencia_pct",
                f"Prevalencia de instrucciones (top {args.top}; "
                f"{len(apps)} aplicaciones, "
                f"{sum(1 for a in apps.values() if a.tiene_datos)} con datos; "
                f"sin configuración)",
                "Aplicaciones donde aparece [%]",
                figuras / f"prevalencia_instrucciones.{args.formato}",
                args.top,
                args.dpi,
                plt,
                Patch,
                xlim=100.0,
            )
            generadas.append(f"prevalencia_instrucciones.{args.formato}")
            figura_barras(
                ranking_inst_frecuencia_global,
                "frecuencia_media_pct",
                f"Importancia dinámica normalizada por instrucción "
                f"(top {args.top}; sin configuración)",
                "Frecuencia media por aplicación [%]",
                figuras / f"frecuencia_instrucciones.{args.formato}",
                args.top,
                args.dpi,
                plt,
                Patch,
                error_inf="q25_pct",
                error_sup="q75_pct",
                mediana="frecuencia_mediana_pct",
            )
            generadas.append(f"frecuencia_instrucciones.{args.formato}")
            figura_barras(
                ranking_fam_prevalencia_global,
                "prevalencia_pct",
                f"Prevalencia de familias funcionales (top {args.top}; "
                f"{len(apps)} aplicaciones, "
                f"{sum(1 for a in apps.values() if a.tiene_datos)} con datos; "
                f"sin configuración)",
                "Aplicaciones donde aparece [%]",
                figuras / f"prevalencia_familias.{args.formato}",
                args.top,
                args.dpi,
                plt,
                Patch,
                xlim=100.0,
            )
            generadas.append(f"prevalencia_familias.{args.formato}")
            figura_barras(
                ranking_fam_frecuencia_global,
                "frecuencia_media_pct",
                f"Importancia dinámica normalizada por familia "
                f"(top {args.top}; sin configuración)",
                "Frecuencia media por aplicación [%]",
                figuras / f"frecuencia_familias.{args.formato}",
                args.top,
                args.dpi,
                plt,
                Patch,
                error_inf="q25_pct",
                error_sup="q75_pct",
                mediana="frecuencia_mediana_pct",
            )
            generadas.append(f"frecuencia_familias.{args.formato}")

            figura_paneles_seccion(
                ranking_inst_prevalencia,
                "prevalencia_pct",
                "Prevalencia por sección",
                "Aplicaciones donde aparece [%]",
                figuras / f"prevalencia_por_seccion.{args.formato}",
                args.top_seccion,
                args.dpi,
                plt,
            )
            generadas.append(f"prevalencia_por_seccion.{args.formato}")
            figura_paneles_seccion(
                ranking_inst_frecuencia,
                "frecuencia_seccion_media_pct",
                "Frecuencia media dentro de cada sección",
                "Frecuencia dentro de la sección [%]",
                figuras / f"frecuencia_por_seccion.{args.formato}",
                args.top_seccion,
                args.dpi,
                plt,
            )
            generadas.append(f"frecuencia_por_seccion.{args.formato}")

            figura_boxplot(
                ranking_inst_frecuencia_global,
                apps,
                apps_ordenadas,
                figuras / f"boxplot_frecuencia_top.{args.formato}",
                args.top,
                args.dpi,
                plt,
            )
            generadas.append(f"boxplot_frecuencia_top.{args.formato}")
            figura_heatmap(
                ranking_inst_prevalencia_global,
                apps,
                apps_ordenadas,
                figuras / f"heatmap_presencia_top.{args.formato}",
                args.top,
                args.dpi,
                plt,
            )
            generadas.append(f"heatmap_presencia_top.{args.formato}")

            if evolucion_inst_global:
                figura_evolucion(
                    evolucion_inst_global,
                    "frecuencia_media_pct",
                    "Evolución de la frecuencia con el tamaño (RiVEC)",
                    "Frecuencia media por aplicación [%]",
                    figuras / f"evolucion_tamano_frecuencia.{args.formato}",
                    min(args.top, 12),
                    args.dpi,
                    plt,
                )
                generadas.append(f"evolucion_tamano_frecuencia.{args.formato}")
                figura_evolucion(
                    evolucion_inst_global,
                    "prevalencia_pct",
                    "Evolución de la prevalencia con el tamaño (RiVEC)",
                    "Aplicaciones donde aparece [%]",
                    figuras / f"evolucion_tamano_prevalencia.{args.formato}",
                    min(args.top, 12),
                    args.dpi,
                    plt,
                    ylim=(0.0, 100.0),
                )
                generadas.append(f"evolucion_tamano_prevalencia.{args.formato}")

    resumen = {
        "resultados": os.path.relpath(args.resultados, BASE),
        "salida": os.path.relpath(args.salida, BASE),
        "archivos_json": len({c.archivo for c in configs}),
        "aplicaciones": len(apps),
        "aplicaciones_con_datos": sum(1 for a in apps.values() if a.tiene_datos),
        "configuraciones": len(configs),
        "instrucciones": len(inst_keys),
        "familias": len(fam_keys),
        "secciones": secciones,
        "ranking_global_excluye_configuracion": True,
        "top": args.top,
        "top_seccion": args.top_seccion,
        "figuras_generadas": generadas,
        "errores": errores,
        "avisos": avisos,
    }
    (args.salida / "resumen.json").write_text(
        json.dumps(resumen, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"CSV y resumen en {args.salida}")
    if generadas:
        print(f"Figuras generadas: {len(generadas)} en {figuras}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
