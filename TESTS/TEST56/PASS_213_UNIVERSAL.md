# MASTER TEST56 — PASS UNIVERSAL — 213 SIDs

**Fecha:** 28 octubre 2026. **Estado:** congelado tras PASS explícito del usuario en VICE.

Seis SID originales nuevos en la clase **LOAD $E001–$F7FF**: `vortex.sid`, `bruceleeii.sid`, `hurlingfruit.sid`, `dancingmoon.sid`, `defcom.sid`, `hurtinggrnd.sid`.

En el **mismo D81 y mismo ONEFILE**, regresión también PASS con `capriphol.sid` (bajo), `montyrun.sid` ($8000), `hawkeye.sid` (9 KB, $7AE0) y `danko.sid` ($2000). Imagen verificada: `TEST56_6_NUEVOS_Y_REGRESION_UNIVERSAL.d81`, SHA256 `2cfd7cc5e947e60fd3ddc75dfd12f14f66ec9ddbb669f103140064855b05177c`. CI `40795407246` PASS en compilación estática.

**Recuento universal confirmado: 207 previos + 6 nuevos = 213 SIDs**. El TEST55 tiene **otros seis PASS únicamente en una variante separada** con simbionte en $8000, incompatible con músicas $8000–$8BFF. No debe fusionarse ni contarse en un reproductor único: total entre variantes 219; universal actual 213.

Código de la variante universal: simbionte $3000–$3BFF; Krill activo $3C00; prefetch 5 s, NEXT, rutas $1000–$2FFF, $7A00–$7FFF 9 KB, $8000–$9FFF, $A000–$BFFF, $E000–$F7FF; nuevas cargas altas no alineadas usan shift TEST44/45 y tail guard TEST47. El MASTER anterior `MASTER-TEST54-207SID-2000-2FFF-PASS` permanece inalterado.

**Política de desarrollo:** nueva funcionalidad en rama de TEST independiente a partir del MASTER56. Priorizar familias que puedan funcionar todas en el MISMO reproductor, sin reubicaciones incompatibles; mantener el selector intacto hasta terminar compatibilidad.
