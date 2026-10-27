# TEST06 — TIMER CIA TOD 10 SEG / 03:05, DOBLE BUFFER KRILL

**Estado:** 64tass y ensamblado CI, pendientes pruebas funcionales del usuario en VICE. **No afirmar PASS de runtime antes del usuario**.  
**Base congelada**: `milestone/test05-double-buffer-vice-pass-26oct2026`, SHA `dac550bfff24fd20cd18ec34c983a02402d7f69b`.  
**Master no modificado**.

## Objetivo

El usuario confirmó TEST05 PASS: los dos bancos permiten tocar SID activo
`$1000` mientras Krill v184 precarga en `$5000`; al cambiar se copian
19 páginas de RAM, sin esperar al disco.

TEST06 sustituye únicamente el **umbral fijo de 500 ticks de PLAY**
por un **timer de tiempo real independiente de la cadencia musical**,
usando el reloj Time-Of-Day (TOD) CIA1 de la 6526 en formato BCD.
Es el mismo tipo de base de reloj que muestra SIDPLAY64 de Glenn, pero
**NO es la interfaz ni las rutinas completas de Glenn**.

Dos variantes idénticas salvo el umbral:

- `TEST06_10S` compara BCD `00:10` (vuelta rápida).
- `TEST06_3M05` compara BCD `03:05` (límite original del ejemplo).

## Cambios aislados

- `tests/test06_tod_timer.tas` creado como copia exacta del
  `tests/test05_double_buffer_loop.tas` aprobado; solo modificaciones
  relacionadas con TOD e indicador tiempo.
- `arm_cia_irq` sigue usando Timer A latch `$4CC8` (~50.1 Hz
  en PAL). Solo bit 7 de CRA cambia de 0 a 1, para que TOD cuente
  alimentación de 50 Hz, conforme a la hoja de datos de MOS 6526.
- `reset_tod`: anula selector ALARM en CRB (`$DC0F=0`);
  escribe horas/minutos/segundos/décimas a cero en orden oficial.
- `draw_tod`: lee horas primero para latch, minutos/segundos,
  décimas al final para liberar latch; convierte dos BCD en pantalla.
- `await_timer` primero exige `next_ready=1`, luego espera que
  TOD haya llegado a 00:10 o 03:05 sin llamar al drive.
- Tras activar siguiente SID, se reinicia TOD y continúa Krill cargando
  la próxima canción sin bloquear reproducción musical.
- Se muestra `N` en `$0403`, contador MM:SS en `$0405-$0409`
  (la pantalla completa de Glenn todavía NO está integrada).

## Mapa de memoria / carga

Sin cambios con TEST05:

| Área | Función |
|---|---|
| `$1000` | SID activo, INIT `$1000`, PLAY `$1003` |
| `$5000-$62FF` | SID siguiente, cargado por Krill mientras suena |
| `$6000` | instalador Krill antes de música |
| `$9000` | residente Krill |
| `$C0-$D5` | Krill ZP; conmutación durante IRQ PLAY |
| `$080D-... ` | motor TEST05+TOD, inferior a `$1000` |

Los siete archivos del D64 son idénticos a la imagen TEST05 PASS
salvo el primer PRG `TEST06`. Para demostrarlo, reensamblamos
el TEST05 en el mismo workflow y verificamos equivalencia binaria
con el primer archivo de la imagen TEST05 PASS.

## Prueba en VICE

1. Cerrar VICE y volver a abrirlo en C64 PAL, **True Drive Emulation ON**.
2. Montar `SIDPLAY64MIX_TEST06_10S.d64`.
3. `LOAD "*",8,1`; `RUN`.
4. La carga inicial debe funcionar igual que el TEST05 PASS.
5. La luz del drive debe encenderse para precargar el tema siguiente
   mientras el actual suena. Durante el periodo READY debe apagarse.
6. Debe aparecer `N` y el timer `MM:SS` en la fila de arriba,
   una vez que el siguiente tema está listo.
7. Verificar `MINIMERCADO → CHACABEZA → COMEME → MINIMERCADO`.
   Cada cambio debe ocurrir al `00:10` visible, sin demora de disco.
8. Probar `TEST06_3M05.d64`: igual, pero cada cambio al `03:05`.
9. Escuchar si el tempo de cada SID sigue como en TEST05 PASS.
10. Si la pantalla no actualiza, revisar selector CRB, latches TOD,
    si hay accesos a $DC08 de la música, ritmo IRQ y CIA PAL/NTSC.

**No confundir que la luz del drive se vuelva a encender inmediatamente
después del cambio** (empieza siguiente precarga) con que haya leído
el disco como parte del cambio.

## Documentos fuente

- Código `sidplay64.tas` de Glenn, rutinas de timer y modo Next:
  `src/plt_function.tas`, `src/init.tas`.
- Datasheet MOS Technology 6526 CIA:
  https://myoldcomputer.nl/Files/mos_6526_cia.pdf
  (TOD BCD, secuencia de escritura, lectura enclavada, CRA bit7 50Hz).
- Prueba TEST05 PASS: `tests/TEST05_PASS_26_OCT_2026.md`.

## Siguiente fase

Si TEST06 funciona, tomar el motor congelado y conectar un adaptador
de eventos de Glenn (dirección, campo de timer, Next/Manual) sin
cambiar su loader ni su IRQ hasta que se demuestre la coexistencia
de UI/dir y protocolo Krill.
