# TEST03C — QUICKSTART + NEXT predeterminado (26 octubre 2026)

## Por qué este experimento

Reporte del usuario en VICE al intentar TEST03B-3:
- Queda en pantalla `Press 0-9 for colors. Any other key to continue.`.
- El drive permanece con luz encendida y no carga otra cosa.
- Se observa interferencia en el borde.

El anterior TEST03B-2 instaló Krill en la unidad; es posible que la
unidad siguiera con su código de protocolo después de reiniciar únicamente
el C64 (hipótesis, no demostrada). **Para repetir esta prueba salir de
VICE y volver a ejecutarlo**, restableciendo la unidad emulada 1541.

## Base elegida

Partimos de `test/test03-sidplay64-integracion` (TEST03A):
- Interfaz original **PASS en VICE por el usuario**.
- Canciones cargan a su velocidad original **PASS**.
- Timer cambia canciones **PASS**.
- KrillLoad NO estaba activado y no interfería con IRQ/KERNAL.

Se evita partir de TEST03B-2/B-3 para no mantener su cargador residual,
wrappers IRQ adicionales o código de takeover en el menú.

## Cambios

- `sidplay64.tas`: `def_attractmode=0` en rama de prueba.
- `src/init.tas`: luego de `setup_colors`, en build
  `DEF_MIX03=1`, saltar directamente a `trkinstd` (inicialización de
  música, vectores y directorio), sin requerir pulsar una tecla
  en el menú de color.
- `sidplay64.tas` (label `start`): inicializar `plt_flag=0` y
  `plt_letter='N'` conjuntamente, evitando visualización incoherente
  entre indicador y modo interno.
- No toca `src/irq.tas`. Sigue `jsr playmus` directo de Glenn.
- `src/mix03_timer_hook.tas` y `src/plt_function.tas` son las mismas
  versiones inertes para caché de TEST03A: siempre se hace carga original.
- **Sin Krill, sin precarga, sin handoff RAM** en este control de regresión.

## Resultado de compilación

- CI GitHub Actions: https://github.com/serigrafiamdp-web/SIDPLAY64MIX/actions/runs/40424776440 **SUCCESS**.
- Ambas variantes `DEF_MIX03=0` y `DEF_MIX03=1` compilan con 64tass.
- PuCrunch crea PRG ejecutable; encabezado BASIC idéntico al PASS.
- D64 174848 bytes; 21 entradas visibles; 20 SID verificados idénticos
  byte a byte contra `SIDPLAY64MIX_TEST03A_ORIGINAL_UI.d64`.
- Validación funcional de reproducción en VICE **pendiente**.

## Protocolo VICE

1. CERRAR VICE y volver a abrirlo para reiniciar **C64 y 1541**.
2. Montar `SIDPLAY64MIX_TEST03C_QUICKSTART_NEXT.d64`; activar
   True Drive Emulation.
3. Ejecutar `LOAD "*",8,1` seguido de `RUN`.
4. Debe abrir directamente el directorio, sin esperar la selección
   de colores. Indicador N visible.
5. Seleccionar MINIMERCADO.SID y pulsar RETURN. Audio correcto.
6. Esperar fin del timer (03:05 si no se modifica). El drive carga
   siguiente canción de modo tradicional, sin precarga.

## Regresión que buscamos descartar

- Que aparezca todavía la pantalla de color o se cuelgue el drive.
- Que N se visualice pero `plt_flag` quede como Manual.
- Que la reubicación de la UI, timer o canción deje de funcionar.

TEST03C no es PASS hasta recibir prueba real del usuario.
No fusionar a `master`.
