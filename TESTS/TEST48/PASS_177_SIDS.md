# MASTER TEST48 — 177 SID compatibles acumulados — PASS informado

Fecha: 2026-10-28.
Congelado desde `test/test48-basic-rom-a000`, después de que el usuario recibió los D81 experimentales TEST48 y contestó **"pass"**.

## Resultado

- MASTER TEST47: 164 SIDs originales compatibles, verificados en varios discos de pruebas.
- TEST48: **13 SID nuevos** con LOAD dentro de RAM bajo ROM BASIC `$A000–$BFFF`, confirmados por el usuario en la prueba VICE.
- **Total acumulado: 177 SID compatibles**, NO 177 archivos juntos en un único D81: el selector sigue limitado a una biblioteca de hasta 162 canciones validada.

SIDs nuevos TEST48: `arkpandora.sid`, `bumpspike.sid`, `cosmonut.sid`, `cybernoid.sid`, `cybernoidii.sid`, `doubledens.sid`, `hunterpatrol.sid`, `intkarate.sid`, `kentilla.sid`, `nibbly92.sid`, `oceanload3.sid`, `starpaws.sid`, `thinktwice3.sid`.

## Implementación y restricciones

- Reconocimiento genérico LOAD original `$A000–$BFFF` e INIT/PLAY originales en su RAM subyacente; dirección virtual en staging `$5000–$6FFF`, transferencia final real a `$A000–$BFFF`.
- Carga Krill / ONEFILE / vectores originales conservados, ningún SID original alterado.
- Mantener `cool tune` y `and again` fuera de la biblioteca.
- Archivos SID en minúsculas, SIN numeración; ejecutable `00player.prg` conservado.
- `test48_basic_rom_13_nuevos.d81`: 13 nuevos + 1 pista de referencia.
- `test48_biblioteca_162_sids.d81`: 143 primeros + seis TEST47 + 13 TEST48.
- Usuario reportó PASS. No implica que los 177 estén montados simultáneamente, ni que se haya probado hardware físico.

**Próximo objetivo acordado:** seguir intentando recuperar SIDs difíciles agrupando incompatibilidades. Solo cuando ya no se puedan recuperar más, ampliar el selector a su máxima capacidad en otro TEST; congelar este MASTER sin cambios.
