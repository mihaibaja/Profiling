### Puesto en relación con los objetivos generales de CMOS 2.0 

([https\://docs.google.com/document/d/1Qakqn0xfqnC5GZu0QeIf-e4FIs9MINtvOc0g8A\_PTB8/edit?tab=t.fv7lbf1us4ad](https://docs.google.com/document/d/1Qakqn0xfqnC5GZu0QeIf-e4FIs9MINtvOc0g8A_PTB8/edit?tab=t.fv7lbf1us4ad))

### C-T2. Herramienta de modelado/análisis a alto nivel (QEMU)

La idea es tener herramienta para analizar con rapidez benchmarks usando QEMU (RAVE) o similar. La intención es poder recabar fácilmente información sobre:  

- Anchos de vectores de aplicación (monitorizar familia vsetvli y duración de bucles)  
  - Average vector length (el real usado, no VLEN)  
  - ¿Es posible sacar un % de utilización de registros? (tanto en número de registros usados simultáneamente como en ancho real usado; por ejemplo si VLEN=16Kbit pero nuestros vectores sode 256 bits, aunque usemos todos los registros, el % de ocupación es muy bajo)  
- Mix de instrucciones  
  - Entre vectoriales.   
    - Categorías tipo aritméticas / memoria / movimiento entre registros  
    - Otros como: comunica con el datapath escalar  o no (y en qué sentido)  
  - Ration instrucciones escalares / vectoriales  
- Tipos de stride  
  - Páginas (de MV)  que abarca (en función de VLEN)  
  - También con indexed load (gather)  
- Tipos de datos (ELEN/EEW) y frecuencia de cambios de ancho de datos  
- Frecuencia de instrucciones de narrowing/widening. Esto tiene impacto en cambios de layout de los registros vectoriales.  
- Frecuencia  y tamaño de máscaras. Uso de mu/ma (mask unidst/agnostc). De nuevo, puede tener impacto en el trasiego de bytes entre bancos.  
- Uso de tu/ta (tail undisturbed/agnostic)  
  - Cuántas veces de verdad surte efecto (TamVEctorReal \< VLEN)  
- Distancias entre dependencias  
  - Tipos de dependencias (RAW, WAR, WAW)  
- Kernels de cómputo relevantes de la aplicación   
- Número de operandos por instrucción (\#lecturas, \#escrituras al banco de registros, incluyendo mask)  
- Relación de las dependencias: qué clase de instrucción (load, vector. float…) genera el dato que necesita otra clase de instrucciones  
- Arithmetic intensity. ¿Es posible tener una aproximación del ratio entre operaciones y bytes leídos?

   
 Un ejemplo de este tipo de análisis está en [https\://riscv.org/blog/towards-an-integrated-matrix-extension-workload-analysis-of-cnn-inference-with-qemu-tcg-plugings/](https://riscv.org/blog/towards-an-integrated-matrix-extension-workload-analysis-of-cnn-inference-with-qemu-tcg-plugings/) donde analizan la interacción entre instrucciones matriciales y vectoriales.

	El objetivo es tener una primer aproximación a preguntas como:

- Trade-off entre VLEN y LMUL.  A mayor LMUL, vectores más largos pero menos número de registros  (posible spilling…)  
- Relación entre VLEN y rendimiento de una aplicación  
- Relación entre número de lanes, presión en banco de registros- memoria. ¿Hay un sweet-spot?  
- Patrones de acceso habituales  
- Detección (y extracción si es posible)de kernels de cómputo relevantes en una aplicación  
- Previsibles cuellos de botella  
    
  En el caso “muy ideal” podríamos tratar de tener modelos analíticos/estadísticos de rendimiento en función de las características de un benchmark.  
    
- ***Estudiantes relacionados:***  Javier, Mihai.


### C-T5. Recolección de benchmarks

           Buscar benchmarks, desde kernels hasta aplicaciones “grandes” que puedan resultar de interés. En CMOS 2.0 mencionamos “sparse”, así que deberíamos tener un porcentaje significativo de benchs de este tipo.  
     

- Jorge está trabajando con parte del mecanismo de atención de Deep Seek  
- Una línea de trabajo de Mihai será trabajar con BLIS. Querríamos poder ejecutarlo en gem5 y en el entorno QEMU que se plantee.  
- Querríamos tener algo de sparse álgebra (SpMV)

 

- ***Estudiantes relacionados:***  Javier, Mihai, Jorge

Otros

\#\# 3\. Benchmarks

\#\#\# 3.1 RVV-specific

\#\#\#\# RVV-bench

\* Open-source vector-focused microbenchmarks  
\* Covers:  
  \* vector add/mul  
  \* memory bandwidth  
  \* reductions  
\* Often used for ISA validation and tuning  
\* https\://github.com/camel-cdr/rvv-bench

\#\#\#\# RVV-evaluation ScaLab  
https\://github.com/KTH-ScaLab/rvv-evaluation

\#\#\#\# riscv-vector-tests

\* Functional \+ performance-oriented tests  
\* Good for:  
  \* verifying correctness  
  \* basic performance sanity checks  
\* https\://github.com/chipsalliance/riscv-vector-tests

\#\#\#\# ARA benchmarks

\* Used with academic designs like ARA vector unit  
\* Includes:  
  \* FFT  
  \* GEMM  
  \* convolution  
\* Much closer to “real workloads”  
\* https\://github.com/pulp-platform/AraXL/tree/main/apps/benchmarks/kernel

\#\#\#\# RVV Intrinsics benchmarks

\* Based on RVV intrinsics (GCC/LLVM)  
\* https\://github.com/hanliutong/VecIntrinBench

\#\#\#\# RiVEC Bencmark Suite

\* Collection composed of data-parallel applications from different domains.

\* https\://github.com/RALC88/riscv-vectorized-benchmark-suite

\#\#\# 3.2 HPC

\#\#\#\# OpenBLAS (RVV backend)

 \* Not a benchmark per se, but:  
   \* run GEMM benchmarks through it  
   \* realistic performance measurement

\#\#\#\# BLIS (RVV support emerging)

 \* Alternative to OpenBLAS  
 \* Cleaner research-oriented structure

\#\#\#\# FFTW (RVV ports in progress)

 \* FFT-heavy workloads  
 \* Useful for memory \+ compute balance

\#\#\#\# SPEC CPU (RVV-enabled toolchains)

 \* Industry-standard benchmark suite  
 \* Used with RVV-enabled compilers

\#\#\#\# ML workloads

\* Tensor kernels (GEMM, convolution)  
\* ONNX Runtime / TVM (experimental RVV backends)