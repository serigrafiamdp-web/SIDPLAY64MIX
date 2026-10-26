# TEST03B-2 — corrección de primera canción / Krill diferido

**Fecha:** 26 de octubre de 2026  
**Estado:** COMPILACIÓN PASS; ejecución/audio en VICE pendiente.  
**Base comprobada por usuario:** TEST03A interfaz + SID + timer PASS.  
**Versión anterior:** TEST03B-1 FAIL: pantalla negra al cargar la primera canción, sin LED.

## Diagnóstico

En B-1 se ejecutaba `jsr $6000` (instalación de Krill en la unidad)
desde `fileSelect`, **antes de que Glenn cargara siquiera el primer SID**.
Sin embargo, el `ROM_load` normal de SIDPLAY64 sigue siendo necesario.
Krill v184 sustituye el protocolo activo de la unidad, y su
documentación advierte que para ciertas operaciones KERNAL se requiere
desinstalar el cargador.

Fuente: https://csdb.dk/release/?id=189130&show=notes

## Cambios concretos

1. En el menú inicial se leen `INSTA` y `RESIDENT` mediante KERNAL,
   **sin ejecutar** el instalador `$6000`. El drive permanece en DOS.
2. El código original de Glenn carga un SID, ejecuta su INIT y recién
   entonces llama a `mix03_mark_playing`, marcando que realmente hay música.
   No confundimos la posición del cursor con la canción que suena.
3. Cuando el usuario activa **N** y realmente suena la pista de
   índice 1 o 2, se invoca el instalador Krill ya residente.
4. Una vez instalado, el sistema fuerza modo **M** antes de realizar
   la precarga, impidiendo una transición del timer por KERNAL mientras
   Krill sigue activo. Esto es deliberado: todavía NO hay handoff.
5. Se mantiene la preservación de ZP Krill `$C0-$D5` en la IRQ
   de Glenn mientras se ejecuta `loadraw`.
6. La velocidad musical y los 20 ficheros originales permanecen intactos.

## Cómo probar en VICE

**AVISO**: prueba de integración restringida a unidad 1541 emulada.
1. Activar True Drive Emulation. Reiniciar emulación/drive antes de arrancar
   el disco corregido si antes quedó otro fastloader instalado.
2. `LOAD "*",8,1` y `RUN`.
3. Seleccionar `MINIMERCADO.SID` y pulsar RETURN.
   **Debe cargar por KERNAL normalmente y comenzar a sonar con velocidad
   correcta**, independientemente de la precarga.
4. Con MINIMERCADO reproduciéndose, pasar de **M** a **N** usando la
   tecla de cambio de modo de SIDPLAY64.
5. Escuchar si el LED del drive trabaja **mientras la música continúa**.
   El mensaje visible debería progresar `S` (preparado) → `I`
   (Krill instalado) → `P` (STB precargado). `E` señala error.
6. **El modo vuelve a M intencionadamente**; no presionar RETURN para
   cambiar de canción tras P/I sin reiniciar el emulador. El driver
   todavía no sabe alternar con seguridad al banco precargado.
7. Si la primera música carga, pero Krill falla al activar N, anotar
   pantalla y color del borde, y si escuchó corte al instalar.

## PASS mínimo

- Reproducción normal de primer SID antes de habilitar Krill.
- Observación de `P` y LED durante reproducción para verificar carga
  de STB en `$5000`, sin bloquear la música.
- No confundirlo con PASS de avance automático. TEST03B-2 **no** lo
  pretende. Ese avance requiere el handoff de TEST03B-3 y tratamiento
  específico de los metadatos PSID.

## Seguridad de memoria

Auxiliar `$3000-$33ff`, carga alternativa `$5000-$6fff`,
instalador `$6000` (se sobrescribe después de usarlo), residente
`$9000`, ZP Krill `$C0-$D5`. NO apto para SID arbitrarios fuera de
la colección experimental.

## Compilación

CI: https://github.com/serigrafiamdp-web/SIDPLAY64MIX/actions/runs/40420313235
Compilación `64tass`, `pucrunch`: PASS.
Audio en VICE: pendiente.
