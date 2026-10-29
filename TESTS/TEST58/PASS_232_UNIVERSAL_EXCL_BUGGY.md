# MASTER TEST58 — 232 SIDs UNIVERSAL PASS (BUGGY.SID EXCLUDED)

**Fecha:** 2026-10-29. **Estado:** versión congelada tras prueba del usuario en VICE; no modificar directamente.

Se congeló desde la rama experimental `test/test58-4000-4fff-universal`, que deriva exclusivamente de `MASTER-TEST57-223SID-LOW-PREFIX-UNIVERSAL-PASS`.

## Resultado en VICE

El usuario confirmó que **el resto de las canciones funciona**, pero tuvo que **eliminar `BUGGY.SID`** del D81 por provocar un **JAM de CPU**. Archivo problemático: original `BUGGY.SID`, además entregó `BUGGY.SID.prg` para futura revisión. Por ahora, el usuario pidió **dejarlo de lado y seguir**. NO declarar BUGGY compatible; NO incluirlo en próximas imágenes de prueba ni como regresión.

**9 nuevos PASS originales en LOAD $4000–$4FFF:**
- `humanoid.sid`
- `weirdscience.sid`
- `inthemood.sid`
- `entering.sid`
- `techno.sid`
- `mazeman.sid`
- `musdemo.sid`
- `bestintro.sid`
- `rikroadie.sid`

**`buggy.sid` = FAIL (CPU JAM), EXCLUIDO.**

El disco de prueba también incorporó siete regresiones anteriormente PASS: `capriphol.sid`, `hawkeye.sid` (9 KB), `montyrun.sid` ($8000), `danko.sid` ($2000), `vortex.sid` ($E008), `lethalweapon.sid` ($0FFF) e `illusion.sid` ($0FF0). Fueron probados en el mismo ONEFILE sin reportarse fallos, tras retirar BUGGY.

## Recuento

**223 PASS anteriores + 9 nuevos PASS = 232 SIDs compatibles en la línea universal.**

Los seis PASS del TEST55 en versión experimental con simbionte en $8000 quedan aparte y NO son compatibles simultáneamente con familia $8000-$9FFF; no sumarlos al ONEFILE universal.

## Técnica de TEST58

- Nuevo tipo PSID original LOAD $4000-$4FFF, cuerpo finaliza como máximo en $5000, INIT/PLAY dentro de región, sin conversiones del archivo.
- Traslado temporal del staging de 9 KB de TEST52 desde $4000-$63FF a $5000-$73FF para que una canción $4000-$4FFF siga ejecutándose mientras se precarga la siguiente.
- Handoff de LOAD $4000/$4FFF, conservando Krill residente $3C00, simbionte $3000, selector y precarga de 5 segundos.
- El PASS experimental puede coexistir con otras familias de MASTER57; JAM de BUGGY no está resuelto.

CI GitHub Actions `40811358667`: éxito de compilación y verificaciones estáticas, sin sustituir PASS musical en VICE.

**Siguiente línea de desarrollo:** buscar nuevas familias que coexistan en el mismo ONEFILE. Mantener MASTER57 y MASTER58 inmutables, y excluir BUGGY de todas las pruebas hasta nuevo aviso.
