# TEST03B-1 — Krill precarga en SIDPLAY64 de Glenn (WIP)

**Fecha:** 26/10/2026
**Rama:** `test/test03b-krill-live-prefetch`
**Base conservada:** TEST03A PASS (interfaz, sonido correcto, timer M/N/R).
**No fusionar a `master` sin prueba real de VICE.**

## Qué hace esta prueba

1. En la primera entrada al bucle de menú, instala Krill v184 con las
   rutinas normales KERNAL, antes de la reproducción.
2. Conserva el player e IRQ de Glenn, sin bajar ni modificar la cadencia
   musical. El cambio en `src/irq.tas` reemplaza el JSR a PLAY por uno
   de idéntico tamaño que llama al reproductor y, SOLO durante transferencias,
   salva/restaura la Zero Page `$C0-$D5` usada por Krill.
3. Si está sonando el SID del índice **1** del directorio y el modo es
   **N**, carga `STB` al banco `$5000` mientras la música continúa.
4. Si está sonando el SID del índice **2** y el modo es **N**, carga
   `STC` al mismo banco mientras continúa reproduciéndose.
5. Al vencer el timer, **todavía ejecuta la carga ROM tradicional**.
   La copia desde RAM, metadatos e INIT directos se implementarán
   solo después de validar primero la convivencia Krill + IRQ.
6. Los auxiliares `INSTA` y `RESIDENT` siguen siendo **PRG visibles**
   al final de la lista porque los usa KERNAL para instalar Krill.
   `STB` y `STC` tienen tipo DEL para ocultarse en el directorio
   estándar, pero Krill reconoce archivos de ese tipo por nombre y track.
   No ejecutar manualmente INSTA/RESIDENT desde el menú.

## Requisitos

- Commodore 64 PAL emulado en VICE / unidad 1541 real o emulada.
- True Drive Emulation activado.
- Solo los 20 SID del D64 de laboratorio: todos ocupan `$1000-$2922`.
- Memoria reservada: helper `$3000-$33FF`; stage `$5000-$6FFF`;
  Krill instalador `$6000`; Krill residente `$9000`; Zero Page `$C0-$D5`.
  ¡NOTA! `$6000` instala como código transitorio; stage 5000-6fff
  puede sobrescribirlo tras instalar. Esta región está diseñada para uso
  experimental, no para archivos SID con carga arbitraria.

## Señales de diagnóstico

En el extremo inferior de la pantalla:
- `I`: Krill instalado correctamente.
- `P`: precarga terminó.
- `E`: error de instalación o de precarga.
- `T`: el timer avanzó y sigue usando el loader convencional.

La música debería seguir reproduciéndose mientras el LED del drive
trabaja cargando STB/STC, inmediatamente después de pasar a N
mientras suena MINIMERCADO o CHACABEZA.

## Diferencias y limitaciones reconocidas

- Este TEST03B **prueba precarga real**, pero todavía NO hace el handoff
  desde banco de RAM; el cambio al siguiente SID seguirá deteniendo
  brevemente el audio si la carga KERNAL tarda.
- Los archivos auxiliares no deben contarse como pistas musicales.
  Evitar avance circular hasta los últimos elementos en este prototipo.
- Un SID que escriba `$3000-$33FF`, `$5000-$6FFF`, `$9000` o que
  dependa de sus propias IRQ puede romper esta arquitectura fija;
  prohibido anunciar soporte PSID universal.
- La selección para el experimento se basa en la posición del cursor
  en el directorio. Mover el cursor lejos del SID que suena altera qué
  se intenta precargar; no apto para la versión final.
- SD2IEC necesita configurar fallback KERNAL de Krill; esta prueba se
  valida primero solo en una unidad 1541 de VICE.
- No se modifican velocidades musicales ni subtunes.

## Criterio de PASS para continuar TEST03B-2

1. La interfaz de SIDPLAY64 funciona igual que TEST03A.
2. Arranca y se reproducen normalmente las canciones con su temporización original.
3. En modo N, el LED del drive muestra precarga con música continua; aparece P.
4. No se bloquea el menú ni se altera el timer.
5. Las canciones siguen cambiando con la carga estándar al vencer el timer.

Después de este PASS, implementar `mix03_cached_handoff` con:
- validación de candidato seleccionado,
- copia del payload `$5000` → `$1000`,
- procesamiento de cabecera PSID e INIT/PLAY equivalente a Glenn,
- invalidación tras cambio y precarga siguiente,
- fallback al loader normal si no hay un cache válido.

Fuentes: `src/mix03_timer_hook.tas`, `src/irq.tas`,
`sidplay64.tas`, `src/plt_function.tas`.
Documentación Krill v184: https://csdb.dk/release/?id=189130&show=notes .
