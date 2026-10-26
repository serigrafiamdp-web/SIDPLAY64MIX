# TEST03B-3 — NEXT predeterminado (control seguro)

**Fecha:** 26/10/2026
**Base:** TEST03B-2 carga correctamente la primera canción (usuario en VICE).
**Fallo diagnosticado:** al pasar a N se ralentiza la canción, hay un acceso
breve al drive y al finalizar el timer no cambia de tema.

## Causa confirmada en el código anterior

1. `mix03_install_now` hace `SEI` y usa `JSR $6000` (instalador de
   Krill), que llama rutinas KERNAL; la ralentización coincide con esa
   instalación durante la música. Su duración exacta no está medida.
2. `mix03_install_now` y `mix03_ensure_loaded` contenían la secuencia
   `LDA #2 / STA plt_flag`, que **fuerza Manual**. Por ello ya no vence
   el timer de Next, aunque el reloj visible siga corriendo.
3. Tampoco existía handoff cache→INIT; Krill v184 instalado en el drive
   no se puede combinar despreocupadamente con la siguiente carga
   KERNAL tradicional. La transición N no debe retomarse hasta resolver
   el protocolo de drive o el handoff directo desde RAM.

**Precaución:** esto identifica el bug del temporizador. No confirma
todavía que la instalación de Krill sea la única causa del audio lento.

## Cambios de esta prueba

- `sidplay64.tas` inicializa `plt_flag=$00` y `plt_letter='N'` en
  `start`, **solo si `DEF_MIX03=1`**. Compilación normal de Glenn sin
  cambios de conducta.
- `DEF_MIX03_PREFETCH` separado, predeterminado `0`. Mientras está
  desactivado, `mix03_watch_next` retorna sin cargar archivos auxiliares
  ni instalar Krill.
- `src/irq.tas` llama directamente al `playmus` original de Glenn
  cuando `DEF_MIX03_PREFETCH=0`: se eliminó el wrapper extra de IRQ.
- Se conserva el punto de instrumentación en `plt_advance`, que
  permite comprobar el disparador N original sin intervención de Krill.
- **Krill temporalmente inactivo en este D64.**
- `master`, TEST03A PASS, TEST02C/02D PASS y TEST03B-2 intactos.

## Comprobaciones

- 64tass build original: **PASS**.
- 64tass TEST03B-3 / N predeterminado: **PASS**.
- PuCrunch genera PRG: **PASS**.
- D64 de 174848 B con PRG nuevo y los **20 PSID originales idénticos**:
  **PASS**, verificación por comparación byte a byte.
- **VICE / interfaz / audio / timer: todavía no probado por usuario**.

## Procedimiento en VICE

1. Reiniciar C64 y emulación de 1541 (True Drive Emulation ON).
2. Cargar `SIDPLAY64MIX_TEST03B3_NEXT_DEFAULT.d64`.
3. `LOAD "*",8,1`, `RUN`.
4. Comprobar que aparece **N** inmediatamente al abrir la interfaz.
5. Seleccionar `MINIMERCADO.SID` y presionar RETURN.
6. Sin tocar teclas, al vencer el timer debe cambiar al siguiente SID
   **mediante carga tradicional**.
7. Verificar velocidad musical normal y controles M/N/R.

Si falla ya en esta variante (sin Krill), la causa no es el fastloader,
sino el hook/estado del reproductor de Glenn.

## Próximos pasos técnicos

- Restaurar Krill sin detener prolongadamente las IRQ: instalación
  en una fase sin música o rediseño bajo contexto IRQ.
- Mantener NEXT activo sin forzar manual y sin acceso KERNAL incompatible.
- Validar candidatos de precarga y recuperar header PSID, flags,
  frecuencia INIT/PLAY, y subtune antes del handoff.
- El siguiente TEST deberá demostrar un cambio efectivo desde RAM
  con el timer N y lectura de un tercer SID mientras el segundo suena.

**Repositorio:** https://github.com/serigrafiamdp-web/SIDPLAY64MIX
**Rama:** `test/test03b3-default-next-timer-safe`.
**No mergear todavía.**
