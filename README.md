# Profiling RAVE - TFG

Scripts y resultados del perfilado de benchmarks **RVV** con **RAVE**. El repositorio
principal contiene los scripts, la documentación y los resultados; el perfilador y los
benchmarks están como submódulos, cada uno con su propio README.

## Estructura

| Ruta | Contenido |
| --- | --- |
| `rave-ext/` | Submódulo: perfilador RAVE extendido. |
| `RiVEC/` | Submódulo: suite de benchmarks RiVEC. |
| `rvv-evaluation/` | Submódulo: apps, proxy benchmarks y microbenchmarks. |
| `resultados/` | Resultados de las ejecuciones (JSON + logs). Forma parte de este repo. |
| `run_*.sh` | Scripts de compilación y perfilado. |
| `config.example.sh` | Plantilla de configuración local. |
| `lib/common.sh` | Resolución de rutas y utilidades comunes. |
| `docs/` | Notas del TFG. |

## Requisitos

- Linux x86_64, `git`, `make`, `python3` y un compilador de host.
- RAVE y su toolchain LLVM cross compilados:

```bash
cd rave-ext
make all
source environment.sh 1_0
cd ..
```

## Clonar el repositorio y sus submódulos

```bash
git clone --recurse-submodules https://github.com/mihaibaja/Profiling.git
cd Profiling
```

Si ya lo clonaste sin submódulos:

```bash
git submodule update --init --recursive
```

Para actualizar los submódulos:

```bash
git submodule sync --recursive
git submodule update --init --recursive
# opcional: traer las últimas versiones de sus ramas
git submodule update --remote --merge
```

## Configuración

Todas las rutas son relativas al repositorio. La configuración local es opcional:

```bash
cp config.example.sh config.sh
```

`config.sh` no se versiona. Solo hay que editarlo si los submódulos, el toolchain o los
resultados están en otra ubicación. Las variables principales son `RAVE_HOME`,
`RIVEC_HOME`, `RVV_EVAL_HOME`, `RESULTS_DIR`, `TOOLCHAIN` y `RAVE_BIN`.

## Uso

| Script | Qué hace |
| --- | --- |
| `./run_apps_bench.sh` | Perfila las aplicaciones de `rvv-evaluation/apps_bench` (qsim). |
| `./run_assembly_microbench.sh` | Perfila los microbenchmarks de ensamblador. |
| `./run_proxy_bench.sh` | Perfila `gemm`, `spmv-v2` y `darknet`. |
| `./run_rivec.sh <tiny\|small\|medium\|large>` | Compila y perfila la variante vectorial de RiVEC. |

Ejemplos:

```bash
./run_apps_bench.sh
./run_assembly_microbench.sh arith_instr
SKIP_BUILD=1 ./run_proxy_bench.sh gemm
./run_rivec.sh small
```

Los resultados se guardan en `resultados/`. Los scripts aceptan variables como `TIMEOUT`,
`SKIP_BUILD=1` y `OUT=<carpeta>`; los parámetros específicos de cada benchmark están
documentados en la cabecera de su script.

## Documentación

- `rave-ext/README.md` y `rave-ext/README_EXTENDED.md`: perfilador y traza extendida.
- `rave-ext/docs/PROFILER_JSON_API.md`: formato de los JSON de resultados.
- `RiVEC/README.md` y `rvv-evaluation/README.md`: benchmarks y sus opciones.
- `docs/`: notas de trabajo y tabla de instrucciones RVV.
