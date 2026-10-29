# TEST57 — Compatibilidad universal con LOAD $0FF0–$0FFE

**Estado:** compilación + controles estáticos PASS (GitHub Actions run `40808517835`); imagen D81 auditada; **pendiente de prueba de audio en VICE**. Rama derivada de `MASTER-TEST56-213SID-UNIVERSAL-HIGH-PASS`, que se mantiene congelado.

## Objetivo

La auditoría de `MUSICIANS.zip` detectó **1.499 candidatos** PSID con LOAD original entre `$0FF0` y `$0FFE`, cabecera estándar, un solo SID, tamaño y vectores admitidos, carga íntegra por debajo de `$3000`. No son 1.499 PASS. La nueva función completa el método de un byte para `$0FFF` del TEST46.

Cambio de arquitectura: guardar **2–16 bytes originales** del prefijo `$0FF0–$0FFF` en RAM del simbionte antes de copiar los siguientes 8 KB al buffer `$5000–$6FFF`; restaurarlos en su LOAD exacto, con interrupciones desactivadas, después de copiar la música a `$1000–$2FFF` y antes de invocar INIT. La validación de PLAY sigue exigiendo `$1000–$2FFF` y INIT válido posterior al comienzo real de los datos. Se conserva sin modificar el camino especial TEST46 `$0FFF`, así como todos los caminos del MASTER56: Krill en `$3C00`, simbionte en `$3000`, canciones $2000, $8000, $A000, $E000 y carga de 9 KB.

## Imagen D81 — prueba mixta de convivencia

Archivo: `TEST57_10_NUEVOS_Y_REGRESIONES_UNIVERSALES.d81`, tamaño **819.200 bytes**, SHA256 `27153b9e7235c41a4f91365a983328ebbb60f8802882fcf2dd0546c27da6f842`. **17 archivos (1 ONEFILE y 16 SID), tres sectores de directorio nativo**; BAM de 80 pistas, sectores encadenados, nombres, tamaños y la recuperación byte a byte de cada archivo verificados.

**Diez SIDs nuevos originales sin modificar** de `MUSICIANS.zip`:
- `illusion.sid` LOAD $0FF0
- `enigmaintro.sid` LOAD $0FF1
- `maddrummer.sid` LOAD $0FF2
- `allthatshe.sid` LOAD $0FF4
- `journey.sid` LOAD $0FF6
- `22years.sid` LOAD $0FF8 (INIT $1000, también prueba esta variante)
- `hiphouse.sid` LOAD $0FFA
- `chase.sid` LOAD $0FFC
- `bomberboy.sid` LOAD $0FFD
- `palanut.sid` LOAD $0FFE

**Seis referencias antiguas PASS**, copiadas byte a byte de los D81 confirmados por el usuario:
`capriphol.sid` ($1000), `lethalweapon.sid` ($0FFF, ruta TEST46), `montyrun.sid` ($8000, Krill TEST50), `hawkeye.sid` ($7AE0, 9 KB TEST52), `danko.sid` ($2000, TEST54), `vortex.sid` ($E008, TEST56).

Todos deben ejecutarse con exactamente el mismo `00player.prg` de TEST57; `00player.prg` fue compilado con 64tass y PuCrunch en CI. No ampliar selector todavía.

## Comprobaciones

La primera compilación falló **solo por saltos de 6502 fuera del alcance de branch** y se corrigió con un trampolín local `mix57_reject`. La compilación corregida **PASS**. Esto NO acredita reproducción musical: probar en VICE la referencia inicial, los diez nuevos, los seis anteriores, NEXT manual y la precarga de cinco segundos. Si todos PASS, elevar el nuevo MASTER universal a **223 SID** (213+10), sin sumar los seis del TEST55 aislado. Si FAIL, conservar MASTER56 y solicitar `r` + `m $3ff0 $3fff` del monitor.

El experimento TEST55 ($3000–$3BFF) continúa congelado e independiente y no forma parte de este ONEFILE. 
