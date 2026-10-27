# TEST05 — PASS EN VICE CONFIRMADO POR USUARIO

**Fecha:** 26/10/2026  
**Motor estable:** `milestone/test05-double-buffer-vice-pass-26oct2026`  
**Commit ejecutable exacto antes de esta nota:** `dac550bfff24fd20cd18ec34c983a02402d7f69b`  
**D64 probado:** `SIDPLAY64MIX_TEST05_DOBLE_BUFFER_KRILL.d64`  
**SHA-256 D64 entregado:** `0083b5ae769d57c4937260e113ed2a09ef54d9523100c2f35ea9d4715f4c765d`

## Validación de usuario: PASS

Tras recibir el TEST05 (motor autónomo derivado del TEST02C aprobado)
se solicitaron dos comprobaciones específicas:

1. **La reproducción de música continúa mientras KrillLoad realiza
   la lectura del siguiente SID a un banco libre.**
2. **La transición de canción 1 a canción 2 se realiza desde RAM,
   sin esperar a que la unidad de disco termine de leer.**

El usuario contestó **«pass»**, por lo que se considera superado
el **objetivo principal de funcionamiento concurrente y conmutación
sin espera de disco** en esta prueba.

En la versión suministrada, el programa pretende repetir el ciclo
MINIMERCADO → CHACABEZA → COMEME → MINIMERCADO. No se dispone de una
medición instrumental de latencia ni una confirmación específica
por separado de la tercera transición ni de la velocidad musical
exacta contra TEST03A. **No ampliar el alcance de PASS** a esos casos
sin nueva prueba.

## Qué contiene el ejecutable probado

- La primera canción se carga mediante KERNAL antes de arrancar.
- El instalador Krill reside en $6000 (transitorio), el cargador en
  $9000 y su Zero Page es $C0–$D5.
- Música activa en $1000, INIT $1000, PLAY $1003.
- Banco del siguiente SID cargado en $5000.
- Interrupción por CIA1 con salvado/restauración de Zero Page de Krill
  durante las llamadas PLAY; sin cambiar de CPU ni cargar KERNAL
  mientras el cargador está activo.
- Tras el umbral de timer, se copian 19 páginas desde el banco $5000
  hacia $1000, se ejecuta INIT y el siguiente SID empieza a reproducir.
- Al terminar la conmutación se activa la siguiente precarga.
- Cadencia de PLAY configurada aproximadamente 50 Hz PAL; **calibración
  audible exacta todavía pendiente**.
- UI original de Glenn Rune no está integrada en esta prueba.

## Qué NO se debe modificar en este hito

**Congelar esta versión como referencia reproducible.**
No editar `tests/test05_double_buffer_loop.tas` dentro de la rama
`milestone/test05-double-buffer-vice-pass-26oct2026`.
Cualquier integración posterior debe realizarse en una rama NUEVA,
y compararse con el TEST05 PASS (audio, IRQ, lectura y timer).

## Próxima fase

1. Validar repetición completa del ciclo B→C→A y velocidad real en VICE.
2. Mantener DOS/loader separados del directorio de SIDPLAY64.
3. Conectar el estado NEXT_READY y el timer gráfico de Glenn al switch
   desde RAM, sin reinstalar Krill durante la música.
4. No activar el avance N sobre un directorio incompleto ni intentar
   cargar con KERNAL después del takeover del drive.
5. Solo después: soporte de PSID con rangos, metadata y subtunes
   diferentes; fallback seguro si NEXT_READY no existe.

**MASTER NO MODIFICADO.** Los resultados fallidos TEST03B/C/D se
conservan para análisis pero no son nuevas bases de desarrollo.
