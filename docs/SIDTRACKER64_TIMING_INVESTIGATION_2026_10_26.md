# SIDTracker64 / SIDPLAY64MIX — investigación de temporización (26/10/2026)

**No existe todavía identificación inequívoca por firma de SIDTracker64.**
El contenedor PSID no codifica el nombre del editor de manera estándar.

## Evidencia extraída del D64 SIPLAY.d64 usado en TEST02C

Los 20 SID del D64 (sin contar el propio ejecutable SIDPLAY64-SD2IEC)
comparten este perfil:

- Magic: `PSID`; versión 2, offset de datos `$007C`.
- Dirección de carga: `$1000` (incluida en los primeros dos bytes del payload).
- INIT: `$1000`; PLAY: `$1003`.
- Una subtune.
- Flags: `$0024` => PAL y modelo SID 8580 recomendado.
- Máximo payload: 6.435 B; todos caben en la ventana experimental de 8 KB.
- **17 temas**: speed bits `$FFFFFFFF`; subtune 1 solicita IRQ CIA
  (default 60 Hz según la especificación PSID).
- **3 temas**: speed bits `$00000000`; subtune 1 solicita IRQ VBI
  (~50 Hz en PAL): `CARA`, `PERROCULO`, `INDIECITO 50`.

Observación importante: el speed word PSID **no expresa un valor arbitrario
de Hz**. Indica principalmente VBI o CIA por subtune. Al exportar música
con velocidad interna variable desde SIDTracker64, puede requerirse
inspeccionar el propio código de INIT/PLAY y medir la cadencia en VICE.

Un valor `$FFFFFFFF` con una sola subtune deja bits sobrantes a 1.
Eso no es una firma inequívoca del editor y no alcanza para concluir
que todos los temas están pensados para 60 Hz exactos.

Los PSID de este D64 no demuestran por sí solos que el audio acelerado
del TEST02C se deba **solo** al timer. Si el driver modifica `$DC04/$DC05`
o ejecuta varios pasos internos por PLAY, hay que identificarlo.

## TEST02D — 50% SOLO en llamadas de PLAY

Base conservada: **TEST02C, usuario confirmó PASS (A→B→C)**.

`tests/test02d_half_playrate.tas` es un motor de prueba autónomo y
no reemplaza `sidplay64.tas`. Modificación funcional única:

```asm
    lda play_divider
    eor #$01
    sta play_divider
    beq sid_skip_play
    jsr sid_play
sid_skip_play
```

- El **IRQ CIA físico sigue a ~60 Hz** (latch `$4025`).
- `sid_play` se llama **a ~30 Hz**: 50% del TEST02C.
- El contador de límite de cada canción sigue contando IRQ CIA
  y su umbral sigue siendo 600 IRQ (unos 10 s).
- KrillLoad no se vuelve más lento por cambiar el período de la CIA.
- El divisor se resetea después de cada cambio para mantener la
  primera llamada PLAY al comenzar el SID nuevo.
- No hay cambios en el constructor D64 ni en el loader.
- No promover a `master` sin validación auditiva en VICE.

## Dirección correcta para la integración final

SIDPLAY64 original sí usa los bits de velocidad por subtune y distingue
PAL/NTSC en `doheaderstuff.tas`, `dotunenumbers.tas` y `restartTune`.
Mantener ese contrato en producción. El 50% es un **modo diagnóstico**
que permite distinguir fácilmente IRQ / disco / handoff; no es el modo
definitivo de reproducción de SidTracker64.

## Validación pendiente

1. Usuario prueba D64 TEST02D en VICE y confirma carga A→B→C.
2. Comparar velocidad musical TEST02C vs TEST02D; si esta vez se oye
   comprensible, investigar nivel de tick esperado de SidTracker64.
3. En un SID concreto, observar `$DC04/$DC05/$DC0E` después de INIT y
   contar invocaciones reales de PLAY por segundo en el monitor VICE.
4. Separar recursos de Krill de ZP y de otros I/O antes de integrar
   en SIDPLAY64; el test fijo no demuestra compatibilidad PSID general.
5. Incorporar trigger `plt_advance` sin modificar el timer Glenn.

## Referencias

- SIDPLAY64MIX `src/doheaderstuff.tas` (flags, velocidad y direcciones);
  `src/dotunenumbers.tas` (speed bit por subtune);
  `sidplay64.tas` (reloj CIA PAL/NTSC).
- `docs/SID_file_format.txt` del repositorio Glenn.
- `https://github.com/c64scene-ar/chipdisk-nac-vol.1`:
  documentación de timers CIA, con advertencia explícita acerca de
  velocidad no estándar de SidTracker64.
- App Store de SidTracker64 (rango 25–240 Hz anunciado).
