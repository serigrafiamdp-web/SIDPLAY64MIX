# TEST39 — SD2IEC (archivos SID sueltos, sin D64)

Estado: **COMPILACION PASS / SD2IEC REAL NO PROBADO**.

## Reproductor

`SIDPLAY64MIX.PRG` se compilo con **defset=4**, el modo SD2IEC del Glenn original y el symbiont Krill de TEST38. No se ha cambiado el mapa de memoria del SID ni las rutinas musicales, de precarga, de header, de portada o de la unidad. Los cambios funcionales de TEST39 son solo:

- El indice del siguiente SID se calcula respecto de `maxfile` (entradas reales), y vuelve de la ultima pista a la primera.
- ENTER comprueba `maxfile` en lugar de un valor fijo 20.
- Sigue activo el fastloader Krill original incrustado, por lo que el comportamiento en un firmware SD2IEC concreto **requiere prueba fisica**.

Glenn almacena hasta unas 163 entradas en el directorio; el primer archivo (indice 0) debe ser el lanzador y el resto exclusivamente SID. Esta primera prueba incluye 72 SID (73 entradas); la capacidad de la tarjeta FAT no limita el total de bytes de un D64.

## Construccion de la carpeta FAT para tarjeta SD

1. Crear una carpeta nueva `SIDPLAYMIX39` en la tarjeta SD.
2. **Primero** descomprimir `TEST39_LAUNCHER_SD2IEC.zip`, que contiene solo `00PLAYER.PRG`.
3. **Despues** descomprimir `TEST39_SD2IEC_72_SID_SUELTOS.zip`, que contiene 72 archivos `001_*.SID` a `072_*.SID` (se entrega en la conversacion de ChatGPT desde la galeria del usuario). No cargar un D64.
4. La carpeta debe contener **solamente** 73 archivos (1 PRG + 72 SID); ni .TXT, .ZIP, .D64 ni directorios adicionales.
5. Con SD2IEC en unidad 8 y posicionado en esa carpeta: `LOAD"00PLAYER.PRG",8,1` y `RUN`. Si el C64 BASIC no reconoce el nombre, revisar mediante `LOAD"$",8` y `LIST` o usar un browser de SD2IEC.
6. Verificar que Glenn enumere todos los archivos (monitor `m $3ff8 $3ffa`, esperar `$3FFA=$49` para 73 entradas), que la portada cambie y que NEXT, ENTER y wrap 72->1 funcionen sin cuelgues.

La galeria de 72 SID es PSID v2, LOAD/INIT $1000, PLAY $1003, cuerpo <= 6656 bytes. El contenido binario de cada SID es identico al de la galeria entregada por el usuario, los nombres son ASCII de 16 caracteres maximo para evitar colisiones de directorio.

## Compatibilidad Krill con SD2IEC

El firmware SD2IEC soporta variaciones de Krill's IRQ Loader con archivos FAT sueltos, pero nuestro instalador embebido deriva del MASTER TEST19 para 1541. Algunas configuraciones Krill requieren el modo KERNAL fallback y pueden ser mas lentas o no compatibles. Esta version **no afirma** que Krill haya pasado en un dispositivo SD2IEC especifico. No modificar ni reemplazar TEST35 ni el TEST38 que corrigio la portada.

Fuentes tecnicas: README de firmware SD2IEC (Krill's IRQ Loader); Krill v184 documentacion original.

## Pruebas para confirmar

- Arranque y conteo de 73 entradas en SD2IEC real.
- La primera seleccion por ENTER carga sin dañar la musica; comprobar dos seleccionadas de la mitad.
- NEXT hasta una entrada de indice 20+.
- Seleccion manual de la pista 72 y wrap automatico hacia la pista 1.
- Cinco segundos: comprobar luz de unidad, borde y continuidad musical.
- Portada: titulo/autor/fecha/nombre de archivo corresponden al SID en reproduccion.
- Fallo seguro si se intenta abrir un SID que no existe: documentar antes de automatizar.

Se recomienda probar primero una subcarpeta con 5 SID y el PRG (sin mezclar los antiguos), luego 72, para aislar problemas de Krill/firmware del parser de listas largas.
