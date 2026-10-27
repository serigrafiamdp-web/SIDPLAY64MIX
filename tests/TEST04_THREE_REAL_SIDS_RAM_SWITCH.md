# TEST04 — Tres SID reales cargados una vez, cambios desde RAM (26/10/2026)

## Alcance

**Prototipo autónomo, sin interfaz SIDPLAY64 original todavía.**

El usuario pidió **cero espera de DISCO entre canciones**.
El TEST04 carga *los tres SID* antes de reproducir ninguna canción,
luego cambia A → B → C → A de forma automática, cada seis segundos,
copiando una instantánea de 19 páginas al rango $1000 y llamando a
INIT $1000 / PLAY $1003. Se usa **únicamente RAM** en el cambio; el
cargador KERNAL nunca vuelve a llamarse. **No hay Krill**.

Originales del D64 aportado por usuario:
- A: MINIMERCADO.SID, payload **3672 bytes**.
- B: CHACABEZA.SID, payload **4442 bytes**.
- C: COMEME (1).SID, payload **4737 bytes**.
- Los tres PSID v2 tienen INIT=$1000 / PLAY=$1003 y velocidad
  marcada CIA (bits 0..31 a 1). Los datos originales NO se reubican.
- El reloj del PROTOTIPO se ajusta a 50Hz aproximados en PAL (CIA1);
  no se copió literalmente la política CIA de Glenn, así que la
  velocidad musical debe validarse auditivamente en VICE.

## Mapa RAM

- $0801-$09B0 aprox: `RAM_PLAYER`, BASIC `SYS 2061`;
- $1000-$22FF: SID actualmente ejecutado;
- $3000-$42FF: caché fija B (code DATA only, no ejecutar ahí);
- $5000-$62FF: caché fija C;
- $7000-$82FF: caché fija A;
- $FFFE/$FFFF: vector IRQ hardware con ROM deshabilitado, $01=$35.

La copia de **4864 bytes** al cambiar toma ciclos de CPU con
interrupciones deshabilitadas; es una transición RAM, **no un
crossfade ni una conmutación absolutamente instantánea**. Es esperable
una pausa breve de algunos fotogramas; **no existe latencia de drive**.
Si este test funciona, el próximo paso será optimizar la copia y/o
reubicar canciones para evitarla.

## Arranque / qué debe verse

Montar `SIDPLAY64MIX_TEST04_3SID_RAM_SIN_ESPERA.d64` en VICE C64 PAL,
**True Drive Emulation habilitada**.

1. `LOAD "*",8,1` y `RUN`.
2. **PRIMERA VEZ**: drive carga los archivos `RAM_A`, `RAM_B`,
   `RAM_C` con KERNAL. Puede llevar un tiempo; es normal.
   En esquina superior izquierda aparecerán 1,2,3 como checkpoints.
3. Después de cargar los 3, empieza a sonar MINIMERCADO.
4. Luego de aproximadamente 6s pasa a CHACABEZA; a los 6s a COMEME;
   luego vuelve a MINIMERCADO, automáticamente.
5. La esquina superior izquierda muestra **1,2,3** según canción.
   La casilla siguiente muestra el número de cambios; el borde varía
   de color. **La luz del drive debe permanecer apagada durante
   A→B→C→A**.
6. En error de precarga KERNAL, borde rojo y "E" en casilla 2.

**No modificar la unidad ni cambiar de D64 mientras está reproduciendo**.
No hace falta pulsar la tecla N porque todavía no hay interfaz Glenn.

## Pruebas de construcción realizadas (NO es PASS en VICE)

- 64tass sobre `tests/test04_three_sid_ram_no_drive.tas`: **PASS**
  (431 bytes; no se superpone con SID $1000).
- GitHub Actions: **PASS** al compilar y armar D64 sintético para
  validación. https://github.com/serigrafiamdp-web/SIDPLAY64MIX/actions/runs/40436859754
- Se extrajeron los PSID reales del D64 original de usuario; encabezado
  PSID v2, direcciones, bits de velocidad, tamaño y cadenas de
  sectores comprobados.
- D64 REAL 174848 bytes, 4 archivos:
  `RAM_PLAYER`, `RAM_A`, `RAM_B`, `RAM_C`.
- SHA256 D64 REAL: `4b910054a1aa680b5266ae1264d349cccf4c9619e946be019c08ce29de0da38a`.
- Lectura independiente de las cuatro cadenas PRG desde el D64 creado
  coincide byte por byte con el empaquetado.
- **El audio y el cambio en VICE quedan PENDIENTES de validación.**

## Justificación técnica

La solución no depende del estado del drive ni del modo N del Glenn
durante INIT, y resuelve la cuestión arquitectónica mínima:
**¿se pueden cambiar estos tres archivos SIN disk I/O?** Sí,
el motor nunca invoca `LOAD/OPEN/CHRIN` durante reproducción.
La corrección y el sonido real se deben verificar en VICE.

**Una vez PASS de este experimento**: integrar esquema A/B/C READY en
la GUI/timer original; luego agregar Krill para renovar bancos durante
audio (sin volver a usar ROM LOAD sobre el mismo protocolo activo).

Ningún MASTER ni PR previo funcional fue modificado.
