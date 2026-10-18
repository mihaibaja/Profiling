# TFG - Perfilado de benchmarks RISC-V Vector con RAVE

Repositorio principal del trabajo de perfilado de benchmarks **RISC-V Vector (RVV)** con
**RAVE** (*RISC-V Automated Vector Emulator*). Aquí se reúnen:

- Los **scripts** que compilan y perfilan cada familia de benchmarks.
- Los **resultados** obtenidos (JSON + logs), versionados dentro de este mismo repositorio.
- Tres **submódulos** con el perfilador y los benchmarks: `rave-ext`, `RiVEC` y
  `rvv-evaluation`.
- La **documentación** de apoyo del TFG.

El objetivo es medir, con los contadores de RAVE, el comportamiento vectorial de cargas de
trabajo reales: longitud media de vector (VL), LMUL efectivo, ocupación de VLMAX, mezcla de
instrucciones, dependencias RAW/WAR/WAW, máscaras, políticas `ta`/`tu`, etc.

---

## Índice

1. [Estructura del repositorio](#estructura-del-repositorio)
2. [Requisitos](#requisitos)
3. [Clonado y submódulos](#clonado-y-submódulos)
4. [Configuración](#configuración)
5. [Scripts](#scripts)
6. [Resultados](#resultados)
7. [Submódulos y cambios locales](#submódulos-y-cambios-locales)
8. [Política de `.gitignore`](#política-de-gitignore)
9. [Publicar los submódulos y el repositorio](#publicar-los-submódulos-y-el-repositorio)
10. [Problemas conocidos](#problemas-conocidos)
11. [Licencias](#licencias)

---

## Estructura del repositorio

```text
Profiling/
├── README.md
├── .gitignore
├── .gitmodules
├── config.example.sh        # plantilla de configuración (se versiona)
├── config.sh                # configuración local (NO se versiona)
├── lib/
│   └── common.sh            # resolución de rutas y utilidades comunes
├── run_apps_bench.sh
├── run_assembly_microbench.sh
├── run_proxy_bench.sh
├── run_rivec.sh
├── docs/
│   ├── guia trabajo.md
│   └── rvv instr.md
├── patches/                 # cambios locales de los submódulos, en formato patch
├── resultados/              # resultados versionados (sin repositorio propio)
│   ├── apps_bench/
│   ├── assembly_microbench/
│   ├── proxy_bench/
│   ├── small/
│   └── medium/
├── rave-ext/                # submódulo: perfilador RAVE extendido
├── RiVEC/                   # submódulo: suite de benchmarks RiVEC
└── rvv-evaluation/          # submódulo: benchmarks de KTH-ScaLab
    └── apps_bench/qsim_rvv/ # submódulo anidado
```

| Ruta | Contenido |
| --- | --- |
| `lib/common.sh` | Resuelve la raíz del repositorio, carga `config.sh` y define las rutas por defecto. |
| `config.example.sh` | Plantilla comentada con todas las variables configurables. |
| `run_*.sh` | Scripts de compilación + perfilado. Se explican más abajo. |
| `resultados/` | Resultados de las ejecuciones. **Forma parte del repositorio principal**, no es un submódulo ni tiene repo propio. |
| `docs/` | Notas del TFG y tabla de instrucciones RVV. |
| `patches/` | Parches con los cambios locales de cada submódulo (`.gitignore`, enlaces, etc.). |
| `rave-ext/` | Fork de RAVE con la traza extendida. |
| `RiVEC/` | Suite `riscv-vectorized-benchmark-suite`. |
| `rvv-evaluation/` | Benchmarks de aplicaciones, proxy y microbenchmarks de ensamblador. |

---

## Requisitos

- **Linux x86_64** (el entorno usado para desarrollar ha sido Debian 13).
- `git` (>= 2.40 recomendado) con soporte de submódulos.
- `bash`, `make`, `python3`, `clang`/`clang++` de host.
- **RAVE compilado** y el ejecutable `rave` disponible:
  - o bien en `PATH` (`source rave-ext/environment.sh 1_0`),
  - o bien definiendo `RAVE_BIN` en `config.sh`.
- El **toolchain LLVM cross** que genera `rave-ext`:
  `rave-ext/build/llvm-cross/llvm-EPI-development-toolchain-cross/`.
- Para `run_apps_bench.sh`, el submódulo anidado `rvv-evaluation/apps_bench/qsim_rvv`.

Construir RAVE y sus dependencias (QEMU, LLVM, sysroot, elfutils, etc.):

```bash
cd rave-ext
make all                 # o: make ISA=RVV-1_0
source environment.sh 1_0
cd ..
```

`make all` descarga y compila bastante código; el directorio `rave-ext/build/` puede ocupar
varios GB y está ignorado por git. `rave-ext/downloads/` también está ignorado.

---

## Clonado y submódulos

### Primera clonación

Clona el repositorio principal **junto con todos los submódulos** (incluido el anidado
`qsim_rvv`):

```bash
git clone --recurse-submodules https://github.com/mihaibaja/TFG-Profiling.git
cd TFG-Profiling
```

> Sustituye la URL por la del repositorio real si tiene otro nombre o propietario.

### Si ya clonaste sin submódulos

```bash
git submodule update --init --recursive
```

Si quieres comprobar el estado de los submódulos:

```bash
git submodule status --recursive
```

### Actualizar los submódulos

Para dejar los submódulos en los commits que fija el repositorio principal:

```bash
git submodule sync --recursive
git submodule update --init --recursive
```

Para traer las últimas versiones de sus ramas (opcional; puede cambiar los commits fijados):

```bash
git submodule update --remote --merge
```

Para actualizar solo el submódulo anidado de `qsim_rvv`:

```bash
git -C rvv-evaluation submodule update --init apps_bench/qsim_rvv
```

### Comandos útiles

```bash
# Ver qué commit de cada submódulo está fijado
git submodule status

# Ejecutar un comando dentro de un submódulo
git -C rave-ext status
git -C rvv-evaluation log --oneline -5

# Recorrer todos los submódulos (incluidos los anidados)
git submodule foreach --recursive 'echo "== $name =="; git status --short'
```

---

## Configuración

**Todas las rutas de los scripts son relativas a la raíz del repositorio.** La raíz se
detecta automáticamente a partir de la ubicación de `lib/common.sh`, así que el repositorio
puede moverse o clonarse en cualquier directorio sin editar nada.

La configuración local es opcional:

```bash
cp config.example.sh config.sh
```

`config.sh` está en `.gitignore` y **no se sube al repositorio**. En `config.example.sh`
todas las variables están comentadas con su valor por defecto; solo hay que descomentar y
cambiar lo que sea distinto en tu máquina.

### Variables disponibles

| Variable | Valor por defecto | Descripción |
| --- | --- | --- |
| `PROFILING_ROOT` | directorio del repo (automático) | Raíz del repositorio. |
| `RAVE_HOME` | `$PROFILING_ROOT/rave-ext` | Submódulo del perfilador. |
| `RIVEC_HOME` | `$PROFILING_ROOT/RiVEC` | Submódulo de RiVEC. |
| `RVV_EVAL_HOME` | `$PROFILING_ROOT/rvv-evaluation` | Submódulo de rvv-evaluation. |
| `RESULTS_DIR` | `$PROFILING_ROOT/resultados` | Carpeta raíz de resultados. |
| `TOOLCHAIN` | `$RAVE_HOME/build/llvm-cross/llvm-EPI-development-toolchain-cross` | Toolchain LLVM cross usado al compilar. |
| `RAVE_BIN` | vacío (usa `rave` de `PATH`) | Ruta explícita al ejecutable `rave`. |
| `RAVE_RVV` | `1_0` | Versión de RVV para `rave-ext/environment.sh` (`1_0` o `0_7_1`). |
| `LOAD_RAVE_ENV` | `1` | Carga automáticamente `rave-ext/environment.sh`. `0` lo desactiva. |
| `TMPDIR` | `/tmp` | Directorio para salidas temporales de las apps de RiVEC. |

Prioridad de configuración: **`config.sh` > variable de entorno > valor por defecto**.

### Ejemplo de `config.sh`

```bash
# Si los submódulos están fuera de este repositorio:
RAVE_HOME="$HOME/src/rave-ext"
RIVEC_HOME="$HOME/src/RiVEC"
RVV_EVAL_HOME="$HOME/src/rvv-evaluation"

# Toolchain y binario de RAVE:
TOOLCHAIN="$HOME/toolchains/llvm-EPI-development-toolchain-cross"
RAVE_BIN="$RAVE_HOME/build/qemu-rave/RVV-1_0/bin/rave"

# Resultados en otro disco:
RESULTS_DIR="/mnt/datos/resultados-tfg"
```

Los scripts también aceptan variables de entorno puntuales (`ITERS`, `VLEN`, `TIMEOUT`,
`OUT`, etc.); se documentan en cada sección.

---

## Scripts

Los cuatro scripts compilan (si hace falta) y ejecutan los benchmarks bajo RAVE. Todos
escriben en `resultados/` por defecto y aceptan `SKIP_BUILD=1` para no recompilar.

### `run_apps_bench.sh`

Perfila las aplicaciones de `rvv-evaluation/apps_bench` (actualmente `qsim_rvv`).

```bash
./run_apps_bench.sh
QUBITS=14 ./run_apps_bench.sh qsim_base_rvv
CIRCUIT=circuits/circuit_q24 ./run_apps_bench.sh
SKIP_BUILD=1 ./run_apps_bench.sh
```

| Variable | Defecto | Descripción |
| --- | --- | --- |
| `QUBITS` | `20` | Qubits del circuito GHZ que se genera si falta. |
| `CIRCUIT` | `circuits/ghz_q<QUBITS>` | Circuito a usar. |
| `QSIM_ARGS` | `-t 1 -f 3 -v 3` | Argumentos de la app. |
| `TIMEOUT` | `900` | Segundos máximos por ejecución. |
| `SKIP_BUILD` | `0` | `1` = no recompilar. |
| `OUT` | `resultados/apps_bench/qsim_rvv` | Carpeta de salida. |

Salida: `resultados/apps_bench/qsim_rvv/<app>.json` y `<app>.log`.

### `run_assembly_microbench.sh`

Perfila los microbenchmarks de ensamblador de `rvv-evaluation/assembly_microbench`.

```bash
./run_assembly_microbench.sh
./run_assembly_microbench.sh arith_instr
ITERS=100000 ./run_assembly_microbench.sh gather reduction
SKIP_BUILD=1 ./run_assembly_microbench.sh ldst_instr
ONLY=vadd ./run_assembly_microbench.sh arith_instr
```

Subgrupos: `arith_instr`, `ldst_instr`, `gather`, `reduction`.

| Variable | Defecto | Descripción |
| --- | --- | --- |
| `ITERS` | `200000` (`arith`/`ldst`/`gather`), `10000` (`reduction`) | Iteraciones por kernel. |
| `VLEN` | `256` | VLEN de RAVE en bits. **No subir a 512/16384**: los kernels desbordan la pila. |
| `EXTENSIONS` | `zfh=true,zvfh=true` | Extensiones extra del `-cpu` de QEMU. |
| `TIMEOUT` | `600` | Segundos máximos por ejecución. |
| `SKIP_BUILD` | `0` | `1` = no recompilar. |
| `COMPILERS` | `clang` | Compiladores a construir. |
| `ONLY` | vacío | Subcadena para filtrar kernels por nombre. |
| `OUT` | `resultados/assembly_microbench` | Carpeta de salida. |

Salida: `resultados/assembly_microbench/<subgrupo>/<kernel>.json` y `.log`, más
`run_info.txt` con la configuración de la ejecución.

### `run_proxy_bench.sh`

Perfila los proxy benchmarks de `rvv-evaluation/proxy_bench`: `gemm`, `spmv-v2` y
`darknet`.

```bash
./run_proxy_bench.sh
./run_proxy_bench.sh gemm
SKIP_BUILD=1 ./run_proxy_bench.sh spmv-v2
GEMM_ARGS="1 1 100 1" ./run_proxy_bench.sh gemm
```

| Variable | Defecto | Descripción |
| --- | --- | --- |
| `VARIANTS` | `nonvec autovec autovec_1 autovec_2 autovec_4 autovec_8` | Variantes a construir/ejecutar. |
| `PRECISIONS` | `float` | Solo `gemm`: `float` o `float double`. |
| `THREADS` | `1` | Hilos OpenMP (se ejecuta con 1 para contadores deterministas). |
| `GEMM_ARGS` | `<threads> 2 100 1` | `threads iters size rep`. |
| `SPMV_ARGS` | `<threads> 2 6 3 1` | `threads iters 2log radius rep`. |
| `DARKNET_RUN` | `0` | `1` = ejecutar darknet (por defecto solo se compila). |
| `DARKNET_ARGS` | vacío | Argumentos para darknet. |
| `TIMEOUT` | `900` | Segundos máximos por ejecución. |
| `SKIP_BUILD` | `0` | `1` = no recompilar. |
| `OUT` | `resultados/proxy_bench` | Carpeta de salida. |

Salida: `resultados/proxy_bench/<bench>/<variante>.json` y `.log`.

### `run_rivec.sh`

Compila la variante **vectorial** de RiVEC (RVV 1.0), la ejecuta bajo RAVE y guarda un JSON
por aplicación.

```bash
./run_rivec.sh tiny
./run_rivec.sh small spmv matmul
SKIP_BUILD=1 ./run_rivec.sh medium
TIMEOUT=1200 ./run_rivec.sh large
```

| Argumento / variable | Defecto | Descripción |
| --- | --- | --- |
| `<tamano>` | obligatorio | `tiny`, `small`, `medium` o `large`. Da nombre a la subcarpeta de resultados. |
| `[app ...]` | las 12 apps | Subconjunto de aplicaciones. |
| `TIMEOUT` | `300` | Segundos máximos por ejecución. |
| `SKIP_BUILD` | `0` | `1` = no recompilar. |

Apps: `axpy`, `blackscholes`, `canneal`, `jacobi-2d`, `lavaMD`, `matmul`, `spmv`,
`swaptions`, `streamcluster`, `somier`, `particlefilter`, `pathfinder`.

Salida: `resultados/<tamano>/<app>.json`. Los ficheros temporales de las apps se escriben en
`${TMPDIR:-/tmp}`.

---

## Resultados

`resultados/` se versiona en el repositorio principal y **no tiene repositorio propio**.
Contenido actual:

| Carpeta | Benchmark | JSON | Logs |
| --- | --- | ---: | ---: |
| `resultados/apps_bench/qsim_rvv/` | qsim (aplicación) | 1 | 1 |
| `resultados/assembly_microbench/arith_instr/` | microbenchmarks aritméticos | 52 | 52 |
| `resultados/assembly_microbench/ldst_instr/` | microbenchmarks de carga/almacenamiento | 56 | 56 |
| `resultados/assembly_microbench/gather/` | gather / segmentadas | 8 | 8 |
| `resultados/assembly_microbench/reduction/` | reducciones | 15 | 15 |
| `resultados/proxy_bench/gemm/` | GEMM | 6 | 6 |
| `resultados/proxy_bench/spmv-v2/` | SpMV | 6 | 6 |
| `resultados/small/` | RiVEC tamaño `small` | 12 | - |
| `resultados/medium/` | RiVEC tamaño `medium` | 12 | - |

### Formato de los JSON

Cada JSON lo genera RAVE e incluye, entre otros campos:

- `generator`: siempre `RAVE`.
- `binary`: binario perfilado, con **ruta relativa a la raíz de este repositorio**
  (por ejemplo `rvv-evaluation/proxy_bench/gemm/build/clang/float/gemm_nonvec`).
- `vlen_bits`, `trace_extended`, `accumulate_regions`.
- `regions[]`: contadores por región (bytes movidos, FLOPS, estadísticas vectoriales,
  dependencias escalares/vectoriales, etc.).

La especificación completa de campos está en
[`rave-ext/docs/PROFILER_JSON_API.md`](rave-ext/docs/PROFILER_JSON_API.md).

### Notas sobre los resultados versionados

- Las rutas absolutas que RAVE escribía en el campo `binary` se han normalizado a rutas
  relativas a la raíz del repositorio.
- Los `.log` conservan la salida de cada ejecución. También se han normalizado los prefijos
  absolutos de ruta de la máquina original para que sean relativos.
- Los scripts **sobrescriben** los JSON/logs con el mismo nombre al volver a ejecutarlos.
  Si quieres conservar una ejecución anterior, copia la carpeta o usa `OUT=...`.
- Para regenerar todo desde cero, puedes mover o borrar `resultados/` (está versionado; usa
  `git checkout -- resultados` para recuperarlo).

---

## Submódulos y cambios locales

| Ruta | URL en `.gitmodules` | Upstream | Rama | Función |
| --- | --- | --- | --- | --- |
| `rave-ext` | `https://github.com/mihaibaja/rave-ext.git` | `ucm-chiplet/rave-ext` | `main` | Perfilador RAVE con traza extendida. |
| `RiVEC` | `https://github.com/mihaibaja/RiVEC.git` | `RALC88/riscv-vectorized-benchmark-suite` | `master` | Suite de benchmarks de RiVEC. |
| `rvv-evaluation` | `https://github.com/mihaibaja/rvv-evaluation.git` | `KTH-ScaLab/rvv-evaluation` | `main` | Apps, proxy benchmarks y microbenchmarks. |
| `rvv-evaluation/apps_bench/qsim_rvv` | `https://github.com/KTH-ScaLab/qsim_rvv.git` | `KTH-ScaLab/qsim_rvv` | `main` | Submódulo anidado usado por `run_apps_bench.sh`. |

### Cambios locales en los submódulos

Los tres submódulos apuntan a **forks** (o futuros forks) con una serie de commits locales
necesarios para este TFG:

| Submódulo | Commit local | Cambios |
| --- | --- | --- |
| `rave-ext` | `471d423` | `.gitignore` ampliado y enlace relativo en `docs/README.md`. |
| `RiVEC` | `1de06d2` | `.gitignore` ampliado; se desversionan 48 binarios/`.dump` de `_*/bin/`. |
| `rvv-evaluation` | `6c833bb` | `.gitignore` nuevo; se desversionan 265 artefactos de `assembly_microbench/*/build/`; URL HTTPS para `qsim_rvv`; drivers `arith_instr`/`ldst_instr` aceptan iteraciones por `argv[1]`. |

Estos cambios también están guardados como parches en `patches/` por si necesitas
reproducirlos sobre un clon de los repos upstream:

```bash
git -C rave-ext apply ../patches/rave-ext.patch
git -C RiVEC apply ../patches/rivec.patch
git -C rvv-evaluation apply ../patches/rvv-evaluation.patch
```

Además, para dejar de versionar artefactos que ya estaban en el índice de los repos
originales (los ficheros permanecen en disco):

```bash
git -C RiVEC rm --cached -r --sparse _*/bin
git -C rvv-evaluation rm --cached -r assembly_microbench/*/build
```

### Submódulo anidado `qsim_rvv`

`rvv-evaluation` incluye a su vez `apps_bench/qsim_rvv`. La URL se ha cambiado de SSH a
HTTPS para que `git clone --recurse-submodules` funcione sin llaves SSH:

```bash
git -C rvv-evaluation submodule update --init apps_bench/qsim_rvv
```

### Ramas y ficheros sin seguimiento

`.gitmodules` fija la rama de cada submódulo (`main` o `master`) y usa
`ignore = untracked` para que los ficheros generados dentro de un submódulo (por ejemplo los
`.x` y circuitos de `qsim_rvv`) no marquen el repositorio principal como modificado. Los
cambios en ficheros **sí versionados** del submódulo siguen apareciendo normalmente en
`git status`.

---

## Política de `.gitignore`

El repositorio aplica una política explícita: **ningún producto de compilación debe
subirse**. Cada submódulo tiene su propio `.gitignore`:

### Repositorio principal

- Ignora `config.sh` (configuración local), temporales, ficheros de editor, `__pycache__/`,
  entornos virtuales y posibles artefactos en la raíz (`*.o`, `*.a`, `*.so`, `*.x`, `*.exe`,
  `*.out`, `build/`).
- **No ignora `resultados/`**: los JSON y logs se versionan a propósito.

### `rave-ext`

- Ignora `build/`, `downloads/`, `*.o`, `*.a`, `*.so`, `*.d`, `*.x`, `*.exe`, `*.out`,
  `*.log`, `*.pcf`, `*.row`, `*.prv`, `*.trace`, `*.dmp`, `*.tar*`,
  `compile_commands.json`, `__pycache__/`, `*.pyc`, `rave_sources/obj/`, `validation/bin/`.

### `RiVEC`

- Ignora `bin/`, `build/`, `*.exe`, `*.dump`, `*.o`, `*.a`, `*.so`, `*.d`, `*.out`,
  `*.log`, `output/`, `m5out/`, `*.keep`, `*.swp`.

### `rvv-evaluation`

- Ignora `build/`, `*/build/`, `*.x`, `*.o`, `*.a`, `*.so`, `*.d`, `*.out`, `*.exe`,
  `*.log`, `*.ll`, `__pycache__/`, `*.pyc`, `*.swp`.
- Los artefactos que ya estaban versionados en los repos originales se han eliminado del
  índice con `git rm --cached` (ver sección anterior). Los ficheros siguen existiendo en
  local, pero git ya no los sigue.

Para comprobar que no queda nada raro en el índice:

```bash
git status --short
git submodule foreach --recursive 'git status --short'
```

---

## Publicar los submódulos y el repositorio

Los commits locales de los submódulos deben existir en un remoto accesible para que
`git clone --recurse-submodules` funcione en otra máquina. El flujo previsto es:

1. Crear (si no existen) los forks en GitHub:
   - `rave-ext`: ya existe en `mihaibaja/rave-ext`.
   - `RiVEC`: crear un fork de `RALC88/riscv-vectorized-benchmark-suite` en tu cuenta.
   - `rvv-evaluation`: crear un fork de `KTH-ScaLab/rvv-evaluation` en tu cuenta.
2. Subir los commits locales:

```bash
# rave-ext (origin ya apunta al fork)
git -C rave-ext push origin main

# RiVEC: conservar upstream y publicar el fork
git -C RiVEC remote rename origin upstream
git -C RiVEC remote add origin https://github.com/mihaibaja/RiVEC.git
git -C RiVEC push -u origin master

# rvv-evaluation: conservar upstream y publicar el fork
git -C rvv-evaluation remote rename origin upstream
git -C rvv-evaluation remote add origin https://github.com/mihaibaja/rvv-evaluation.git
git -C rvv-evaluation push -u origin main
```

3. Publicar el repositorio principal:

```bash
git remote add origin https://github.com/mihaibaja/TFG-Profiling.git
git push -u origin main
```

> Los enlaces de `.gitmodules` apuntan a `https://github.com/mihaibaja/...`. Si publicas
> los forks en otra cuenta u organización, actualízalos con:
>
> ```bash
> git submodule set-url RiVEC https://github.com/<usuario>/RiVEC.git
> git submodule set-url rvv-evaluation https://github.com/<usuario>/rvv-evaluation.git
> git submodule sync
> ```

---

## Problemas conocidos

- **`rave` no está en `PATH`**: ejecuta `source rave-ext/environment.sh 1_0` o define
  `RAVE_BIN` en `config.sh`.
- **No encuentra el toolchain**: compila `rave-ext` (`make all`) o ajusta `TOOLCHAIN`.
- **`qsim_rvv` no está clonado**: `git -C rvv-evaluation submodule update --init --recursive`.
- **`darknet` no enlaza en variantes RVV**: al toolchain EPI le falta la libm vectorial
  (`__epi_exp_nxv4f64`, etc.). Solo compila la variante `nonvec`. Además faltan los pesos,
  por lo que por defecto solo se compila (`DARKNET_RUN=1` + `DARKNET_ARGS` para ejecutar).
- **SIGSEGV en microbenchmarks con VLEN grande**: los kernels vierten `v0` sobre
  `int32_t buf[32]`; con VLEN 512 o 16384 se desborda la pila. Usa `VLEN=256`.
- **SIGILL en kernels de coma flotante de 16 bits**: se compilan con `zfh`/`zvfh`, que hay
  que añadir al `-cpu` de QEMU. El script ya lo hace con `RAVE_CUSTOM_EXTENSIONS`.
- **qsim tarda mucho**: cada qubit dobla el trabajo. `q20` ronda los 19 s y `q24` supera los
  5 minutos con contadores. El valor por defecto es `QUBITS=20`.
- **Los contadores no son deterministas con varios hilos**: los scripts ejecutan con 1 hilo
  (`-t 1` en qsim, `THREADS=1` en los proxy benchmarks, OpenMP de RiVEC con 1 hilo).

---

## Licencias

Cada submódulo conserva su licencia original:

- `rave-ext`: BSD 3-Clause (Barcelona Supercomputing Center).
- `RiVEC`: copyright Barcelona Supercomputing Center (ver `RiVEC/LICENSE`).
- `rvv-evaluation`: GNU GPL v3 (ver `rvv-evaluation/LICENSE`).

El contenido propio de este repositorio (scripts, resultados y documentación) se distribuye
junto con el TFG; consulta con el autor antes de reutilizarlo fuera del ámbito académico.
