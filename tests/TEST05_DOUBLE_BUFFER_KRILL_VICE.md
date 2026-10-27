# TEST05 — Doble buffer Krill, precarga durante la música

**Fecha:** 26 octubre de 2026  
**Estado:** ensamblaje 64tass **PASS**; D64 (7 PRG) y extracción del SID **PASS**; **audio y comportamiento en VICE PENDIENTES**.  
**Base técnica:** `tests/test02_krill_irq_harness.tas` del TEST02C, probado funcional en VICE por el usuario. NO heredamos TEST03B/C/D FAIL.  
**Objetivo:** evitar espera por disco entre canciones; un banco activo + un banco de precarga.  
**No incluye todavía la interfaz original de SIDPLAY64.**

## Secuencia exacta

1. Con KERNAL, **antes de la primera nota**, cargar `INSTA` en $6000,
   `RESIDENT` en $9000 y `MIX_A` en $1000.
2. Instalar Krill v184 en la unidad 1541. No se volverá a usar KERNAL
   para acceder a la unidad durante el resto de la sesión.
3. Arrancar MINIMERCADO con INIT $1000, PLAY $1003 mediante IRQ CIA1.
4. **Inmediatamente** cargar `MIX_B` (CHACABEZA) a $5000 mediante Krill
   mientras la IRQ sigue ejecutando PLAY de MINIMERCADO.
5. Una vez cargado completamente, `next_ready=1`; el drive queda libre.
6. Al vencer el temporizador de prueba (~10s), copiar exactamente
   19 páginas ($1300 = 4864 bytes, padding a cero incluido) de
   $5000 a $1000, ejecutar INIT y rearmar IRQ. **Ningún acceso al
   drive durante este cambio**.
7. CHACABEZA reproduce, mientras Krill carga `MIX_C` (COMEME)
   al mismo banco $5000.
8. Tras ~10s, CHACABEZA → COMEME desde RAM; luego `MIX_A2` (otra copia
   del programa musical de MINIMERCADO, con load-address $5000).
9. El ciclo A → B → C → A se repite indefinidamente. Son tres archivos
   de ejemplo pero solo hay **dos buffers residentes de trabajo**:
   activo $1000 y next $5000.
10. Si la lectura Krill falla, mostrar indicador E, código de error
    y borde rojo. Nunca conmutar un archivo parcial o no READY.

## Mapa de RAM

- $0801–$0A94: programa TEST05 y sus variables (símbolos 64tass).
- $1000–$22FF: código activo del SID, con INIT=$1000 y PLAY=$1003.
- $5000–$62FF: único banco NEXT, 19 páginas, rellenado a cero.
- $6000–$7AE5: instalador Krill TRANSITORIO, después sobrescribible.
- $9000: residente Krill v184.
- $C0–$D5: Krill Zero Page, intercambiada en las IRQ con la versión
  necesaria para el SID. Rutina tomada del TEST02C probado.
- $E0–$E3: punteros transitorios del copy desde RAM, con IRQ inhibidas.
- IRQ $FFFE con ROM deshabilitada durante reproducción.

**Límites de este experimento:** SID reales conocidos, no SID genéricos.
Los tres archivos originales son PSID V2, con load-address=$1000,
INIT=$1000 y PLAY=$1003. Longitudes: 3672, 4442 y 4737 bytes.

## Velocidad y calidad

- En TEST02C, la frecuencia de ~60Hz fue reportada demasiado rápida.
- En TEST02D, llamar PLAY a ~30Hz fue reportado demasiado lento para
  los primeros temas.
- Este TEST05 intenta ~50.1Hz PAL ($DC04=$C8, $DC05=$4C).
- **La correcta velocidad y la suavidad de cambio no se pueden
  declarar PASS hasta comparar en VICE con TEST03A**.
- El copy+INIT de 4864 bytes mantiene IRQ apagadas unas decenas
  de milisegundos; no es un crossfade sin micro-pausa, pero no
  espera disco. Si se percibe, se optimizará aparte.

## Cómo probar en VICE

1. Salir COMPLETAMENTE de VICE y volver a abrir C64 PAL/1541
   (para reiniciar también la unidad y eliminar Krill anterior).
2. Activar **True Drive Emulation**.
3. Montar `SIDPLAY64MIX_TEST05_DOBLE_BUFFER_KRILL.d64`.
4. `LOAD "*",8,1` y `RUN`.
5. Durante la instalación inicial el drive sí lee; al empezar
   MINIMERCADO debe hacer otra lectura **mientras ya hay música**.
6. Borde celeste = Krill leyendo NEXT; verde = NEXT READY;
   rojo = error. Pantalla arriba izq = 1/2/3 tema activo.
7. Observar el ciclo 1 → 2 → 3 → 1, con sonido continuo y sin
   apagones ni espera entre transiciones.
8. Justo DESPUÉS de cambiar tema es NORMAL que se encienda
   otra vez la luz: ya está precargando el SIGUIENTE. Lo importante
   es que la transición no espere a la unidad y la música continúe
   durante esas lecturas.
9. Verificar velocidad musical comparando con TEST03A ya validado.

## Cadena técnica de CI / entregable

- Rama: `test/test05-double-buffer-krill-loop`.
- Código: `tests/test05_double_buffer_loop.tas`.
- GitHub Actions run: https://github.com/serigrafiamdp-web/SIDPLAY64MIX/actions/runs/40437758112
  64tass **PASS**, PRG de 661 B, código < $1000.
- Instador/residente Krill reutilizados del artefacto TEST02C ya
  probado (`INSTA.PRG` 6888 B, `RESIDENT.PRG` 497 B).
- Los tres SID originales extraídos de `SIPLAY.d64` del usuario;
  se conservaron sus cuerpos de código exactos, solo se antepuso
  la dirección de banco y se completó con padding.
- D64: exactamente 174848 B, 7 entradas `TEST05`,
  `INSTA`, `RESIDENT`, `MIX_A`, `MIX_B`, `MIX_C`, `MIX_A2`.
- SHA256 imagen final:
  `0083b5ae769d57c4937260e113ed2a09ef54d9523100c2f35ea9d4715f4c765d`.
- D64 verificado leyendo todos los sectores encadenados de vuelta
  y comparando byte por byte con los siete PRG originales.

**Master y todos los hitos PASS sin tocar. No hacer merge a master
hasta PASS real en VICE.**

### Después del PASS

1. Integrar estado READY/PLAYING/LOADING en la interfaz de Glenn,
   manteniendo rutina de cambio desde RAM ya validada.
2. Separar `N` visual de `playlist_ready` hasta terminar directorio
   para evitar bloqueo de inicialización.
3. Calibrar velocidad por PSID, no por divisor global.
4. Cambiar timer a 03:05 configurables por usuario.
5. Evaluar reubicación en vez de memcpy si hace falta eliminar
   incluso su corta pausa.
