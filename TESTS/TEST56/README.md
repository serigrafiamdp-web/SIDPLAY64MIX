# TEST56 — PSID altos no alineados, en el MISMO ONEFILE universal

**Estado:** **PASS en VICE confirmado expresamente por el usuario**. Compilación GitHub Actions PASS; D81 verificado byte a byte. MASTER congelado, no modificar.

## Línea de referencia y objetivo

Esta rama deriva exclusivamente de `MASTER-TEST54-207SID-2000-2FFF-PASS`, que conserva sus **207 SIDs** confirmados en la línea universal. NO deriva de TEST55, cuyo simbionte fue trasladado a $8000 y que por ello no puede convivir con música que cargue en ese banco.

TEST56 conserva simbionte $3000–$3BFF y residente Krill $3C00–$3DEE, sin tocar selector, prefetch 5 segundos ni ONEFILE arquitectura. Solo incorpora PSID originales con LOAD entre $E001 y $F7FF que terminan antes de la fuente de caracteres $F800. Las direcciones INIT y PLAY deben estar dentro de la zona de carga y no antes del LOAD. Reutiliza desplazamiento por página y byte de TEST44/45 y protección de cola de TEST47, copiando a $E000–$F7FF sin modificar bytes originales.

**Estimación estática del ZIP MUSICIANS:** 127 archivos PSID originales de un solo chip, cabecera $007C, LOAD embebido, INIT/PLAY dentro del cuerpo, tamaño <=8192, LOAD en ($E000,$F800), fin <=$F800. No declarar 127 PASS: es potencial estructural.

## Un D81 combinado para probar convivencia

`TEST56_6_NUEVOS_Y_REGRESION_UNIVERSAL.d81` — **819.200 bytes**, SHA256 `2cfd7cc5e947e60fd3ddc75dfd12f14f66ec9ddbb669f103140064855b05177c`. 11 archivos y **10 SID**, directorio D81 de dos sectores: BAM, cadenas completas y extracción del contenido verificadas.

**ONEFILE** `00player.prg`, SHA256 `07ccf697f9593329eb10cd9052a4ec6045fe5ceee582253d78f695ad2946cba0`. Compilado con 64tass+PuCrunch desde esta rama, CI `40795407246`, SUCCESS (solo compilación y aserciones estáticas).

Contenidos:

| Archivo | Origen | LOAD | Fin exclusivo |
|---|---|---|---|
| `capriphol.sid` | referencia PASS memoria baja | según original | |
| `vortex.sid` | NUEVO Aviador Dro / Vortex | $E008 | $E69F |
| `bruceleeii.sid` | NUEVO Jonas Hulten / Bruce Lee II | $E081 | $ED10 |
| `hurlingfruit.sid` | NUEVO Rockin Limited / Hurling Frootmig | $E100 | $EFAA |
| `dancingmoon.sid` | NUEVO Gallefoss Glenn / Dancing in the Moonlight | $E8FF | $F6F3 |
| `defcom.sid` | NUEVO David Whittaker / Defcom | $E900 | $F789 |
| `hurtinggrnd.sid` | NUEVO Kim Andersen / Hurting the Ground | $F000 | $F7DA |
| `montyrun.sid` | referencia PASS $8000/$9000 Krill | $8000 | |
| `hawkeye.sid` | referencia PASS cuerpo 9 KB | $7AE0 | |
| `danko.sid` | referencia PASS $2000 | $2000 | $3000 |

Los 6 nuevos son originales de MUSICIANS.zip, originales sin conversión y distintos por hash de cuerpo musical de los SIDs en las pruebas anteriores. Los 4 de referencia fueron reutilizados byte a byte desde D81 que el usuario marcó PASS.

## Prueba de VICE realizada — PASS

El usuario probó el D81 combinado en VICE y confirmó **«pass»**. Esto confirma musicalmente las seis canciones nuevas y la convivencia con `capriphol`, `montyrun`, `hawkeye` y `danko` en **el mismo ejecutable**. La compilación estática por sí sola no habría sido prueba suficiente.

**213 SIDs compatibles confirmados acumulados en la línea universal** (207+6). TEST55 conserva 6 PASS en una variante aislada que aún no se integró y **no debe sumarse** a la compatibilidad de un solo ONEFILE. Hay 219 distintos confirmados entre las dos variantes, pero solo 213 en la universal.

Mantener `MASTER-TEST54-207SID-2000-2FFF-PASS` y esta rama `MASTER-TEST56-213SID-UNIVERSAL-HIGH-PASS` congelados. Toda mejora nueva debe partir de un MASTER en una rama de prueba. No ampliar selector todavía.
