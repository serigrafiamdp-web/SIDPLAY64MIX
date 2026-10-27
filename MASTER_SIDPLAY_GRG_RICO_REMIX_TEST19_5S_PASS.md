# MASTER SIDPLAY GRG - RICO REMIX — TEST19 (VICE PASS)

**Fecha:** 27 de octubre de 2026  
**Estado:** **PASS informado por el usuario** en VICE. No confundir con el resultado de la compilacion: la prueba real del reproductor es el hito de aceptacion.

## Base que debemos preservar
- SIDPLAY64 **original de Glenn Rune Gallefoss**, con su propia interfaz, directorio, reloj, timer, controles y reproductor SID.
- **KrillLoad y simbionte** conectados al reproductor original.
- **Version MULTIARCHIVO**, ultimo punto recuperado con precarga funcionando, despues de fallar las pruebas que intentaron meter todo en un solo PRG (TEST16, TEST17 y TEST18). **No repetir esas pruebas sobre este MASTER.**
- **Precarga de la siguiente cancion desde los 5 segundos** de la reproduccion, usando CIA1 TOD segundos: `LDA $DC09 / CMP #$05`. Opera mientras hay musica tanto en Manual (M) como en Next (N).
- El comienzo de la precarga a 00:05 es **independiente** del temporizador original de Glenn para el final de la cancion. No se modifico el vencimiento de su timer.
- Directorio de esta imagen: 38 PRG: **19 archivos .SID originales**, 13 stage `MIX_*`, y seis ejecutables/auxiliares: `BOOT`, `SYMBIONT`, `INSTA`, `RESIDENT`, `GLENN`, `FIX`.
- El modulo `FIX` es parte funcional del arranque e integracion. No eliminarlo sin adaptar el cargador.
- **Seleccion manual RETURN** y avance Next: usar la version TEST19 aprobada como referencia, no atribuirle validaciones que aun no se hayan probado en cada SID.
- Sigue siendo un trabajo abierto convertir toda la solucion a **1 PRG + 19 SID** conservando la precarga: se intento y fallo. Posible futuro archivo de playlist con duracion por SID: **solo propuesta, NO implementado**.

## Imagen D64 aprobada
```
TEST19_MULTIPLES_ARCHIVOS_KRILL_5_SEGUNDOS.d64
Tamaño: 174848 bytes
SHA256: b247f58ce9d3df87025d0f09ca145998bffe31e8f9e520c5c29dcfc238d66cc5
```

Esta imagen es EXACTAMENTE el `TEST13_13_SIDS_RETURN_FIX.d64` aprobado anteriormente, excepto por **dos bytes** en el archivo `FIX` que convierten la precarga de 01:00 a 00:05:
- Offset fisico 0x2928F: 0A -> 09 (registro de minutos $DC0A a segundos $DC09).
- Offset fisico 0x29292: 01 -> 05 (BCD 01 a BCD 05).
- Base TEST13 SHA256: `ecb884ca6fb125c34b644b540c677d61fb70d621bb7c0c52e4749376dadac58e`.
- Los otros 36 ficheros en la imagen y el resto de FIX no cambiaron.

La rama Git contiene el **codigo fuente de Glenn+Krill en modo 5 segundos**, mas `tests/reproducir_master_test19.py` para reproducir byte a byte el D64 desde la imagen TEST13 conocida. **El binario D64 aprobado se distribuyo en la conversacion, no se afirma que este archivado como objeto binario en el repositorio**.

## Para retomar en otro chat
**Primera instruccion recomendada:** 
> Continuemos desde el MASTER SIDPLAY GRG - RICO REMIX TEST19, 27/10/2026, branch `MASTER-SIDPLAY-GRG-RICO-REMIX-TEST19-5S-27OCT2026`, D64 SHA256 `b247f58ce9d3df87025d0f09ca145998bffe31e8f9e520c5c29dcfc238d66cc5`. Es un PASS real del reproductor original Glenn con varios archivos y Krill precargando a los 5 segundos en cualquier modo. No tocar este master. Seguimos en una rama nueva para integrar los auxiliares en un PRG sin perder la precarga, y mejorar el recorrido completo del directorio.

**Reglas:** No renombrar `main` de proyectos que dependan de ese nombre; no modificar los checkpoints PASS; mantener Glenn GUI/IRQ/timer, y validar siempre el D64 completo en VICE antes de otorgar PASS.
