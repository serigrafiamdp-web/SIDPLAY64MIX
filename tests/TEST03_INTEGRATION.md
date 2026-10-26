# TEST03A — Integración inicial en SIDPLAY64 (26/10/2026)

**Estado confirmado:**
- Original Glenn v1.21, `defset=4` (SD2IEC), compilación 64tass: **PASS**.
- TEST03A opt-in (`DEF_MIX03=1`), compilación 64tass: **PASS**.
- Compresión PuCrunch a PRG ejecutable con entrada original `$9000`: **PASS**.
- Construcción y verificación de D64 (21 archivos, 20 SID byte a byte intactos): **PASS**.
- **VICE AUDIO/UI: PENDIENTE.** No afirmar que precarga funcione en esta versión.

**Rama:** `test/test03-sidplay64-integracion`. **No fusionar a master.**

## Qué cambiamos realmente

En `sidplay64.tas`:
- Un `DEF_MIX03` opt-in default OFF mediante `.weak`, por lo que
  el build tradicional no incorpora nuevas rutinas.
- En el ciclo `fileSelect`, tras `wjs_display`, llamada a
  `mix03_watch_next` (solo memoriza próximo índice previsto en modo N).
- El helper se ubica en `$3000-$30FF` exclusivamente para la colección
  experimental que carga música en `$1000-$291F`, manteniendo el núcleo
  autorreubicable de Glenn dentro de su límite.

En `src/plt_function.tas`:
- **Dentro de `doload`**, antes del `JMP (wjp_load)`, llamada a
  `mix03_before_load`. Está correctamente situada para cubrir los
  saltos de N normal, fin de lista y R aleatorio.
- Para esta fase NO activa otro banco, NO reconfigura INIT/PLAY,
  NO instala Krill, y nunca saltea el cargador original.
- Si llega a `doload`, se registra el índice elegido y se invalida
  cualquier estado de cache. El `JMP (wjp_load)` original se ejecuta.

Esto demuestra que el punto de decisión del timer está localizado sin
alterar las semánticas de Next/Random/Manual, **NO** demuestra precarga.

## Mapa de memoria del primer build

| Símbolo | Original | TEST03A |
|---|---:|---:|
| `fileSelect` | `$C910` | `$C910` |
| `checkdigits` | `$C9F3` | `$C9F6` |
| `plt_advance` | `$CA03` | `$CA06` |
| `driverend` | `$CF7A` | `$CF80` |
| Límite `driverend` | `$CF84` | `$CF84` |
| `mix03_watch_next` | — | `$3000` |
| `mix03_before_load` | — | `$301E` |

**ADVERTENCIA:** el helper fijo en `$3000` **NO es seguro para PSID
arbitrarios**: una canción que ocupe esa página destruirá el helper. Esta
versión se entrega solo para el D64 limitado a los 20 PSID concretos del
laboratorio. Antes de generalizar se exige un mapa de colisión o
reubicación automática y un chequeo previo a cada carga.

## Empaquetado

- Compilación: `64tass --m6502 -D defset=4 -D DEF_SIDFX=0 -D DEF_REU=0 -D DEF_MIX03=1 -a sidplay64.tas`.
- `tools/normalize_tass_includes.py` adapta rutas antiguas durante la
  compilación CI; no es una modificación del lenguaje musical.
- Compresión: `pucrunch '-x$9000' SIDPLAY64_TEST03_SD2IEC.o64 SIDPLAY64_TEST03_SD2IEC.PRG`.
- D64 final: `SIDPLAY64MIX_TEST03A_ORIGINAL_UI.d64`, producido a partir de
  `SIPLAY.d64`, reemplazando solo el primer PRG y conservando exactamente
  los bytes de las otras 20 entradas.

## Criterios para TEST03A — VICE

1. Cargar `LOAD "*",8,1`, luego `RUN`.
2. Mostrar exactamente la interfaz de SIDPLAY64 y el directorio.
3. Poder seleccionar y ejecutar cualquiera de los 20 SID originales.
4. M, N, R, Next y su timer deben seguir funcionando como en el master.
5. Con transición N al llegar al timer se efectuará **todavía carga
   tradicional desde disco**. Esto es esperado para TEST03A y no un FAIL.
6. Registrar cualquier bug de pausa/velocidad; en este test no se modificó
   la cadencia musical.

## TEST03B — Integración real de precarga pendiente

Primero instalar Krill al entrar en reproducción y separar su memoria de
la del SID que suena y del driver reubicado; proteger CIA IRQ y Zero Page
de Glenn. En modo N capturar el próximo nombre de directorio,
prefetch al banco alternativo mientras suena el actual, verificar
integridad y metadatos de cabecera, marcar `NEXT_READY` **únicamente
al terminar** y, cuando vence el timer, reproducir directamente desde
RAM sin abrir disco. Después cargar C durante B.

R = Random debe reservar un candidato idéntico al que luego seleccionará
la lógica de Glenn; hasta entonces conserva carga tradicional.

No mezclar este hito con el TEST02C/TEST02D, que sí obtuvieron PASS real
de Krill + transición **en un motor aislado**.

## Fuentes

Repositorio: https://github.com/serigrafiamdp-web/SIDPLAY64MIX
Branch PASS aislado: `milestone/test02d-krill-three-sids-audio-pass-26oct2026`.
