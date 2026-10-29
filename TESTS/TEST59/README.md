# TEST59 — Universal original SID LOAD $0F80–$0FEF

**Estado:** GitHub Actions CI de 64tass+PuCrunch **PASS**, run `40814507627`; D81 nativo verificado; **pendiente de PASS musical del usuario en VICE**. MASTER58 de **232 SID universal PASS** se conserva intacto. BUGGY.SID sigue excluido por JAM.

## Objetivo

En el ZIP original `MUSICIANS.zip` (56.568 archivos SID), **109 candidatos estructurales** cumplen condiciones de LOAD desde `$0F80` hasta `$0FEF`, PSID con cabecera estándar $007C, INIT posterior al LOAD, PLAY entre $1000 y $2FFF, cuerpo contenido hasta $2FFF; todos necesitan más de 16 bytes protegidos debajo de $1000. **No confundir 109 candidatos con reproducciones confirmadas.**

## Implementación experimental

- Extender la ruta original TEST57, que guardaba 2–16 bytes antes de $1000, a guardar **2–128 bytes** de las canciones que comienzan entre $0F80 y $0FFE.
- En prefetch, retener esos bytes originales en la memoria propia del simbionte mientras se copia el resto al staging universal $5000.
- **Corregir explícitamente la suma de 16 bits del origen $53CC + tamaño-prefijo**: si cruza $53FF, propagar acarreo al byte alto. Sin esto, los archivos $0F80-$0FCE se interpretarían incorrectamente.
- Antes de INIT, restaurar los bytes originales en $0F80–$0FFF con IRQ desactivadas.
- **Conservar intactas** las rutas de un solo byte $0FFF, $1000–$2FFF, TEST58 $4000–$4FFF, TEST52 9 KB (stage temporal $5000), $8000–$9FFF, $A000–$BFFF, $E000–$F7FF, Krill residente en $3C00, simbionte $3000–$3BFF, NEXT, temporizador cinco segundos y selector.
- El TEST55 que ocupaba $8000 queda fuera de esta línea, como siempre.

## Disco D81 para VICE

`TEST59_10_SIDS_0F80_REGRESION_UNIVERSAL.d81`:
- Tamaño: 819.200 bytes.
- SHA256 `cad4fa8d90de59c700f746694e7292602b33e1585caff54aa74c6439c30a2163`.
- ONEFILE `00player.prg` SHA256 `bfaac11797663c3bc98ed84da99c0b17b81530b1228c7b974d739e5deab52bc1`.
- 20 archivos: **1 ONEFILE, 10 nuevos SIDs originales, 9 regresiones PASS**.
- D81 BAM 80×40, 3 sectores de directorio, cadenas completas, nombres únicos en minúsculas <=16 caracteres y contenidos byte a byte comprobados. ZIP original preservado sin cambios.

Diez SID nuevos originales: `magnificent.sid` ($0F80), `chopper.sid` ($0F87), `pitfall.sid` ($0F88), `mrmonster.sid` ($0F94), `anthem.sid` ($0F9C), `aisledance.sid` ($0FAD), `tuneseven.sid` ($0FD0), `lightspeed.sid` ($0FE0), `vampireintro.sid` ($0FE5) y `aurum.sid` ($0FEB). Incluyen INIT debajo y encima de $1000, y subtunes múltiples sin múltiples chips.

Nueve regresiones previamente aprobadas: `capriphol.sid`, `humanoid.sid` ($4000), `hawkeye.sid` (9 KB), `montyrun.sid` ($8000), `danko.sid` ($2000), `vortex.sid` (alta), `lethalweapon.sid` ($0FFF), `illusion.sid` ($0FF0), `weirdscience.sid` ($4003). **BUGGY.SID no incluido**.

## Validación solicitada

Cargar el D81 en VICE, probar los 10 nuevos, selección manual y NEXT, incluyendo las transiciones `magnificent → humanoid → chopper → hawkeye`. Comprobar reproducción de las nueve referencias y prefetch. Si PASS completo, **242 SIDs compatibles en la línea universal (232+10)**, pero NO subir recuento antes de la confirmación del usuario. No crear nuevo MASTER sin PASS en VICE.
