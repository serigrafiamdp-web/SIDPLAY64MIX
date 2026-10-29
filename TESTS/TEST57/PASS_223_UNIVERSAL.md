# MASTER TEST57 — 223 SIDs PASS UNIVERSAL

**Fecha:** 2026-10-28 / 29, confirmación VICE explícita del usuario: **«pass»**. Esta rama queda congelada.

## Recuento

- Base universal: `MASTER-TEST56-213SID-UNIVERSAL-HIGH-PASS` — 213 SID acumulados.
- TEST57: 10 nuevos originales PSID con LOAD `$0FF0–$0FFE`, varios prefijos de 2–16 bytes preservados sin modificar SID.
- **Total universal confirmado: 223 SID** entre diferentes D81 usando una misma línea de ONEFILE.
- TEST55 aislado: otros 6 SID probados en variante con simbionte desplazado a $8000, que sigue siendo **incompatible** con la familia original de $8000-$8BFF; **no sumarlos a los 223 del universal**.

## Prueba validada

Archivo `TEST57_10_NUEVOS_Y_REGRESIONES_UNIVERSALES.d81`: 819200 bytes, SHA256 `27153b9e7235c41a4f91365a983328ebbb60f8802882fcf2dd0546c27da6f842`, un ONEFILE y 16 SID.

Nuevos SID probados: `illusion.sid` ($0FF0), `enigmaintro.sid` ($0FF1), `maddrummer.sid` ($0FF2), `allthatshe.sid` ($0FF4), `journey.sid` ($0FF6), `22years.sid` ($0FF8), `hiphouse.sid` ($0FFA), `chase.sid` ($0FFC), `bomberboy.sid` ($0FFD), `palanut.sid` ($0FFE).

Regresiones de familias anteriores en el mismo D81: `capriphol.sid` ($1000), `lethalweapon.sid` ($0FFF), `montyrun.sid` ($8000), `hawkeye.sid` ($7AE0, 9 KB), `danko.sid` ($2000), `vortex.sid` ($E008).

## Modificación

Guardado del prefijo de 2–16 bytes originales que ocupan $0FF0–$0FFF, transferencia normal del resto a $1000–$2FFF y restauración exacta del prefijo antes de invocar INIT. El tratamiento antiguo de LOAD $0FFF (TEST46) permanece intacto. Krill sigue activo en $3C00, el simbionte universal en $3000–$3BFF; prefetch/NEXT y selector sin cambios.

La auditoría previa de `MUSICIANS.zip` (56.568 SID) halló **1.499 candidatos estructurales** en la nueva subfamilia. No confundir con 1.499 pruebas de audio confirmadas: esta tanda añadió únicamente 10 PASS.

Compilación GitHub Actions: run `40808517835`, SUCCESS tras corregir saltos 6502 fuera de rango.

**Próximos cambios:** trabajar en ramas experimentales basadas en este MASTER; integrar solo familias que coexistan en el mismo reproductor y no destruyan compatibilidad anterior. Mantener todos los MASTER anteriores y `PASS-TEST55-6SID-3000-3BFF-ISOLATED` separados.
