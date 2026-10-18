## Configuration-Setting Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vsetvli`|`rd, rs1, vtypei`|rd = new vl, rs1 = AVL, vtypei = new vtype setting|vsetvli_counter|vsetvl_instr|
|☑|`vsetivli`|`rd, uimm, vtypei`|rd = new vl, uimm = AVL, vtypei = new vtype setting|vsetivli_counter|vsetvl_instr|
|☑|`vsetvl`|`rd, rs1, rs2`|rd = new vl, rs1 = AVL, rs2 = new vtype value|vsetvl_counter|vsetvl_instr|

## Vector Loads and Stores
### Vector Unit-Stride Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vle8.v`|`vd, (rs1), vm`|8-bit unit-stride load|vle8_v_counter|vunit_instr|
|☑|`vle16.v`|`vd, (rs1), vm`|16-bit unit-stride load|vle16_v_counter|vunit_instr|
|☑|`vle32.v`|`vd, (rs1), vm`|32-bit unit-stride load|vle32_v_counter|vunit_instr|
|☑|`vle64.v`|`vd, (rs1), vm`|64-bit unit-stride load|vle64_v_counter|vunit_instr|
|☑|`vse8.v`|`vs3, (rs1), vm`|8-bit unit-stride store|vse8_v_counter|vunit_instr|
|☑|`vse16.v`|`vs3, (rs1), vm`|16-bit unit-stride store|vse16_v_counter|vunit_instr|
|☑|`vse32.v`|`vs3, (rs1), vm`|32-bit unit-stride store|vse32_v_counter|vunit_instr|
|☑|`vse64.v`|`vs3, (rs1), vm`|64-bit unit-stride store|vse64_v_counter|vunit_instr|
|☑|`vlm.v`|`vd, (rs1)`|Load byte vector of length ceil(vl/8)|vlm_v_counter|vunit_instr|
|☑|`vsm.v`|`vs3, (rs1)`|Store byte vector of length ceil(vl/8)|vsm_v_counter|vunit_instr|

### Vector Strided Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vlse8.v`|`vd, (rs1), rs2, vm`|8-bit strided load|vlse8_v_counter|vstride_instr|
|☑|`vlse16.v`|`vd, (rs1), rs2, vm`|16-bit strided load|vlse16_v_counter|vstride_instr|
|☑|`vlse32.v`|`vd, (rs1), rs2, vm`|32-bit strided load|vlse32_v_counter|vstride_instr|
|☑|`vlse64.v`|`vd, (rs1), rs2, vm`|64-bit strided load|vlse64_v_counter|vstride_instr|
|☑|`vsse8.v`|`vs3, (rs1), rs2, vm`|8-bit strided store|vsse8_v_counter|vstride_instr|
|☑|`vsse16.v`|`vs3, (rs1), rs2, vm`|16-bit strided store|vsse16_v_counter|vstride_instr|
|☑|`vsse32.v`|`vs3, (rs1), rs2, vm`|32-bit strided store|vsse32_v_counter|vstride_instr|
|☑|`vsse64.v`|`vs3, (rs1), rs2, vm`|64-bit strided store|vsse64_v_counter|vstride_instr|

### Vector Indexed Instructions
> En el JSON de RAVE estas instrucciones **no** tienen clave propia: todas las
> cargas se suman en `vector_loads_and_stores.indexed.load` y todos los
> almacenamientos en `indexed.store`. Sus direcciones se resumen por grupo en
> `counters.memory_addresses` (media del rango, mismo peso por instrucción).

|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vluxei8.v`|`vd, (rs1), vs2, vm`|unordered 8-bit indexed load of SEW data|vluxei8_v_counter|vidx_instr, vidx_instr_unordered|
|☑|`vluxei16.v`|`vd, (rs1), vs2, vm`|unordered 16-bit indexed load of SEW data|vluxei16_v_counter|vidx_instr, vidx_instr_unordered|
|☑|`vluxei32.v`|`vd, (rs1), vs2, vm`|unordered 32-bit indexed load of SEW data|vluxei32_v_counter|vidx_instr, vidx_instr_unordered|
|☑|`vluxei64.v`|`vd, (rs1), vs2, vm`|unordered 64-bit indexed load of SEW data|vluxei64_v_counter|vidx_instr, vidx_instr_unordered|
|☑|`vloxei8.v`|`vd, (rs1), vs2, vm`|ordered 8-bit indexed load of SEW data|vloxei8_v_counter|vidx_instr, vidx_instr_ordered|
|☑|`vloxei16.v`|`vd, (rs1), vs2, vm`|ordered 16-bit indexed load of SEW data|vloxei16_v_counter|vidx_instr, vidx_instr_ordered|
|☑|`vloxei32.v`|`vd, (rs1), vs2, vm`|ordered 32-bit indexed load of SEW data|vloxei32_v_counter|vidx_instr, vidx_instr_ordered|
|☑|`vloxei64.v`|`vd, (rs1), vs2, vm`|ordered 64-bit indexed load of SEW data|vloxei64_v_counter|vidx_instr, vidx_instr_ordered|
|☑|`vsuxei8.v`|`vs3, (rs1), vs2, vm`|unordered 8-bit indexed store of SEW data|vsuxei8_v_counter|vidx_instr, vidx_instr_unordered|
|☑|`vsuxei16.v`|`vs3, (rs1), vs2, vm`|unordered 16-bit indexed store of SEW data|vsuxei16_v_counter|vidx_instr, vidx_instr_unordered|
|☑|`vsuxei32.v`|`vs3, (rs1), vs2, vm`|unordered 32-bit indexed store of SEW data|vsuxei32_v_counter|vidx_instr, vidx_instr_unordered|
|☑|`vsuxei64.v`|`vs3, (rs1), vs2, vm`|unordered 64-bit indexed store of SEW data|vsuxei64_v_counter|vidx_instr, vidx_instr_unordered|
|☑|`vsoxei8.v`|`vs3, (rs1), vs2, vm`|ordered 8-bit indexed store of SEW data|vsoxei8_v_counter|vidx_instr, vidx_instr_ordered|
|☑|`vsoxei16.v`|`vs3, (rs1), vs2, vm`|ordered 16-bit indexed store of SEW data|vsoxei16_v_counter|vidx_instr, vidx_instr_ordered|
|☑|`vsoxei32.v`|`vs3, (rs1), vs2, vm`|ordered 32-bit indexed store of SEW data|vsoxei32_v_counter|vidx_instr, vidx_instr_ordered|
|☑|`vsoxei64.v`|`vs3, (rs1), vs2, vm`|ordered 64-bit indexed store of SEW data|vsoxei64_v_counter|vidx_instr, vidx_instr_ordered|

### Unit-stride Fault-Only-First Loads
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vle8ff.v`|`vd, (rs1), vm`|8-bit unit-stride fault-only-first load|vle8ff_v_counter|vunit_instr|
|☑|`vle16ff.v`|`vd, (rs1), vm`|16-bit unit-stride fault-only-first load|vle16ff_v_counter|vunit_instr|
|☑|`vle32ff.v`|`vd, (rs1), vm`|32-bit unit-stride fault-only-first load|vle32ff_v_counter|vunit_instr|
|☑|`vle64ff.v`|`vd, (rs1), vm`|64-bit unit-stride fault-only-first load|vle64ff_v_counter|vunit_instr|

### Vector Load/Store Segment Instructions
#### Vector Unit-Stride Segment Loads and Stores
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vlseg2e8.v`|`vd, (rs1), vm`|unit-stride segment load, 2 fields of 8 bits|vlseg2e8_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg2e16.v`|`vd, (rs1), vm`|unit-stride segment load, 2 fields of 16 bits|vlseg2e16_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg2e32.v`|`vd, (rs1), vm`|unit-stride segment load, 2 fields of 32 bits|vlseg2e32_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg2e64.v`|`vd, (rs1), vm`|unit-stride segment load, 2 fields of 64 bits|vlseg2e64_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg3e8.v`|`vd, (rs1), vm`|unit-stride segment load, 3 fields of 8 bits|vlseg3e8_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg3e16.v`|`vd, (rs1), vm`|unit-stride segment load, 3 fields of 16 bits|vlseg3e16_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg3e32.v`|`vd, (rs1), vm`|unit-stride segment load, 3 fields of 32 bits|vlseg3e32_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg3e64.v`|`vd, (rs1), vm`|unit-stride segment load, 3 fields of 64 bits|vlseg3e64_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg4e8.v`|`vd, (rs1), vm`|unit-stride segment load, 4 fields of 8 bits|vlseg4e8_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg4e16.v`|`vd, (rs1), vm`|unit-stride segment load, 4 fields of 16 bits|vlseg4e16_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg4e32.v`|`vd, (rs1), vm`|unit-stride segment load, 4 fields of 32 bits|vlseg4e32_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg4e64.v`|`vd, (rs1), vm`|unit-stride segment load, 4 fields of 64 bits|vlseg4e64_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg5e8.v`|`vd, (rs1), vm`|unit-stride segment load, 5 fields of 8 bits|vlseg5e8_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg5e16.v`|`vd, (rs1), vm`|unit-stride segment load, 5 fields of 16 bits|vlseg5e16_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg5e32.v`|`vd, (rs1), vm`|unit-stride segment load, 5 fields of 32 bits|vlseg5e32_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg5e64.v`|`vd, (rs1), vm`|unit-stride segment load, 5 fields of 64 bits|vlseg5e64_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg6e8.v`|`vd, (rs1), vm`|unit-stride segment load, 6 fields of 8 bits|vlseg6e8_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg6e16.v`|`vd, (rs1), vm`|unit-stride segment load, 6 fields of 16 bits|vlseg6e16_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg6e32.v`|`vd, (rs1), vm`|unit-stride segment load, 6 fields of 32 bits|vlseg6e32_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg6e64.v`|`vd, (rs1), vm`|unit-stride segment load, 6 fields of 64 bits|vlseg6e64_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg7e8.v`|`vd, (rs1), vm`|unit-stride segment load, 7 fields of 8 bits|vlseg7e8_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg7e16.v`|`vd, (rs1), vm`|unit-stride segment load, 7 fields of 16 bits|vlseg7e16_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg7e32.v`|`vd, (rs1), vm`|unit-stride segment load, 7 fields of 32 bits|vlseg7e32_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg7e64.v`|`vd, (rs1), vm`|unit-stride segment load, 7 fields of 64 bits|vlseg7e64_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg8e8.v`|`vd, (rs1), vm`|Load eight vector registers with eight byte fields.|vlseg8e8_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg8e16.v`|`vd, (rs1), vm`|unit-stride segment load, 8 fields of 16 bits|vlseg8e16_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg8e32.v`|`vd, (rs1), vm`|unit-stride segment load, 8 fields of 32 bits|vlseg8e32_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vlseg8e64.v`|`vd, (rs1), vm`|unit-stride segment load, 8 fields of 64 bits|vlseg8e64_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg2e8.v`|`vs3, (rs1), vm`|unit-stride segment store, 2 fields of 8 bits|vsseg2e8_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg2e16.v`|`vs3, (rs1), vm`|unit-stride segment store, 2 fields of 16 bits|vsseg2e16_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg2e32.v`|`vs3, (rs1), vm`|unit-stride segment store, 2 fields of 32 bits|vsseg2e32_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg2e64.v`|`vs3, (rs1), vm`|unit-stride segment store, 2 fields of 64 bits|vsseg2e64_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg3e8.v`|`vs3, (rs1), vm`|unit-stride segment store, 3 fields of 8 bits|vsseg3e8_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg3e16.v`|`vs3, (rs1), vm`|unit-stride segment store, 3 fields of 16 bits|vsseg3e16_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg3e32.v`|`vs3, (rs1), vm`|Store packed vector of 3*4-byte segments from vs3,vs3+1,vs3+2 to mem|vsseg3e32_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg3e64.v`|`vs3, (rs1), vm`|unit-stride segment store, 3 fields of 64 bits|vsseg3e64_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg4e8.v`|`vs3, (rs1), vm`|unit-stride segment store, 4 fields of 8 bits|vsseg4e8_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg4e16.v`|`vs3, (rs1), vm`|unit-stride segment store, 4 fields of 16 bits|vsseg4e16_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg4e32.v`|`vs3, (rs1), vm`|unit-stride segment store, 4 fields of 32 bits|vsseg4e32_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg4e64.v`|`vs3, (rs1), vm`|unit-stride segment store, 4 fields of 64 bits|vsseg4e64_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg5e8.v`|`vs3, (rs1), vm`|unit-stride segment store, 5 fields of 8 bits|vsseg5e8_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg5e16.v`|`vs3, (rs1), vm`|unit-stride segment store, 5 fields of 16 bits|vsseg5e16_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg5e32.v`|`vs3, (rs1), vm`|unit-stride segment store, 5 fields of 32 bits|vsseg5e32_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg5e64.v`|`vs3, (rs1), vm`|unit-stride segment store, 5 fields of 64 bits|vsseg5e64_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg6e8.v`|`vs3, (rs1), vm`|unit-stride segment store, 6 fields of 8 bits|vsseg6e8_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg6e16.v`|`vs3, (rs1), vm`|unit-stride segment store, 6 fields of 16 bits|vsseg6e16_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg6e32.v`|`vs3, (rs1), vm`|unit-stride segment store, 6 fields of 32 bits|vsseg6e32_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg6e64.v`|`vs3, (rs1), vm`|unit-stride segment store, 6 fields of 64 bits|vsseg6e64_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg7e8.v`|`vs3, (rs1), vm`|unit-stride segment store, 7 fields of 8 bits|vsseg7e8_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg7e16.v`|`vs3, (rs1), vm`|unit-stride segment store, 7 fields of 16 bits|vsseg7e16_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg7e32.v`|`vs3, (rs1), vm`|unit-stride segment store, 7 fields of 32 bits|vsseg7e32_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg7e64.v`|`vs3, (rs1), vm`|unit-stride segment store, 7 fields of 64 bits|vsseg7e64_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg8e8.v`|`vs3, (rs1), vm`|unit-stride segment store, 8 fields of 8 bits|vsseg8e8_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg8e16.v`|`vs3, (rs1), vm`|unit-stride segment store, 8 fields of 16 bits|vsseg8e16_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg8e32.v`|`vs3, (rs1), vm`|unit-stride segment store, 8 fields of 32 bits|vsseg8e32_v_counter|vunit_instr, vseg_instr_unit|
|☑|`vsseg8e64.v`|`vs3, (rs1), vm`|unit-stride segment store, 8 fields of 64 bits|vsseg8e64_v_counter|vunit_instr, vseg_instr_unit|

#### Vector Strided Segment Loads and Stores
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vlsseg2e8.v`|`vd, (rs1), rs2, vm`|strided segment load, 2 fields of 8 bits|vlsseg2e8_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg2e16.v`|`vd, (rs1), rs2, vm`|strided segment load, 2 fields of 16 bits|vlsseg2e16_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg2e32.v`|`vd, (rs1), rs2, vm`|strided segment load, 2 fields of 32 bits|vlsseg2e32_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg2e64.v`|`vd, (rs1), rs2, vm`|strided segment load, 2 fields of 64 bits|vlsseg2e64_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg3e8.v`|`vd, (rs1), rs2, vm`|strided segment load, 3 fields of 8 bits|vlsseg3e8_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg3e16.v`|`vd, (rs1), rs2, vm`|strided segment load, 3 fields of 16 bits|vlsseg3e16_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg3e32.v`|`vd, (rs1), rs2, vm`|strided segment load, 3 fields of 32 bits|vlsseg3e32_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg3e64.v`|`vd, (rs1), rs2, vm`|strided segment load, 3 fields of 64 bits|vlsseg3e64_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg4e8.v`|`vd, (rs1), rs2, vm`|strided segment load, 4 fields of 8 bits|vlsseg4e8_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg4e16.v`|`vd, (rs1), rs2, vm`|strided segment load, 4 fields of 16 bits|vlsseg4e16_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg4e32.v`|`vd, (rs1), rs2, vm`|strided segment load, 4 fields of 32 bits|vlsseg4e32_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg4e64.v`|`vd, (rs1), rs2, vm`|strided segment load, 4 fields of 64 bits|vlsseg4e64_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg5e8.v`|`vd, (rs1), rs2, vm`|strided segment load, 5 fields of 8 bits|vlsseg5e8_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg5e16.v`|`vd, (rs1), rs2, vm`|strided segment load, 5 fields of 16 bits|vlsseg5e16_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg5e32.v`|`vd, (rs1), rs2, vm`|strided segment load, 5 fields of 32 bits|vlsseg5e32_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg5e64.v`|`vd, (rs1), rs2, vm`|strided segment load, 5 fields of 64 bits|vlsseg5e64_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg6e8.v`|`vd, (rs1), rs2, vm`|strided segment load, 6 fields of 8 bits|vlsseg6e8_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg6e16.v`|`vd, (rs1), rs2, vm`|strided segment load, 6 fields of 16 bits|vlsseg6e16_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg6e32.v`|`vd, (rs1), rs2, vm`|strided segment load, 6 fields of 32 bits|vlsseg6e32_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg6e64.v`|`vd, (rs1), rs2, vm`|strided segment load, 6 fields of 64 bits|vlsseg6e64_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg7e8.v`|`vd, (rs1), rs2, vm`|strided segment load, 7 fields of 8 bits|vlsseg7e8_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg7e16.v`|`vd, (rs1), rs2, vm`|strided segment load, 7 fields of 16 bits|vlsseg7e16_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg7e32.v`|`vd, (rs1), rs2, vm`|strided segment load, 7 fields of 32 bits|vlsseg7e32_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg7e64.v`|`vd, (rs1), rs2, vm`|strided segment load, 7 fields of 64 bits|vlsseg7e64_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg8e8.v`|`vd, (rs1), rs2, vm`|strided segment load, 8 fields of 8 bits|vlsseg8e8_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg8e16.v`|`vd, (rs1), rs2, vm`|strided segment load, 8 fields of 16 bits|vlsseg8e16_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg8e32.v`|`vd, (rs1), rs2, vm`|strided segment load, 8 fields of 32 bits|vlsseg8e32_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vlsseg8e64.v`|`vd, (rs1), rs2, vm`|strided segment load, 8 fields of 64 bits|vlsseg8e64_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg2e8.v`|`vs3, (rs1), rs2, vm`|strided segment store, 2 fields of 8 bits|vssseg2e8_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg2e16.v`|`vs3, (rs1), rs2, vm`|strided segment store, 2 fields of 16 bits|vssseg2e16_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg2e32.v`|`vs3, (rs1), rs2, vm`|strided segment store, 2 fields of 32 bits|vssseg2e32_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg2e64.v`|`vs3, (rs1), rs2, vm`|strided segment store, 2 fields of 64 bits|vssseg2e64_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg3e8.v`|`vs3, (rs1), rs2, vm`|strided segment store, 3 fields of 8 bits|vssseg3e8_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg3e16.v`|`vs3, (rs1), rs2, vm`|strided segment store, 3 fields of 16 bits|vssseg3e16_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg3e32.v`|`vs3, (rs1), rs2, vm`|strided segment store, 3 fields of 32 bits|vssseg3e32_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg3e64.v`|`vs3, (rs1), rs2, vm`|strided segment store, 3 fields of 64 bits|vssseg3e64_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg4e8.v`|`vs3, (rs1), rs2, vm`|strided segment store, 4 fields of 8 bits|vssseg4e8_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg4e16.v`|`vs3, (rs1), rs2, vm`|strided segment store, 4 fields of 16 bits|vssseg4e16_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg4e32.v`|`vs3, (rs1), rs2, vm`|strided segment store, 4 fields of 32 bits|vssseg4e32_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg4e64.v`|`vs3, (rs1), rs2, vm`|strided segment store, 4 fields of 64 bits|vssseg4e64_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg5e8.v`|`vs3, (rs1), rs2, vm`|strided segment store, 5 fields of 8 bits|vssseg5e8_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg5e16.v`|`vs3, (rs1), rs2, vm`|strided segment store, 5 fields of 16 bits|vssseg5e16_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg5e32.v`|`vs3, (rs1), rs2, vm`|strided segment store, 5 fields of 32 bits|vssseg5e32_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg5e64.v`|`vs3, (rs1), rs2, vm`|strided segment store, 5 fields of 64 bits|vssseg5e64_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg6e8.v`|`vs3, (rs1), rs2, vm`|strided segment store, 6 fields of 8 bits|vssseg6e8_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg6e16.v`|`vs3, (rs1), rs2, vm`|strided segment store, 6 fields of 16 bits|vssseg6e16_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg6e32.v`|`vs3, (rs1), rs2, vm`|strided segment store, 6 fields of 32 bits|vssseg6e32_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg6e64.v`|`vs3, (rs1), rs2, vm`|strided segment store, 6 fields of 64 bits|vssseg6e64_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg7e8.v`|`vs3, (rs1), rs2, vm`|strided segment store, 7 fields of 8 bits|vssseg7e8_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg7e16.v`|`vs3, (rs1), rs2, vm`|strided segment store, 7 fields of 16 bits|vssseg7e16_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg7e32.v`|`vs3, (rs1), rs2, vm`|strided segment store, 7 fields of 32 bits|vssseg7e32_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg7e64.v`|`vs3, (rs1), rs2, vm`|strided segment store, 7 fields of 64 bits|vssseg7e64_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg8e8.v`|`vs3, (rs1), rs2, vm`|strided segment store, 8 fields of 8 bits|vssseg8e8_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg8e16.v`|`vs3, (rs1), rs2, vm`|strided segment store, 8 fields of 16 bits|vssseg8e16_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg8e32.v`|`vs3, (rs1), rs2, vm`|strided segment store, 8 fields of 32 bits|vssseg8e32_v_counter|vstride_instr, vseg_instr_stride|
|☑|`vssseg8e64.v`|`vs3, (rs1), rs2, vm`|strided segment store, 8 fields of 64 bits|vssseg8e64_v_counter|vstride_instr, vseg_instr_stride|

#### Vector Indexed Segment Loads and Stores
> En el JSON de RAVE estas instrucciones **no** tienen clave propia: todas las
> cargas se suman en `vector_loads_and_stores.indexed.load` y todos los
> almacenamientos en `indexed.store`. Sus direcciones se resumen por grupo en
> `counters.memory_addresses` (media del rango, mismo peso por instrucción).

|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vluxseg2ei8.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 2 fields, 8-bit byte offsets|vluxseg2ei8_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg2ei16.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 2 fields, 16-bit byte offsets|vluxseg2ei16_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg2ei32.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 2 fields, 32-bit byte offsets|vluxseg2ei32_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg2ei64.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 2 fields, 64-bit byte offsets|vluxseg2ei64_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg3ei8.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 3 fields, 8-bit byte offsets|vluxseg3ei8_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg3ei16.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 3 fields, 16-bit byte offsets|vluxseg3ei16_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg3ei32.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 3 fields, 32-bit byte offsets|vluxseg3ei32_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg3ei64.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 3 fields, 64-bit byte offsets|vluxseg3ei64_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg4ei8.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 4 fields, 8-bit byte offsets|vluxseg4ei8_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg4ei16.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 4 fields, 16-bit byte offsets|vluxseg4ei16_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg4ei32.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 4 fields, 32-bit byte offsets|vluxseg4ei32_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg4ei64.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 4 fields, 64-bit byte offsets|vluxseg4ei64_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg5ei8.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 5 fields, 8-bit byte offsets|vluxseg5ei8_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg5ei16.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 5 fields, 16-bit byte offsets|vluxseg5ei16_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg5ei32.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 5 fields, 32-bit byte offsets|vluxseg5ei32_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg5ei64.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 5 fields, 64-bit byte offsets|vluxseg5ei64_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg6ei8.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 6 fields, 8-bit byte offsets|vluxseg6ei8_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg6ei16.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 6 fields, 16-bit byte offsets|vluxseg6ei16_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg6ei32.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 6 fields, 32-bit byte offsets|vluxseg6ei32_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg6ei64.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 6 fields, 64-bit byte offsets|vluxseg6ei64_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg7ei8.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 7 fields, 8-bit byte offsets|vluxseg7ei8_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg7ei16.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 7 fields, 16-bit byte offsets|vluxseg7ei16_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg7ei32.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 7 fields, 32-bit byte offsets|vluxseg7ei32_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg7ei64.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 7 fields, 64-bit byte offsets|vluxseg7ei64_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg8ei8.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 8 fields, 8-bit byte offsets|vluxseg8ei8_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg8ei16.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 8 fields, 16-bit byte offsets|vluxseg8ei16_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg8ei32.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 8 fields, 32-bit byte offsets|vluxseg8ei32_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vluxseg8ei64.v`|`vd, (rs1), vs2, vm`|indexed-unordered segment load of SEW data, 8 fields, 64-bit byte offsets|vluxseg8ei64_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vloxseg2ei8.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 2 fields, 8-bit byte offsets|vloxseg2ei8_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg2ei16.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 2 fields, 16-bit byte offsets|vloxseg2ei16_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg2ei32.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 2 fields, 32-bit byte offsets|vloxseg2ei32_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg2ei64.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 2 fields, 64-bit byte offsets|vloxseg2ei64_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg3ei8.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 3 fields, 8-bit byte offsets|vloxseg3ei8_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg3ei16.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 3 fields, 16-bit byte offsets|vloxseg3ei16_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg3ei32.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 3 fields, 32-bit byte offsets|vloxseg3ei32_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg3ei64.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 3 fields, 64-bit byte offsets|vloxseg3ei64_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg4ei8.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 4 fields, 8-bit byte offsets|vloxseg4ei8_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg4ei16.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 4 fields, 16-bit byte offsets|vloxseg4ei16_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg4ei32.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 4 fields, 32-bit byte offsets|vloxseg4ei32_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg4ei64.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 4 fields, 64-bit byte offsets|vloxseg4ei64_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg5ei8.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 5 fields, 8-bit byte offsets|vloxseg5ei8_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg5ei16.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 5 fields, 16-bit byte offsets|vloxseg5ei16_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg5ei32.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 5 fields, 32-bit byte offsets|vloxseg5ei32_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg5ei64.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 5 fields, 64-bit byte offsets|vloxseg5ei64_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg6ei8.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 6 fields, 8-bit byte offsets|vloxseg6ei8_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg6ei16.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 6 fields, 16-bit byte offsets|vloxseg6ei16_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg6ei32.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 6 fields, 32-bit byte offsets|vloxseg6ei32_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg6ei64.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 6 fields, 64-bit byte offsets|vloxseg6ei64_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg7ei8.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 7 fields, 8-bit byte offsets|vloxseg7ei8_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg7ei16.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 7 fields, 16-bit byte offsets|vloxseg7ei16_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg7ei32.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 7 fields, 32-bit byte offsets|vloxseg7ei32_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg7ei64.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 7 fields, 64-bit byte offsets|vloxseg7ei64_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg8ei8.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 8 fields, 8-bit byte offsets|vloxseg8ei8_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg8ei16.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 8 fields, 16-bit byte offsets|vloxseg8ei16_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg8ei32.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 8 fields, 32-bit byte offsets|vloxseg8ei32_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vloxseg8ei64.v`|`vd, (rs1), vs2, vm`|indexed-ordered segment load of SEW data, 8 fields, 64-bit byte offsets|vloxseg8ei64_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsuxseg2ei8.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 2 fields, 8-bit byte offsets|vsuxseg2ei8_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg2ei16.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 2 fields, 16-bit byte offsets|vsuxseg2ei16_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg2ei32.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 2 fields, 32-bit byte offsets|vsuxseg2ei32_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg2ei64.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 2 fields, 64-bit byte offsets|vsuxseg2ei64_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg3ei8.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 3 fields, 8-bit byte offsets|vsuxseg3ei8_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg3ei16.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 3 fields, 16-bit byte offsets|vsuxseg3ei16_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg3ei32.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 3 fields, 32-bit byte offsets|vsuxseg3ei32_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg3ei64.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 3 fields, 64-bit byte offsets|vsuxseg3ei64_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg4ei8.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 4 fields, 8-bit byte offsets|vsuxseg4ei8_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg4ei16.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 4 fields, 16-bit byte offsets|vsuxseg4ei16_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg4ei32.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 4 fields, 32-bit byte offsets|vsuxseg4ei32_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg4ei64.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 4 fields, 64-bit byte offsets|vsuxseg4ei64_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg5ei8.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 5 fields, 8-bit byte offsets|vsuxseg5ei8_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg5ei16.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 5 fields, 16-bit byte offsets|vsuxseg5ei16_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg5ei32.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 5 fields, 32-bit byte offsets|vsuxseg5ei32_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg5ei64.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 5 fields, 64-bit byte offsets|vsuxseg5ei64_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg6ei8.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 6 fields, 8-bit byte offsets|vsuxseg6ei8_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg6ei16.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 6 fields, 16-bit byte offsets|vsuxseg6ei16_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg6ei32.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 6 fields, 32-bit byte offsets|vsuxseg6ei32_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg6ei64.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 6 fields, 64-bit byte offsets|vsuxseg6ei64_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg7ei8.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 7 fields, 8-bit byte offsets|vsuxseg7ei8_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg7ei16.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 7 fields, 16-bit byte offsets|vsuxseg7ei16_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg7ei32.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 7 fields, 32-bit byte offsets|vsuxseg7ei32_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg7ei64.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 7 fields, 64-bit byte offsets|vsuxseg7ei64_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg8ei8.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 8 fields, 8-bit byte offsets|vsuxseg8ei8_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg8ei16.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 8 fields, 16-bit byte offsets|vsuxseg8ei16_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg8ei32.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 8 fields, 32-bit byte offsets|vsuxseg8ei32_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsuxseg8ei64.v`|`vs3, (rs1), vs2, vm`|indexed-unordered segment store of SEW data, 8 fields, 64-bit byte offsets|vsuxseg8ei64_v_counter|vidx_instr, vidx_instr_unordered, vseg_instr_idx|
|☑|`vsoxseg2ei8.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 2 fields, 8-bit byte offsets|vsoxseg2ei8_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg2ei16.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 2 fields, 16-bit byte offsets|vsoxseg2ei16_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg2ei32.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 2 fields, 32-bit byte offsets|vsoxseg2ei32_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg2ei64.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 2 fields, 64-bit byte offsets|vsoxseg2ei64_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg3ei8.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 3 fields, 8-bit byte offsets|vsoxseg3ei8_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg3ei16.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 3 fields, 16-bit byte offsets|vsoxseg3ei16_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg3ei32.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 3 fields, 32-bit byte offsets|vsoxseg3ei32_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg3ei64.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 3 fields, 64-bit byte offsets|vsoxseg3ei64_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg4ei8.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 4 fields, 8-bit byte offsets|vsoxseg4ei8_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg4ei16.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 4 fields, 16-bit byte offsets|vsoxseg4ei16_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg4ei32.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 4 fields, 32-bit byte offsets|vsoxseg4ei32_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg4ei64.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 4 fields, 64-bit byte offsets|vsoxseg4ei64_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg5ei8.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 5 fields, 8-bit byte offsets|vsoxseg5ei8_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg5ei16.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 5 fields, 16-bit byte offsets|vsoxseg5ei16_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg5ei32.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 5 fields, 32-bit byte offsets|vsoxseg5ei32_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg5ei64.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 5 fields, 64-bit byte offsets|vsoxseg5ei64_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg6ei8.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 6 fields, 8-bit byte offsets|vsoxseg6ei8_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg6ei16.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 6 fields, 16-bit byte offsets|vsoxseg6ei16_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg6ei32.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 6 fields, 32-bit byte offsets|vsoxseg6ei32_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg6ei64.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 6 fields, 64-bit byte offsets|vsoxseg6ei64_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg7ei8.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 7 fields, 8-bit byte offsets|vsoxseg7ei8_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg7ei16.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 7 fields, 16-bit byte offsets|vsoxseg7ei16_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg7ei32.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 7 fields, 32-bit byte offsets|vsoxseg7ei32_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg7ei64.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 7 fields, 64-bit byte offsets|vsoxseg7ei64_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg8ei8.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 8 fields, 8-bit byte offsets|vsoxseg8ei8_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg8ei16.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 8 fields, 16-bit byte offsets|vsoxseg8ei16_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg8ei32.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 8 fields, 32-bit byte offsets|vsoxseg8ei32_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|
|☑|`vsoxseg8ei64.v`|`vs3, (rs1), vs2, vm`|indexed-ordered segment store of SEW data, 8 fields, 64-bit byte offsets|vsoxseg8ei64_v_counter|vidx_instr, vidx_instr_ordered, vseg_instr_idx|

### Vector Load/Store Whole Register Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vl1re8.v`|`vd, (rs1)`|load 1 whole register, EEW=8|vl1re8_v_counter|vspill_instr|
|☑|`vl1re16.v`|`vd, (rs1)`|load 1 whole register, EEW=16|vl1re16_v_counter|vspill_instr|
|☑|`vl1re32.v`|`vd, (rs1)`|load 1 whole register, EEW=32|vl1re32_v_counter|vspill_instr|
|☑|`vl1re64.v`|`vd, (rs1)`|load 1 whole register, EEW=64|vl1re64_v_counter|vspill_instr|
|☑|`vl2re8.v`|`vd, (rs1)`|load 2 whole registers, EEW=8|vl2re8_v_counter|vspill_instr|
|☑|`vl2re16.v`|`vd, (rs1)`|load 2 whole registers, EEW=16|vl2re16_v_counter|vspill_instr|
|☑|`vl2re32.v`|`vd, (rs1)`|load 2 whole registers, EEW=32|vl2re32_v_counter|vspill_instr|
|☑|`vl2re64.v`|`vd, (rs1)`|load 2 whole registers, EEW=64|vl2re64_v_counter|vspill_instr|
|☑|`vl4re8.v`|`vd, (rs1)`|load 4 whole registers, EEW=8|vl4re8_v_counter|vspill_instr|
|☑|`vl4re16.v`|`vd, (rs1)`|load 4 whole registers, EEW=16|vl4re16_v_counter|vspill_instr|
|☑|`vl4re32.v`|`vd, (rs1)`|load 4 whole registers, EEW=32|vl4re32_v_counter|vspill_instr|
|☑|`vl4re64.v`|`vd, (rs1)`|load 4 whole registers, EEW=64|vl4re64_v_counter|vspill_instr|
|☑|`vl8re8.v`|`vd, (rs1)`|load 8 whole registers, EEW=8|vl8re8_v_counter|vspill_instr|
|☑|`vl8re16.v`|`vd, (rs1)`|load 8 whole registers, EEW=16|vl8re16_v_counter|vspill_instr|
|☑|`vl8re32.v`|`vd, (rs1)`|load 8 whole registers, EEW=32|vl8re32_v_counter|vspill_instr|
|☑|`vl8re64.v`|`vd, (rs1)`|load 8 whole registers, EEW=64|vl8re64_v_counter|vspill_instr|
|☑|`vs1r.v`|`vs3, (rs1)`|store 1 whole register, EEW=8|vs1r_v_counter|vspill_instr|
|☑|`vs2r.v`|`vs3, (rs1)`|store 2 whole registers, EEW=8|vs2r_v_counter|vspill_instr|
|☑|`vs4r.v`|`vs3, (rs1)`|store 4 whole registers, EEW=8|vs4r_v_counter|vspill_instr|
|☑|`vs8r.v`|`vs3, (rs1)`|store 8 whole registers, EEW=8|vs8r_v_counter|vspill_instr|

## Vector Integer Arithmetic Instructions
### Vector Single-Width Integer Add and Subtract
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vadd.vv`|`vd, vs2, vs1, vm`|Vector-vector|vadd_vv_counter|vint_instr, vcomputation_instr|
|☑|`vadd.vx`|`vd, vs2, rs1, vm`|vector-scalar|vadd_vx_counter|vint_instr, vcomputation_instr|
|☑|`vadd.vi`|`vd, vs2, imm, vm`|vector-immediate|vadd_vi_counter|vint_instr, vcomputation_instr|
|☑|`vsub.vv`|`vd, vs2, vs1, vm`|Vector-vector|vsub_vv_counter|vint_instr, vcomputation_instr|
|☑|`vsub.vx`|`vd, vs2, rs1, vm`|vector-scalar|vsub_vx_counter|vint_instr, vcomputation_instr|
|☑|`vrsub.vx`|`vd, vs2, rs1, vm`|vd[i] = x[rs1] - vs2[i]|vrsub_vx_counter|vint_instr, vcomputation_instr|
|☑|`vrsub.vi`|`vd, vs2, imm, vm`|vd[i] = imm - vs2[i]|vrsub_vi_counter|vint_instr, vcomputation_instr|

### Vector Widening Integer Add/Subtract
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vwaddu.vv`|`vd, vs2, vs1, vm`|vector-vector|vwaddu_vv_counter|vint_instr, vwidening_instr|
|☑|`vwaddu.vx`|`vd, vs2, rs1, vm`|vector-scalar|vwaddu_vx_counter|vint_instr, vwidening_instr|
|☑|`vwaddu.wv`|`vd, vs2, vs1, vm`|vector-vector|vwaddu_wv_counter|vint_instr, vwidening_instr|
|☑|`vwaddu.wx`|`vd, vs2, rs1, vm`|vector-scalar|vwaddu_wx_counter|vint_instr, vwidening_instr|
|☑|`vwsubu.vv`|`vd, vs2, vs1, vm`|vector-vector|vwsubu_vv_counter|vint_instr, vwidening_instr|
|☑|`vwsubu.vx`|`vd, vs2, rs1, vm`|vector-scalar|vwsubu_vx_counter|vint_instr, vwidening_instr|
|☑|`vwsubu.wv`|`vd, vs2, vs1, vm`|vector-vector|vwsubu_wv_counter|vint_instr, vwidening_instr|
|☑|`vwsubu.wx`|`vd, vs2, rs1, vm`|vector-scalar|vwsubu_wx_counter|vint_instr, vwidening_instr|
|☑|`vwadd.vv`|`vd, vs2, vs1, vm`|vector-vector|vwadd_vv_counter|vint_instr, vwidening_instr|
|☑|`vwadd.vx`|`vd, vs2, rs1, vm`|vector-scalar|vwadd_vx_counter|vint_instr, vwidening_instr|
|☑|`vwadd.wv`|`vd, vs2, vs1, vm`|vector-vector|vwadd_wv_counter|vint_instr, vwidening_instr|
|☑|`vwadd.wx`|`vd, vs2, rs1, vm`|vector-scalar|vwadd_wx_counter|vint_instr, vwidening_instr|
|☑|`vwsub.vv`|`vd, vs2, vs1, vm`|vector-vector|vwsub_vv_counter|vint_instr, vwidening_instr|
|☑|`vwsub.vx`|`vd, vs2, rs1, vm`|vector-scalar|vwsub_vx_counter|vint_instr, vwidening_instr|
|☑|`vwsub.wv`|`vd, vs2, vs1, vm`|vector-vector|vwsub_wv_counter|vint_instr, vwidening_instr|
|☑|`vwsub.wx`|`vd, vs2, rs1, vm`|vector-scalar|vwsub_wx_counter|vint_instr, vwidening_instr|

### Vector Integer Extension
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vzext.vf2`|`vd, vs2, vm`|Zero-extend SEW/2 source to SEW destination|vzext_vf2_counter|vint_instr, vcomputation_instr|
|☑|`vzext.vf4`|`vd, vs2, vm`|Zero-extend SEW/4 source to SEW destination|vzext_vf4_counter|vint_instr, vcomputation_instr|
|☑|`vzext.vf8`|`vd, vs2, vm`|Zero-extend SEW/8 source to SEW destination|vzext_vf8_counter|vint_instr, vcomputation_instr|
|☑|`vsext.vf2`|`vd, vs2, vm`|Sign-extend SEW/2 source to SEW destination|vsext_vf2_counter|vint_instr, vcomputation_instr|
|☑|`vsext.vf4`|`vd, vs2, vm`|Sign-extend SEW/4 source to SEW destination|vsext_vf4_counter|vint_instr, vcomputation_instr|
|☑|`vsext.vf8`|`vd, vs2, vm`|Sign-extend SEW/8 source to SEW destination|vsext_vf8_counter|vint_instr, vcomputation_instr|

### Vector Integer Add-with-Carry / Subtract-with-Borrow Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vadc.vvm`|`vd, vs2, vs1, v0`|Vector-vector|vadc_vvm_counter|vint_instr, vcomputation_instr|
|☑|`vadc.vxm`|`vd, vs2, rs1, v0`|Vector-scalar|vadc_vxm_counter|vint_instr, vcomputation_instr|
|☑|`vadc.vim`|`vd, vs2, imm, v0`|Vector-immediate|vadc_vim_counter|vint_instr, vcomputation_instr|
|☑|`vmadc.vvm`|`vd, vs2, vs1, v0`|Vector-vector|vmadc_vvm_counter|vint_instr, vcomputation_instr|
|☑|`vmadc.vxm`|`vd, vs2, rs1, v0`|Vector-scalar|vmadc_vxm_counter|vint_instr, vcomputation_instr|
|☑|`vmadc.vim`|`vd, vs2, imm, v0`|Vector-immediate|vmadc_vim_counter|vint_instr, vcomputation_instr|
|☑|`vmadc.vv`|`vd, vs2, vs1`|Vector-vector, no carry-in|vmadc_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmadc.vx`|`vd, vs2, rs1`|Vector-scalar, no carry-in|vmadc_vx_counter|vint_instr, vcomputation_instr|
|☑|`vmadc.vi`|`vd, vs2, imm`|Vector-immediate, no carry-in|vmadc_vi_counter|vint_instr, vcomputation_instr|
|☑|`vsbc.vvm`|`vd, vs2, vs1, v0`|Vector-vector|vsbc_vvm_counter|vint_instr, vcomputation_instr|
|☑|`vsbc.vxm`|`vd, vs2, rs1, v0`|Vector-scalar|vsbc_vxm_counter|vint_instr, vcomputation_instr|
|☑|`vmsbc.vvm`|`vd, vs2, vs1, v0`|Vector-vector|vmsbc_vvm_counter|vint_instr, vcomputation_instr|
|☑|`vmsbc.vxm`|`vd, vs2, rs1, v0`|Vector-scalar|vmsbc_vxm_counter|vint_instr, vcomputation_instr|
|☑|`vmsbc.vv`|`vd, vs2, vs1`|Vector-vector, no borrow-in|vmsbc_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmsbc.vx`|`vd, vs2, rs1`|Vector-scalar, no borrow-in|vmsbc_vx_counter|vint_instr, vcomputation_instr|

### Vector Bitwise Logical Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vand.vv`|`vd, vs2, vs1, vm`|Vector-vector|vand_vv_counter|vint_instr, vcomputation_instr|
|☑|`vand.vx`|`vd, vs2, rs1, vm`|vector-scalar|vand_vx_counter|vint_instr, vcomputation_instr|
|☑|`vand.vi`|`vd, vs2, imm, vm`|vector-immediate|vand_vi_counter|vint_instr, vcomputation_instr|
|☑|`vor.vv`|`vd, vs2, vs1, vm`|Vector-vector|vor_vv_counter|vint_instr, vcomputation_instr|
|☑|`vor.vx`|`vd, vs2, rs1, vm`|vector-scalar|vor_vx_counter|vint_instr, vcomputation_instr|
|☑|`vor.vi`|`vd, vs2, imm, vm`|vector-immediate|vor_vi_counter|vint_instr, vcomputation_instr|
|☑|`vxor.vv`|`vd, vs2, vs1, vm`|Vector-vector|vxor_vv_counter|vint_instr, vcomputation_instr|
|☑|`vxor.vx`|`vd, vs2, rs1, vm`|vector-scalar|vxor_vx_counter|vint_instr, vcomputation_instr|
|☑|`vxor.vi`|`vd, vs2, imm, vm`|vector-immediate|vxor_vi_counter|vint_instr, vcomputation_instr|

### Vector Single-Width Shift Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vsll.vv`|`vd, vs2, vs1, vm`|Vector-vector|vsll_vv_counter|vint_instr, vcomputation_instr|
|☑|`vsll.vx`|`vd, vs2, rs1, vm`|vector-scalar|vsll_vx_counter|vint_instr, vcomputation_instr|
|☑|`vsll.vi`|`vd, vs2, uimm, vm`|vector-immediate|vsll_vi_counter|vint_instr, vcomputation_instr|
|☑|`vsrl.vv`|`vd, vs2, vs1, vm`|Vector-vector|vsrl_vv_counter|vint_instr, vcomputation_instr|
|☑|`vsrl.vx`|`vd, vs2, rs1, vm`|vector-scalar|vsrl_vx_counter|vint_instr, vcomputation_instr|
|☑|`vsrl.vi`|`vd, vs2, uimm, vm`|vector-immediate|vsrl_vi_counter|vint_instr, vcomputation_instr|
|☑|`vsra.vv`|`vd, vs2, vs1, vm`|Vector-vector|vsra_vv_counter|vint_instr, vcomputation_instr|
|☑|`vsra.vx`|`vd, vs2, rs1, vm`|vector-scalar|vsra_vx_counter|vint_instr, vcomputation_instr|
|☑|`vsra.vi`|`vd, vs2, uimm, vm`|vector-immediate|vsra_vi_counter|vint_instr, vcomputation_instr|

### Vector Narrowing Integer Right Shift Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vnsrl.wv`|`vd, vs2, vs1, vm`|vector-vector|vnsrl_wv_counter|vint_instr, vnarrowing_instr|
|☑|`vnsrl.wx`|`vd, vs2, rs1, vm`|vector-scalar|vnsrl_wx_counter|vint_instr, vnarrowing_instr|
|☑|`vnsrl.wi`|`vd, vs2, uimm, vm`|vector-immediate|vnsrl_wi_counter|vint_instr, vnarrowing_instr|
|☑|`vnsra.wv`|`vd, vs2, vs1, vm`|vector-vector|vnsra_wv_counter|vint_instr, vnarrowing_instr|
|☑|`vnsra.wx`|`vd, vs2, rs1, vm`|vector-scalar|vnsra_wx_counter|vint_instr, vnarrowing_instr|
|☑|`vnsra.wi`|`vd, vs2, uimm, vm`|vector-immediate|vnsra_wi_counter|vint_instr, vnarrowing_instr|

### Vector Integer Compare Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vmseq.vv`|`vd, vs2, vs1, vm`|Vector-vector|vmseq_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmseq.vx`|`vd, vs2, rs1, vm`|vector-scalar|vmseq_vx_counter|vint_instr, vcomputation_instr|
|☑|`vmseq.vi`|`vd, vs2, imm, vm`|vector-immediate|vmseq_vi_counter|vint_instr, vcomputation_instr|
|☑|`vmsne.vv`|`vd, vs2, vs1, vm`|Vector-vector|vmsne_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmsne.vx`|`vd, vs2, rs1, vm`|vector-scalar|vmsne_vx_counter|vint_instr, vcomputation_instr|
|☑|`vmsne.vi`|`vd, vs2, imm, vm`|vector-immediate|vmsne_vi_counter|vint_instr, vcomputation_instr|
|☑|`vmsltu.vv`|`vd, vs2, vs1, vm`|Vector-vector|vmsltu_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmsltu.vx`|`vd, vs2, rs1, vm`|Vector-scalar|vmsltu_vx_counter|vint_instr, vcomputation_instr|
|☑|`vmslt.vv`|`vd, vs2, vs1, vm`|Vector-vector|vmslt_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmslt.vx`|`vd, vs2, rs1, vm`|vector-scalar|vmslt_vx_counter|vint_instr, vcomputation_instr|
|☑|`vmsleu.vv`|`vd, vs2, vs1, vm`|Vector-vector|vmsleu_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmsleu.vx`|`vd, vs2, rs1, vm`|vector-scalar|vmsleu_vx_counter|vint_instr, vcomputation_instr|
|☑|`vmsleu.vi`|`vd, vs2, imm, vm`|Vector-immediate|vmsleu_vi_counter|vint_instr, vcomputation_instr|
|☑|`vmsle.vv`|`vd, vs2, vs1, vm`|Vector-vector|vmsle_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmsle.vx`|`vd, vs2, rs1, vm`|vector-scalar|vmsle_vx_counter|vint_instr, vcomputation_instr|
|☑|`vmsle.vi`|`vd, vs2, imm, vm`|vector-immediate|vmsle_vi_counter|vint_instr, vcomputation_instr|
|☑|`vmsgtu.vx`|`vd, vs2, rs1, vm`|Vector-scalar|vmsgtu_vx_counter|vint_instr, vcomputation_instr|
|☑|`vmsgtu.vi`|`vd, vs2, imm, vm`|Vector-immediate|vmsgtu_vi_counter|vint_instr, vcomputation_instr|
|☑|`vmsgt.vx`|`vd, vs2, rs1, vm`|Vector-scalar|vmsgt_vx_counter|vint_instr, vcomputation_instr|
|☑|`vmsgt.vi`|`vd, vs2, imm, vm`|Vector-immediate|vmsgt_vi_counter|vint_instr, vcomputation_instr|

### Vector Integer Min/Max Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vminu.vv`|`vd, vs2, vs1, vm`|Vector-vector|vminu_vv_counter|vint_instr, vcomputation_instr|
|☑|`vminu.vx`|`vd, vs2, rs1, vm`|vector-scalar|vminu_vx_counter|vint_instr, vcomputation_instr|
|☑|`vmin.vv`|`vd, vs2, vs1, vm`|Vector-vector|vmin_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmin.vx`|`vd, vs2, rs1, vm`|vector-scalar|vmin_vx_counter|vint_instr, vcomputation_instr|
|☑|`vmaxu.vv`|`vd, vs2, vs1, vm`|Vector-vector|vmaxu_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmaxu.vx`|`vd, vs2, rs1, vm`|vector-scalar|vmaxu_vx_counter|vint_instr, vcomputation_instr|
|☑|`vmax.vv`|`vd, vs2, vs1, vm`|Vector-vector|vmax_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmax.vx`|`vd, vs2, rs1, vm`|vector-scalar|vmax_vx_counter|vint_instr, vcomputation_instr|

### Vector Single-Width Integer Multiply Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vmul.vv`|`vd, vs2, vs1, vm`|Vector-vector|vmul_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmul.vx`|`vd, vs2, rs1, vm`|vector-scalar|vmul_vx_counter|vint_instr, vcomputation_instr|
|☑|`vmulh.vv`|`vd, vs2, vs1, vm`|Vector-vector|vmulh_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmulh.vx`|`vd, vs2, rs1, vm`|vector-scalar|vmulh_vx_counter|vint_instr, vcomputation_instr|
|☑|`vmulhu.vv`|`vd, vs2, vs1, vm`|Vector-vector|vmulhu_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmulhu.vx`|`vd, vs2, rs1, vm`|vector-scalar|vmulhu_vx_counter|vint_instr, vcomputation_instr|
|☑|`vmulhsu.vv`|`vd, vs2, vs1, vm`|Vector-vector|vmulhsu_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmulhsu.vx`|`vd, vs2, rs1, vm`|vector-scalar|vmulhsu_vx_counter|vint_instr, vcomputation_instr|

### Vector Integer Divide Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vdivu.vv`|`vd, vs2, vs1, vm`|Vector-vector|vdivu_vv_counter|vint_instr, vcomputation_instr|
|☑|`vdivu.vx`|`vd, vs2, rs1, vm`|vector-scalar|vdivu_vx_counter|vint_instr, vcomputation_instr|
|☑|`vremu.vv`|`vd, vs2, vs1, vm`|Vector-vector|vremu_vv_counter|vint_instr, vcomputation_instr|
|☑|`vremu.vx`|`vd, vs2, rs1, vm`|vector-scalar|vremu_vx_counter|vint_instr, vcomputation_instr|
|☑|`vdiv.vv`|`vd, vs2, vs1, vm`|Vector-vector|vdiv_vv_counter|vint_instr, vcomputation_instr|
|☑|`vdiv.vx`|`vd, vs2, rs1, vm`|vector-scalar|vdiv_vx_counter|vint_instr, vcomputation_instr|
|☑|`vrem.vv`|`vd, vs2, vs1, vm`|Vector-vector|vrem_vv_counter|vint_instr, vcomputation_instr|
|☑|`vrem.vx`|`vd, vs2, rs1, vm`|vector-scalar|vrem_vx_counter|vint_instr, vcomputation_instr|

### Vector Widening Integer Multiply Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vwmulu.vv`|`vd, vs2, vs1, vm`|vector-vector|vwmulu_vv_counter|vint_instr, vwidening_instr|
|☑|`vwmulu.vx`|`vd, vs2, rs1, vm`|vector-scalar|vwmulu_vx_counter|vint_instr, vwidening_instr|
|☑|`vwmulsu.vv`|`vd, vs2, vs1, vm`|vector-vector|vwmulsu_vv_counter|vint_instr, vwidening_instr|
|☑|`vwmulsu.vx`|`vd, vs2, rs1, vm`|vector-scalar|vwmulsu_vx_counter|vint_instr, vwidening_instr|
|☑|`vwmul.vv`|`vd, vs2, vs1, vm`|vector-vector|vwmul_vv_counter|vint_instr, vwidening_instr|
|☑|`vwmul.vx`|`vd, vs2, rs1, vm`|vector-scalar|vwmul_vx_counter|vint_instr, vwidening_instr|

### Vector Single-Width Integer Multiply-Add Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vmacc.vv`|`vd, vs1, vs2, vm`|vd[i] = +(vs1[i] * vs2[i]) + vd[i]|vmacc_vv_counter|vint_instr, vcomputation_instr, vfused_instr|
|☑|`vmacc.vx`|`vd, rs1, vs2, vm`|vd[i] = +(x[rs1] * vs2[i]) + vd[i]|vmacc_vx_counter|vint_instr, vcomputation_instr, vfused_instr|
|☑|`vnmsac.vv`|`vd, vs1, vs2, vm`|vd[i] = -(vs1[i] * vs2[i]) + vd[i]|vnmsac_vv_counter|vint_instr, vcomputation_instr, vfused_instr|
|☑|`vnmsac.vx`|`vd, rs1, vs2, vm`|vd[i] = -(x[rs1] * vs2[i]) + vd[i]|vnmsac_vx_counter|vint_instr, vcomputation_instr, vfused_instr|
|☑|`vmadd.vv`|`vd, vs1, vs2, vm`|vd[i] = (vs1[i] * vd[i]) + vs2[i]|vmadd_vv_counter|vint_instr, vcomputation_instr, vfused_instr|
|☑|`vmadd.vx`|`vd, rs1, vs2, vm`|vd[i] = (x[rs1] * vd[i]) + vs2[i]|vmadd_vx_counter|vint_instr, vcomputation_instr, vfused_instr|
|☑|`vnmsub.vv`|`vd, vs1, vs2, vm`|vd[i] = -(vs1[i] * vd[i]) + vs2[i]|vnmsub_vv_counter|vint_instr, vcomputation_instr, vfused_instr|
|☑|`vnmsub.vx`|`vd, rs1, vs2, vm`|vd[i] = -(x[rs1] * vd[i]) + vs2[i]|vnmsub_vx_counter|vint_instr, vcomputation_instr, vfused_instr|

### Vector Widening Integer Multiply-Add Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vwmaccu.vv`|`vd, vs1, vs2, vm`|vd[i] = +(vs1[i] * vs2[i]) + vd[i]|vwmaccu_vv_counter|vint_instr, vwidening_instr, vwfused_instr|
|☑|`vwmaccu.vx`|`vd, rs1, vs2, vm`|vd[i] = +(x[rs1] * vs2[i]) + vd[i]|vwmaccu_vx_counter|vint_instr, vwidening_instr, vwfused_instr|
|☑|`vwmacc.vv`|`vd, vs1, vs2, vm`|vd[i] = +(vs1[i] * vs2[i]) + vd[i]|vwmacc_vv_counter|vint_instr, vwidening_instr, vwfused_instr|
|☑|`vwmacc.vx`|`vd, rs1, vs2, vm`|vd[i] = +(x[rs1] * vs2[i]) + vd[i]|vwmacc_vx_counter|vint_instr, vwidening_instr, vwfused_instr|
|☑|`vwmaccsu.vv`|`vd, vs1, vs2, vm`|vd[i] = +(signed(vs1[i]) * unsigned(vs2[i])) + vd[i]|vwmaccsu_vv_counter|vint_instr, vwidening_instr, vwfused_instr|
|☑|`vwmaccsu.vx`|`vd, rs1, vs2, vm`|vd[i] = +(signed(x[rs1]) * unsigned(vs2[i])) + vd[i]|vwmaccsu_vx_counter|vint_instr, vwidening_instr, vwfused_instr|
|☑|`vwmaccus.vx`|`vd, rs1, vs2, vm`|vd[i] = +(unsigned(x[rs1]) * signed(vs2[i])) + vd[i]|vwmaccus_vx_counter|vint_instr, vwidening_instr, vwfused_instr|

### Vector Integer Merge Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vmerge.vvm`|`vd, vs2, vs1, v0`|vd[i] = v0.mask[i] ? vs1[i] : vs2[i]|vmerge_vvm_counter|vint_instr, vcomputation_instr|
|☑|`vmerge.vxm`|`vd, vs2, rs1, v0`|vd[i] = v0.mask[i] ? x[rs1] : vs2[i]|vmerge_vxm_counter|vint_instr, vcomputation_instr|
|☑|`vmerge.vim`|`vd, vs2, imm, v0`|vd[i] = v0.mask[i] ? imm : vs2[i]|vmerge_vim_counter|vint_instr, vcomputation_instr|

### Vector Integer Move Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vmv.v.v`|`vd, vs1`|vd[i] = vs1[i]|vmv_v_v_counter|vint_instr, vmove_instr|
|☑|`vmv.v.x`|`vd, rs1`|vd[i] = x[rs1]|vmv_v_x_counter|vint_instr, vmove_instr|
|☑|`vmv.v.i`|`vd, imm`|vd[i] = imm|vmv_v_i_counter|vint_instr, vmove_instr|

## Vector Fixed-Point Arithmetic Instructions
### Vector Single-Width Saturating Add and Subtract
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vsaddu.vv`|`vd, vs2, vs1, vm`|Vector-vector|vsaddu_vv_counter|vint_instr, vcomputation_instr|
|☑|`vsaddu.vx`|`vd, vs2, rs1, vm`|vector-scalar|vsaddu_vx_counter|vint_instr, vcomputation_instr|
|☑|`vsaddu.vi`|`vd, vs2, imm, vm`|vector-immediate|vsaddu_vi_counter|vint_instr, vcomputation_instr|
|☑|`vsadd.vv`|`vd, vs2, vs1, vm`|Vector-vector|vsadd_vv_counter|vint_instr, vcomputation_instr|
|☑|`vsadd.vx`|`vd, vs2, rs1, vm`|vector-scalar|vsadd_vx_counter|vint_instr, vcomputation_instr|
|☑|`vsadd.vi`|`vd, vs2, imm, vm`|vector-immediate|vsadd_vi_counter|vint_instr, vcomputation_instr|
|☑|`vssubu.vv`|`vd, vs2, vs1, vm`|Vector-vector|vssubu_vv_counter|vint_instr, vcomputation_instr|
|☑|`vssubu.vx`|`vd, vs2, rs1, vm`|vector-scalar|vssubu_vx_counter|vint_instr, vcomputation_instr|
|☑|`vssub.vv`|`vd, vs2, vs1, vm`|Vector-vector|vssub_vv_counter|vint_instr, vcomputation_instr|
|☑|`vssub.vx`|`vd, vs2, rs1, vm`|vector-scalar|vssub_vx_counter|vint_instr, vcomputation_instr|

### Vector Single-Width Averaging Add and Subtract
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vaaddu.vv`|`vd, vs2, vs1, vm`|roundoff_unsigned(vs2[i] + vs1[i], 1)|vaaddu_vv_counter|vint_instr, vcomputation_instr|
|☑|`vaaddu.vx`|`vd, vs2, rs1, vm`|roundoff_unsigned(vs2[i] + x[rs1], 1)|vaaddu_vx_counter|vint_instr, vcomputation_instr|
|☑|`vaadd.vv`|`vd, vs2, vs1, vm`|roundoff_signed(vs2[i] + vs1[i], 1)|vaadd_vv_counter|vint_instr, vcomputation_instr|
|☑|`vaadd.vx`|`vd, vs2, rs1, vm`|roundoff_signed(vs2[i] + x[rs1], 1)|vaadd_vx_counter|vint_instr, vcomputation_instr|
|☑|`vasubu.vv`|`vd, vs2, vs1, vm`|roundoff_unsigned(vs2[i] - vs1[i], 1)|vasubu_vv_counter|vint_instr, vcomputation_instr|
|☑|`vasubu.vx`|`vd, vs2, rs1, vm`|roundoff_unsigned(vs2[i] - x[rs1], 1)|vasubu_vx_counter|vint_instr, vcomputation_instr|
|☑|`vasub.vv`|`vd, vs2, vs1, vm`|roundoff_signed(vs2[i] - vs1[i], 1)|vasub_vv_counter|vint_instr, vcomputation_instr|
|☑|`vasub.vx`|`vd, vs2, rs1, vm`|roundoff_signed(vs2[i] - x[rs1], 1)|vasub_vx_counter|vint_instr, vcomputation_instr|

### Vector Single-Width Fractional Multiply with Rounding and Saturation
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vsmul.vv`|`vd, vs2, vs1, vm`|vd[i] = clip(roundoff_signed(vs2[i]*vs1[i], SEW-1))|vsmul_vv_counter|vint_instr, vcomputation_instr|
|☑|`vsmul.vx`|`vd, vs2, rs1, vm`|vd[i] = clip(roundoff_signed(vs2[i]*x[rs1], SEW-1))|vsmul_vx_counter|vint_instr, vcomputation_instr|

### Vector Single-Width Scaling Shift Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vssrl.vv`|`vd, vs2, vs1, vm`|vd[i] = roundoff_unsigned(vs2[i], vs1[i])|vssrl_vv_counter|vint_instr, vcomputation_instr|
|☑|`vssrl.vx`|`vd, vs2, rs1, vm`|vd[i] = roundoff_unsigned(vs2[i], x[rs1])|vssrl_vx_counter|vint_instr, vcomputation_instr|
|☑|`vssrl.vi`|`vd, vs2, uimm, vm`|vd[i] = roundoff_unsigned(vs2[i], uimm)|vssrl_vi_counter|vint_instr, vcomputation_instr|
|☑|`vssra.vv`|`vd, vs2, vs1, vm`|vd[i] = roundoff_signed(vs2[i],vs1[i])|vssra_vv_counter|vint_instr, vcomputation_instr|
|☑|`vssra.vx`|`vd, vs2, rs1, vm`|vd[i] = roundoff_signed(vs2[i], x[rs1])|vssra_vx_counter|vint_instr, vcomputation_instr|
|☑|`vssra.vi`|`vd, vs2, uimm, vm`|vd[i] = roundoff_signed(vs2[i], uimm)|vssra_vi_counter|vint_instr, vcomputation_instr|

### Vector Narrowing Fixed-Point Clip Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vnclipu.wv`|`vd, vs2, vs1, vm`|vd[i] = clip(roundoff_unsigned(vs2[i], vs1[i]))|vnclipu_wv_counter|vint_instr, vnarrowing_instr|
|☑|`vnclipu.wx`|`vd, vs2, rs1, vm`|vd[i] = clip(roundoff_unsigned(vs2[i], x[rs1]))|vnclipu_wx_counter|vint_instr, vnarrowing_instr|
|☑|`vnclipu.wi`|`vd, vs2, uimm, vm`|vd[i] = clip(roundoff_unsigned(vs2[i], uimm))|vnclipu_wi_counter|vint_instr, vnarrowing_instr|
|☑|`vnclip.wv`|`vd, vs2, vs1, vm`|vd[i] = clip(roundoff_signed(vs2[i], vs1[i]))|vnclip_wv_counter|vint_instr, vnarrowing_instr|
|☑|`vnclip.wx`|`vd, vs2, rs1, vm`|vd[i] = clip(roundoff_signed(vs2[i], x[rs1]))|vnclip_wx_counter|vint_instr, vnarrowing_instr|
|☑|`vnclip.wi`|`vd, vs2, uimm, vm`|vd[i] = clip(roundoff_signed(vs2[i], uimm))|vnclip_wi_counter|vint_instr, vnarrowing_instr|

## Vector Floating-Point Instructions
### Vector Single-Width Floating-Point Add/Subtract Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfadd.vv`|`vd, vs2, vs1, vm`|Vector-vector|vfadd_vv_counter|vfp_instr, vcomputation_instr|
|☑|`vfadd.vf`|`vd, vs2, rs1, vm`|vector-scalar|vfadd_vf_counter|vfp_instr, vcomputation_instr|
|☑|`vfsub.vv`|`vd, vs2, vs1, vm`|Vector-vector|vfsub_vv_counter|vfp_instr, vcomputation_instr|
|☑|`vfsub.vf`|`vd, vs2, rs1, vm`|Vector-scalar vd[i] = vs2[i] - f[rs1]|vfsub_vf_counter|vfp_instr, vcomputation_instr|
|☑|`vfrsub.vf`|`vd, vs2, rs1, vm`|Scalar-vector vd[i] = f[rs1] - vs2[i]|vfrsub_vf_counter|vfp_instr, vcomputation_instr|

### Vector Widening Floating-Point Add/Subtract Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfwadd.vv`|`vd, vs2, vs1, vm`|vector-vector|vfwadd_vv_counter|vfp_instr, vwidening_instr|
|☑|`vfwadd.vf`|`vd, vs2, rs1, vm`|vector-scalar|vfwadd_vf_counter|vfp_instr, vwidening_instr|
|☑|`vfwadd.wv`|`vd, vs2, vs1, vm`|vector-vector|vfwadd_wv_counter|vfp_instr, vwidening_instr|
|☑|`vfwadd.wf`|`vd, vs2, rs1, vm`|vector-scalar|vfwadd_wf_counter|vfp_instr, vwidening_instr|
|☑|`vfwsub.vv`|`vd, vs2, vs1, vm`|vector-vector|vfwsub_vv_counter|vfp_instr, vwidening_instr|
|☑|`vfwsub.vf`|`vd, vs2, rs1, vm`|vector-scalar|vfwsub_vf_counter|vfp_instr, vwidening_instr|
|☑|`vfwsub.wv`|`vd, vs2, vs1, vm`|vector-vector|vfwsub_wv_counter|vfp_instr, vwidening_instr|
|☑|`vfwsub.wf`|`vd, vs2, rs1, vm`|vector-scalar|vfwsub_wf_counter|vfp_instr, vwidening_instr|

### Vector Single-Width Floating-Point Multiply/Divide Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfmul.vv`|`vd, vs2, vs1, vm`|Vector-vector|vfmul_vv_counter|vfp_instr, vcomputation_instr|
|☑|`vfmul.vf`|`vd, vs2, rs1, vm`|vector-scalar|vfmul_vf_counter|vfp_instr, vcomputation_instr|
|☑|`vfdiv.vv`|`vd, vs2, vs1, vm`|Vector-vector|vfdiv_vv_counter|vfp_instr, vcomputation_instr|
|☑|`vfdiv.vf`|`vd, vs2, rs1, vm`|vector-scalar|vfdiv_vf_counter|vfp_instr, vcomputation_instr|
|☑|`vfrdiv.vf`|`vd, vs2, rs1, vm`|scalar-vector, vd[i] = f[rs1]/vs2[i]|vfrdiv_vf_counter|vfp_instr, vcomputation_instr|

### Vector Widening Floating-Point Multiply
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfwmul.vv`|`vd, vs2, vs1, vm`|vector-vector|vfwmul_vv_counter|vfp_instr, vwidening_instr|
|☑|`vfwmul.vf`|`vd, vs2, rs1, vm`|vector-scalar|vfwmul_vf_counter|vfp_instr, vwidening_instr|

### Vector Single-Width Floating-Point Fused Multiply-Add Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfmacc.vv`|`vd, vs1, vs2, vm`|vd[i] = +(vs1[i] * vs2[i]) + vd[i]|vfmacc_vv_counter|vfp_instr, vcomputation_instr, vfused_instr|
|☑|`vfmacc.vf`|`vd, rs1, vs2, vm`|vd[i] = +(f[rs1] * vs2[i]) + vd[i]|vfmacc_vf_counter|vfp_instr, vcomputation_instr, vfused_instr|
|☑|`vfnmacc.vv`|`vd, vs1, vs2, vm`|vd[i] = -(vs1[i] * vs2[i]) - vd[i]|vfnmacc_vv_counter|vfp_instr, vcomputation_instr, vfused_instr|
|☑|`vfnmacc.vf`|`vd, rs1, vs2, vm`|vd[i] = -(f[rs1] * vs2[i]) - vd[i]|vfnmacc_vf_counter|vfp_instr, vcomputation_instr, vfused_instr|
|☑|`vfmsac.vv`|`vd, vs1, vs2, vm`|vd[i] = +(vs1[i] * vs2[i]) - vd[i]|vfmsac_vv_counter|vfp_instr, vcomputation_instr, vfused_instr|
|☑|`vfmsac.vf`|`vd, rs1, vs2, vm`|vd[i] = +(f[rs1] * vs2[i]) - vd[i]|vfmsac_vf_counter|vfp_instr, vcomputation_instr, vfused_instr|
|☑|`vfnmsac.vv`|`vd, vs1, vs2, vm`|vd[i] = -(vs1[i] * vs2[i]) + vd[i]|vfnmsac_vv_counter|vfp_instr, vcomputation_instr, vfused_instr|
|☑|`vfnmsac.vf`|`vd, rs1, vs2, vm`|vd[i] = -(f[rs1] * vs2[i]) + vd[i]|vfnmsac_vf_counter|vfp_instr, vcomputation_instr, vfused_instr|
|☑|`vfmadd.vv`|`vd, vs1, vs2, vm`|vd[i] = +(vs1[i] * vd[i]) + vs2[i]|vfmadd_vv_counter|vfp_instr, vcomputation_instr, vfused_instr|
|☑|`vfmadd.vf`|`vd, rs1, vs2, vm`|vd[i] = +(f[rs1] * vd[i]) + vs2[i]|vfmadd_vf_counter|vfp_instr, vcomputation_instr, vfused_instr|
|☑|`vfnmadd.vv`|`vd, vs1, vs2, vm`|vd[i] = -(vs1[i] * vd[i]) - vs2[i]|vfnmadd_vv_counter|vfp_instr, vcomputation_instr, vfused_instr|
|☑|`vfnmadd.vf`|`vd, rs1, vs2, vm`|vd[i] = -(f[rs1] * vd[i]) - vs2[i]|vfnmadd_vf_counter|vfp_instr, vcomputation_instr, vfused_instr|
|☑|`vfmsub.vv`|`vd, vs1, vs2, vm`|vd[i] = +(vs1[i] * vd[i]) - vs2[i]|vfmsub_vv_counter|vfp_instr, vcomputation_instr, vfused_instr|
|☑|`vfmsub.vf`|`vd, rs1, vs2, vm`|vd[i] = +(f[rs1] * vd[i]) - vs2[i]|vfmsub_vf_counter|vfp_instr, vcomputation_instr, vfused_instr|
|☑|`vfnmsub.vv`|`vd, vs1, vs2, vm`|vd[i] = -(vs1[i] * vd[i]) + vs2[i]|vfnmsub_vv_counter|vfp_instr, vcomputation_instr, vfused_instr|
|☑|`vfnmsub.vf`|`vd, rs1, vs2, vm`|vd[i] = -(f[rs1] * vd[i]) + vs2[i]|vfnmsub_vf_counter|vfp_instr, vcomputation_instr, vfused_instr|

### Vector Widening Floating-Point Fused Multiply-Add Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfwmacc.vv`|`vd, vs1, vs2, vm`|vd[i] = +(vs1[i] * vs2[i]) + vd[i]|vfwmacc_vv_counter|vfp_instr, vwidening_instr, vwfused_instr|
|☑|`vfwmacc.vf`|`vd, rs1, vs2, vm`|vd[i] = +(f[rs1] * vs2[i]) + vd[i]|vfwmacc_vf_counter|vfp_instr, vwidening_instr, vwfused_instr|
|☑|`vfwnmacc.vv`|`vd, vs1, vs2, vm`|vd[i] = -(vs1[i] * vs2[i]) - vd[i]|vfwnmacc_vv_counter|vfp_instr, vwidening_instr, vwfused_instr|
|☑|`vfwnmacc.vf`|`vd, rs1, vs2, vm`|vd[i] = -(f[rs1] * vs2[i]) - vd[i]|vfwnmacc_vf_counter|vfp_instr, vwidening_instr, vwfused_instr|
|☑|`vfwmsac.vv`|`vd, vs1, vs2, vm`|vd[i] = +(vs1[i] * vs2[i]) - vd[i]|vfwmsac_vv_counter|vfp_instr, vwidening_instr, vwfused_instr|
|☑|`vfwmsac.vf`|`vd, rs1, vs2, vm`|vd[i] = +(f[rs1] * vs2[i]) - vd[i]|vfwmsac_vf_counter|vfp_instr, vwidening_instr, vwfused_instr|
|☑|`vfwnmsac.vv`|`vd, vs1, vs2, vm`|vd[i] = -(vs1[i] * vs2[i]) + vd[i]|vfwnmsac_vv_counter|vfp_instr, vwidening_instr, vwfused_instr|
|☑|`vfwnmsac.vf`|`vd, rs1, vs2, vm`|vd[i] = -(f[rs1] * vs2[i]) + vd[i]|vfwnmsac_vf_counter|vfp_instr, vwidening_instr, vwfused_instr|

### Vector Floating-Point Square-Root Instruction
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfsqrt.v`|`vd, vs2, vm`|Vector-vector square root|vfsqrt_v_counter|vfp_instr, vcomputation_instr|

### Vector Floating-Point Reciprocal Square-Root Estimate Instruction
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfrsqrt7.v`|`vd, vs2, vm`|7-bit reciprocal square-root estimate|vfrsqrt7_v_counter|vfp_instr, vcomputation_instr|

### Vector Floating-Point Reciprocal Estimate Instruction
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfrec7.v`|`vd, vs2, vm`|7-bit reciprocal estimate|vfrec7_v_counter|vfp_instr, vcomputation_instr|

### Vector Floating-Point MIN/MAX Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfmin.vv`|`vd, vs2, vs1, vm`|Vector-vector|vfmin_vv_counter|vfp_instr, vcomputation_instr|
|☑|`vfmin.vf`|`vd, vs2, rs1, vm`|vector-scalar|vfmin_vf_counter|vfp_instr, vcomputation_instr|
|☑|`vfmax.vv`|`vd, vs2, vs1, vm`|Vector-vector|vfmax_vv_counter|vfp_instr, vcomputation_instr|
|☑|`vfmax.vf`|`vd, vs2, rs1, vm`|vector-scalar|vfmax_vf_counter|vfp_instr, vcomputation_instr|

### Vector Floating-Point Sign-Injection Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfsgnj.vv`|`vd, vs2, vs1, vm`|Vector-vector|vfsgnj_vv_counter|vfp_instr, vcomputation_instr|
|☑|`vfsgnj.vf`|`vd, vs2, rs1, vm`|vector-scalar|vfsgnj_vf_counter|vfp_instr, vcomputation_instr|
|☑|`vfsgnjn.vv`|`vd, vs2, vs1, vm`|Vector-vector|vfsgnjn_vv_counter|vfp_instr, vcomputation_instr|
|☑|`vfsgnjn.vf`|`vd, vs2, rs1, vm`|vector-scalar|vfsgnjn_vf_counter|vfp_instr, vcomputation_instr|
|☑|`vfsgnjx.vv`|`vd, vs2, vs1, vm`|Vector-vector|vfsgnjx_vv_counter|vfp_instr, vcomputation_instr|
|☑|`vfsgnjx.vf`|`vd, vs2, rs1, vm`|vector-scalar|vfsgnjx_vf_counter|vfp_instr, vcomputation_instr|

### Vector Floating-Point Compare Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vmfeq.vv`|`vd, vs2, vs1, vm`|Vector-vector|vmfeq_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmfeq.vf`|`vd, vs2, rs1, vm`|vector-scalar|vmfeq_vf_counter|vint_instr, vcomputation_instr|
|☑|`vmfne.vv`|`vd, vs2, vs1, vm`|Vector-vector|vmfne_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmfne.vf`|`vd, vs2, rs1, vm`|vector-scalar|vmfne_vf_counter|vint_instr, vcomputation_instr|
|☑|`vmflt.vv`|`vd, vs2, vs1, vm`|Vector-vector|vmflt_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmflt.vf`|`vd, vs2, rs1, vm`|vector-scalar|vmflt_vf_counter|vint_instr, vcomputation_instr|
|☑|`vmfle.vv`|`vd, vs2, vs1, vm`|Vector-vector|vmfle_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmfle.vf`|`vd, vs2, rs1, vm`|vector-scalar|vmfle_vf_counter|vint_instr, vcomputation_instr|
|☑|`vmfgt.vf`|`vd, vs2, rs1, vm`|vector-scalar|vmfgt_vf_counter|vint_instr, vcomputation_instr|
|☑|`vmfge.vf`|`vd, vs2, rs1, vm`|vector-scalar|vmfge_vf_counter|vint_instr, vcomputation_instr|

### Vector Floating-Point Classify Instruction
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfclass.v`|`vd, vs2, vm`|Vector-vector|vfclass_v_counter|vfp_instr, vcomputation_instr|

### Vector Floating-Point Merge Instruction
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfmerge.vfm`|`vd, vs2, rs1, v0`|vd[i] = v0.mask[i] ? f[rs1] : vs2[i]|vfmerge_vfm_counter|vfp_instr, vcomputation_instr|

### Vector Floating-Point Move Instruction
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfmv.v.f`|`vd, rs1`|vd[i] = f[rs1]|vfmv_v_f_counter|vfp_instr, vmove_instr|

### Single-Width Floating-Point/Integer Type-Convert Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfcvt.xu.f.v`|`vd, vs2, vm`|Convert float to unsigned integer.|vfcvt_xu_f_v_counter|vfp_instr, vcomputation_instr|
|☑|`vfcvt.x.f.v`|`vd, vs2, vm`|Convert float to signed integer.|vfcvt_x_f_v_counter|vfp_instr, vcomputation_instr|
|☑|`vfcvt.f.xu.v`|`vd, vs2, vm`|Convert unsigned integer to float.|vfcvt_f_xu_v_counter|vfp_instr, vcomputation_instr|
|☑|`vfcvt.f.x.v`|`vd, vs2, vm`|Convert signed integer to float.|vfcvt_f_x_v_counter|vfp_instr, vcomputation_instr|
|☑|`vfcvt.rtz.xu.f.v`|`vd, vs2, vm`|Convert float to unsigned integer, truncating.|vfcvt_rtz_xu_f_v_counter|vfp_instr, vcomputation_instr|
|☑|`vfcvt.rtz.x.f.v`|`vd, vs2, vm`|Convert float to signed integer, truncating.|vfcvt_rtz_x_f_v_counter|vfp_instr, vcomputation_instr|

### Widening Floating-Point/Integer Type-Convert Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfwcvt.xu.f.v`|`vd, vs2, vm`|Convert float to double-width unsigned integer.|vfwcvt_xu_f_v_counter|vfp_instr, vwidening_instr|
|☑|`vfwcvt.x.f.v`|`vd, vs2, vm`|Convert float to double-width signed integer.|vfwcvt_x_f_v_counter|vfp_instr, vwidening_instr|
|☑|`vfwcvt.f.xu.v`|`vd, vs2, vm`|Convert unsigned integer to double-width float.|vfwcvt_f_xu_v_counter|vfp_instr, vwidening_instr|
|☑|`vfwcvt.f.x.v`|`vd, vs2, vm`|Convert signed integer to double-width float.|vfwcvt_f_x_v_counter|vfp_instr, vwidening_instr|
|☑|`vfwcvt.f.f.v`|`vd, vs2, vm`|Convert single-width float to double-width float.|vfwcvt_f_f_v_counter|vfp_instr, vwidening_instr|
|☑|`vfwcvt.rtz.xu.f.v`|`vd, vs2, vm`|Convert float to double-width unsigned integer, truncating.|vfwcvt_rtz_xu_f_v_counter|vfp_instr, vwidening_instr|
|☑|`vfwcvt.rtz.x.f.v`|`vd, vs2, vm`|Convert float to double-width signed integer, truncating.|vfwcvt_rtz_x_f_v_counter|vfp_instr, vwidening_instr|

### Narrowing Floating-Point/Integer Type-Convert Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfncvt.xu.f.w`|`vd, vs2, vm`|Convert double-width float to unsigned integer.|vfncvt_xu_f_w_counter|vfp_instr, vnarrowing_instr|
|☑|`vfncvt.x.f.w`|`vd, vs2, vm`|Convert double-width float to signed integer.|vfncvt_x_f_w_counter|vfp_instr, vnarrowing_instr|
|☑|`vfncvt.f.xu.w`|`vd, vs2, vm`|Convert double-width unsigned integer to float.|vfncvt_f_xu_w_counter|vfp_instr, vnarrowing_instr|
|☑|`vfncvt.f.x.w`|`vd, vs2, vm`|Convert double-width signed integer to float.|vfncvt_f_x_w_counter|vfp_instr, vnarrowing_instr|
|☑|`vfncvt.f.f.w`|`vd, vs2, vm`|Convert double-width float to single-width float.|vfncvt_f_f_w_counter|vfp_instr, vnarrowing_instr|
|☑|`vfncvt.rod.f.f.w`|`vd, vs2, vm`|Convert double-width float to single-width float, rounding towards odd.|vfncvt_rod_f_f_w_counter|vfp_instr, vnarrowing_instr|
|☑|`vfncvt.rtz.xu.f.w`|`vd, vs2, vm`|Convert double-width float to unsigned integer, truncating.|vfncvt_rtz_xu_f_w_counter|vfp_instr, vnarrowing_instr|
|☑|`vfncvt.rtz.x.f.w`|`vd, vs2, vm`|Convert double-width float to signed integer, truncating.|vfncvt_rtz_x_f_w_counter|vfp_instr, vnarrowing_instr|

## Vector Reduction Operations
### Vector Single-Width Integer Reduction Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vredsum.vs`|`vd, vs2, vs1, vm`|vd[0] = sum( vs1[0] , vs2[*] )|vredsum_vs_counter|vint_instr, vint_reductions_n|
|☑|`vredand.vs`|`vd, vs2, vs1, vm`|vd[0] = and( vs1[0] , vs2[*] )|vredand_vs_counter|vint_instr, vint_reductions_n|
|☑|`vredor.vs`|`vd, vs2, vs1, vm`|vd[0] = or( vs1[0] , vs2[*] )|vredor_vs_counter|vint_instr, vint_reductions_n|
|☑|`vredxor.vs`|`vd, vs2, vs1, vm`|vd[0] = xor( vs1[0] , vs2[*] )|vredxor_vs_counter|vint_instr, vint_reductions_n|
|☑|`vredminu.vs`|`vd, vs2, vs1, vm`|vd[0] = minu( vs1[0] , vs2[*] )|vredminu_vs_counter|vint_instr, vint_reductions_n|
|☑|`vredmin.vs`|`vd, vs2, vs1, vm`|vd[0] = min( vs1[0] , vs2[*] )|vredmin_vs_counter|vint_instr, vint_reductions_n|
|☑|`vredmaxu.vs`|`vd, vs2, vs1, vm`|vd[0] = maxu( vs1[0] , vs2[*] )|vredmaxu_vs_counter|vint_instr, vint_reductions_n|
|☑|`vredmax.vs`|`vd, vs2, vs1, vm`|vd[0] = max( vs1[0] , vs2[*] )|vredmax_vs_counter|vint_instr, vint_reductions_n|

### Vector Widening Integer Reduction Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vwredsumu.vs`|`vd, vs2, vs1, vm`|2*SEW = 2*SEW + sum(zero-extend(SEW))|vwredsumu_vs_counter|vint_instr, vwidening_instr, vint_reductions|
|☑|`vwredsum.vs`|`vd, vs2, vs1, vm`|2*SEW = 2*SEW + sum(sign-extend(SEW))|vwredsum_vs_counter|vint_instr, vwidening_instr, vint_reductions|

### Vector Single-Width Floating-Point Reduction Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfredusum.vs`|`vd, vs2, vs1, vm`|Unordered sum|vfredusum_vs_counter|vfp_instr, vfp_reductions_n|
|☑|`vfredosum.vs`|`vd, vs2, vs1, vm`|Ordered sum|vfredosum_vs_counter|vfp_instr, vfp_reductions_n|
|☑|`vfredmin.vs`|`vd, vs2, vs1, vm`|Minimum value|vfredmin_vs_counter|vfp_instr, vfp_reductions_n|
|☑|`vfredmax.vs`|`vd, vs2, vs1, vm`|Maximum value|vfredmax_vs_counter|vfp_instr, vfp_reductions_n|

### Vector Widening Floating-Point Reduction Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfwredusum.vs`|`vd, vs2, vs1, vm`|Unordered sum|vfwredusum_vs_counter|vfp_instr, vwidening_instr, vfp_reductions|
|☑|`vfwredosum.vs`|`vd, vs2, vs1, vm`|Ordered sum|vfwredosum_vs_counter|vfp_instr, vwidening_instr, vfp_reductions|

## Vector Mask Instructions
### Vector Mask-Register Logical Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vmand.mm`|`vd, vs2, vs1`|vd.mask[i] = vs2.mask[i] && vs1.mask[i]|vmand_mm_counter|vint_instr, vcomputation_instr|
|☑|`vmnand.mm`|`vd, vs2, vs1`|vd.mask[i] = !(vs2.mask[i] && vs1.mask[i])|vmnand_mm_counter|vint_instr, vcomputation_instr|
|☑|`vmandn.mm`|`vd, vs2, vs1`|vd.mask[i] = vs2.mask[i] && !vs1.mask[i]|vmandn_mm_counter|vint_instr, vcomputation_instr|
|☑|`vmxor.mm`|`vd, vs2, vs1`|vd.mask[i] = vs2.mask[i] ^^ vs1.mask[i]|vmxor_mm_counter|vint_instr, vcomputation_instr|
|☑|`vmor.mm`|`vd, vs2, vs1`|vd.mask[i] = vs2.mask[i] \|\| vs1.mask[i]|vmor_mm_counter|vint_instr, vcomputation_instr|
|☑|`vmnor.mm`|`vd, vs2, vs1`|vd.mask[i] = !(vs2.mask[i] \|\| vs1.mask[i])|vmnor_mm_counter|vint_instr, vcomputation_instr|
|☑|`vmorn.mm`|`vd, vs2, vs1`|vd.mask[i] = vs2.mask[i] \|\| !vs1.mask[i]|vmorn_mm_counter|vint_instr, vcomputation_instr|
|☑|`vmxnor.mm`|`vd, vs2, vs1`|vd.mask[i] = !(vs2.mask[i] ^^ vs1.mask[i])|vmxnor_mm_counter|vint_instr, vcomputation_instr|

### Vector count population in mask vcpop.m
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vcpop.m`|`rd, vs2, vm`|x[rd] = sum_i ( vs2.mask[i] && v0.mask[i] )|vcpop_m_counter|vint_instr, vmask_instr, inst_v_s|

### vfirst find-first-set mask bit
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfirst.m`|`rd, vs2, vm`|index of the first set bit in the mask|vfirst_m_counter|vint_instr, vmask_instr, inst_v_s|

### vmsbf.m set-before-first mask bit
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vmsbf.m`|`vd, vs2, vm`|set mask bits before the first set bit|vmsbf_m_counter|vint_instr, vcomputation_instr|

### vmsif.m set-including-first mask bit
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vmsif.m`|`vd, vs2, vm`|set mask bits up to and including the first set bit|vmsif_m_counter|vint_instr, vcomputation_instr|

### vmsof.m set-only-first mask bit
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vmsof.m`|`vd, vs2, vm`|set only the first set bit|vmsof_m_counter|vint_instr, vcomputation_instr|

### Vector Iota Instruction
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`viota.m`|`vd, vs2, vm`|prefix sum of the mask bits|viota_m_counter|vint_instr, vcomputation_instr|

### Vector Element Index Instruction
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vid.v`|`vd, vm`|Write element ID to destination.|vid_v_counter|vint_instr, vcomputation_instr|

## Vector Permutation Instructions
### Integer Scalar Move Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vmv.x.s`|`rd, vs2`|x[rd] = vs2[0] (vs1=0)|vmv_x_s_counter|vint_instr, vmove_instr, m_inst_v_s|
|☑|`vmv.s.x`|`vd, rs1`|vd[0] = x[rs1] (vs2=0)|vmv_s_x_counter|vint_instr, vmove_instr|

### Floating-Point Scalar Move Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vfmv.f.s`|`rd, vs2`|f[rd] = vs2[0] (rs1=0)|vfmv_f_s_counter|vfp_instr, vmove_instr, m_inst_v_s|
|☑|`vfmv.s.f`|`vd, rs1`|vd[0] = f[rs1] (vs2=0)|vfmv_s_f_counter|vfp_instr, vmove_instr|

### Vector Slide Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vslideup.vx`|`vd, vs2, rs1, vm`|vd[i+rs1] = vs2[i]|vslideup_vx_counter|vint_instr, vslideup_instr|
|☑|`vslideup.vi`|`vd, vs2, uimm, vm`|vd[i+uimm] = vs2[i]|vslideup_vi_counter|vint_instr, vslideup_instr|
|☑|`vslidedown.vx`|`vd, vs2, rs1, vm`|vd[i] = vs2[i+rs1]|vslidedown_vx_counter|vint_instr, vslidedown_instr|
|☑|`vslidedown.vi`|`vd, vs2, uimm, vm`|vd[i] = vs2[i+uimm]|vslidedown_vi_counter|vint_instr, vslidedown_instr|
|☑|`vslide1up.vx`|`vd, vs2, rs1, vm`|vd[0]=x[rs1], vd[i+1] = vs2[i]|vslide1up_vx_counter|vint_instr, vslide1up_instr|
|☑|`vfslide1up.vf`|`vd, vs2, rs1, vm`|vd[0]=f[rs1], vd[i+1] = vs2[i]|vfslide1up_vf_counter|vfp_instr, vslide1up_instr|
|☑|`vslide1down.vx`|`vd, vs2, rs1, vm`|vd[i] = vs2[i+1], vd[vl-1]=x[rs1]|vslide1down_vx_counter|vint_instr, vslide1down_instr|
|☑|`vfslide1down.vf`|`vd, vs2, rs1, vm`|vd[i] = vs2[i+1], vd[vl-1]=f[rs1]|vfslide1down_vf_counter|vfp_instr, vslide1down_instr|

### Vector Register Gather Instructions
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vrgather.vv`|`vd, vs2, vs1, vm`|vd[i] = (vs1[i] >= VLMAX) ? 0 : vs2[vs1[i]];|vrgather_vv_counter|vint_instr, vgath_instr|
|☑|`vrgather.vx`|`vd, vs2, rs1, vm`|vd[i] = (x[rs1] >= VLMAX) ? 0 : vs2[x[rs1]]|vrgather_vx_counter|vint_instr, vgath_instr|
|☑|`vrgather.vi`|`vd, vs2, uimm, vm`|vd[i] = (uimm >= VLMAX) ? 0 : vs2[uimm]|vrgather_vi_counter|vint_instr, vgath_instr|
|☑|`vrgatherei16.vv`|`vd, vs2, vs1, vm`|vd[i] = (vs1[i] >= VLMAX) ? 0 : vs2[vs1[i]];|vrgatherei16_vv_counter|vint_instr, vgath_instr|

### Vector Compress Instruction
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vcompress.vm`|`vd, vs2, vs1`|Compress into vd elements of vs2 where vs1 is enabled|vcompress_vm_counter|vint_instr, vcmprss_instr|

### Whole Vector Register Move
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vmv1r.v`|`vd, vs2`|copy 1 whole vector register|vmv1r_v_counter|vint_instr, vmove_instr, vmove_wh_instr|
|☑|`vmv2r.v`|`vd, vs2`|copy 2 whole vector registers|vmv2r_v_counter|vint_instr, vmove_instr, vmove_wh_instr|
|☑|`vmv4r.v`|`vd, vs2`|copy 4 whole vector registers|vmv4r_v_counter|vint_instr, vmove_instr, vmove_wh_instr|
|☑|`vmv8r.v`|`vd, vs2`|copy 8 whole vector registers|vmv8r_v_counter|vint_instr, vmove_instr, vmove_wh_instr|

## Alias y pseudo-instrucciones
### Pseudo-instrucciones aritméticas y lógicas
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vneg.v`|`vd, vs`|= vrsub.vx vd, vs, x0|vneg_v_counter|vint_instr, vcomputation_instr|
|☑|`vwcvt.x.x.v`|`vd, vs, vm`|= vwadd.vx vd, vs, x0, vm|vwcvt_x_x_v_counter|vint_instr, vwidening_instr|
|☑|`vwcvtu.x.x.v`|`vd, vs, vm`|= vwaddu.vx vd, vs, x0, vm|vwcvtu_x_x_v_counter|vint_instr, vwidening_instr|
|☑|`vnot.v`|`vd, vs, vm`|= vxor.vi vd, vs, -1, vm|vnot_v_counter|vint_instr, vcomputation_instr|
|☑|`vncvt.x.x.w`|`vd, vs, vm`|= vnsrl.wx vd, vs, x0, vm|vncvt_x_x_w_counter|vint_instr, vnarrowing_instr|
|☑|`vfneg.v`|`vd, vs`|= vfsgnjn.vv vd, vs, vs|vfneg_v_counter|vfp_instr, vcomputation_instr|
|☑|`vfabs.v`|`vd, vs`|= vfsgnjx.vv vd, vs, vs|vfabs_v_counter|vfp_instr, vcomputation_instr|

### Pseudo-instrucciones de comparación entera
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vmsgt.vv`|`vd, va, vb, vm`|= vmslt.vv vd, vb, va, vm|vmsgt_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmsgtu.vv`|`vd, va, vb, vm`|= vmsltu.vv vd, vb, va, vm|vmsgtu_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmsge.vv`|`vd, va, vb, vm`|= vmsle.vv vd, vb, va, vm|vmsge_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmsgeu.vv`|`vd, va, vb, vm`|= vmsleu.vv vd, vb, va, vm|vmsgeu_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmslt.vi`|`vd, va, i, vm`|= vmsle.vi vd, va, i-1, vm|vmslt_vi_counter|vint_instr, vcomputation_instr|
|☑|`vmsltu.vi`|`vd, va, i, vm`|= vmsleu.vi vd, va, i-1, vm|vmsltu_vi_counter|vint_instr, vcomputation_instr|
|☑|`vmsge.vi`|`vd, va, i, vm`|= vmsgt.vi vd, va, i-1, vm|vmsge_vi_counter|vint_instr, vcomputation_instr|
|☑|`vmsgeu.vi`|`vd, va, i, vm`|= vmsgtu.vi vd, va, i-1, vm|vmsgeu_vi_counter|vint_instr, vcomputation_instr|
|☑|`vmsge.vx`|`vd, va, x, vm`|pseudoinstruction, expanded with vmslt.vx plus mask logic|vmsge_vx_counter|vint_instr, vcomputation_instr|
|☑|`vmsgeu.vx`|`vd, va, x, vm`|pseudoinstruction, unsigned version of vmsge.vx|vmsgeu_vx_counter|vint_instr, vcomputation_instr|

### Pseudo-instrucciones de comparación FP
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vmfgt.vv`|`vd, va, vb, vm`|= vmflt.vv vd, vb, va, vm|vmfgt_vv_counter|vint_instr, vcomputation_instr|
|☑|`vmfge.vv`|`vd, va, vb, vm`|= vmfle.vv vd, vb, va, vm|vmfge_vv_counter|vint_instr, vcomputation_instr|

### Pseudo-instrucciones de lógica de máscaras
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vmmv.m`|`vd, vs`|= vmand.mm vd, vs, vs|vmmv_m_counter|vint_instr, vcomputation_instr|
|☑|`vmclr.m`|`vd`|= vmxor.mm vd, vd, vd|vmclr_m_counter|vint_instr, vcomputation_instr|
|☑|`vmset.m`|`vd`|= vmxnor.mm vd, vd, vd|vmset_m_counter|vint_instr, vcomputation_instr|
|☑|`vmnot.m`|`vd, vs`|= vmnand.mm vd, vs, vs|vmnot_m_counter|vint_instr, vcomputation_instr|

### Alias de compatibilidad conservados por la especificación
|☑☐☒|Instruction|Operands|Description|Counter|Aggregate|
|---|---|---|---|---|---|
|☑|`vpopc.m`|`rd, vs2, vm`|assembler alias of vcpop.m|vpopc_m_counter|vint_instr, vmask_instr, inst_v_s|
|☑|`vmandnot.mm`|`vd, vs2, vs1`|assembler alias of vmandn.mm|vmandnot_mm_counter|vint_instr, vcomputation_instr|
|☑|`vmornot.mm`|`vd, vs2, vs1`|assembler alias of vmorn.mm|vmornot_mm_counter|vint_instr, vcomputation_instr|
|☑|`vmcpy.m`|`vd, vs`|assembler alias of vmmv.m|vmcpy_m_counter|vint_instr, vcomputation_instr|
|☑|`vl1r.v`|`vd, (rs1)`|pseudoinstruction equal to vl1re8.v|vl1r_v_counter|vspill_instr|
|☑|`vl2r.v`|`vd, (rs1)`|pseudoinstruction equal to vl2re8.v|vl2r_v_counter|vspill_instr|
|☑|`vl4r.v`|`vd, (rs1)`|pseudoinstruction equal to vl4re8.v|vl4r_v_counter|vspill_instr|
|☑|`vl8r.v`|`vd, (rs1)`|pseudoinstruction equal to vl8re8.v|vl8r_v_counter|vspill_instr|
