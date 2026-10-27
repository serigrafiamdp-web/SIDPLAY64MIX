# TEST08 — PLAYLIST VISIBLE SOBRE TEST07 PASS

**Origen congelado:** `milestone/test07-keys-m-n-return-vice-pass-26oct2026`,
commit `178045f63d6f2a94a2b7a327d6365f3555cc6466`.

El usuario dio **PASS en VICE** a TEST07 (controles M, N, RETURN
sobre Krill doble buffer y reloj CIA TOD). No confirmó separadamente
cada variante 10s/03:05; el alcance validado se conserva sin ampliarlo.

## Qué agrega TEST08

- **Pantalla estática de playlist de 3 SID**:
  MINIMERCADO, CHACABEZA y COMEME.
- Marca * en la línea de la canción activa, tras cada cambio.
- Presenta estado Krill `L` mientras se carga el siguiente SID,
  `R` cuando quedó completo y el timer espera para cambiar.
- Conserva modo N/M y tiempo real MM:SS arriba a la izquierda,
  RETURN sigue saltando cuando está READY.
- Son DOS D64 separados:
  `SIDPLAY64MIX_TEST08_UI_PLAYLIST_10S.d64` y
  `SIDPLAY64MIX_TEST08_UI_PLAYLIST_3M05.d64`.
- Todavía **NO** es el navegador/directorio auténtico de Glenn
  integrado. Esta es una pantalla sobre el motor Krill probado, y
  exclusivamente valida convivencia de GUI/IRQ/fastload.

## Qué NO se modifica

- Instalador Krill y residente.
- Playlist A/B/C y PSID originales.
- INIT/PLAY en `$1000`, cache en `$5000`.
- Conmutación de ZP Krill durante IRQ.
- Frecuencia de música, reloj TOD y controles de TEST07.
- Directorio secuencial original de Glenn; no se invoca.
- MASTER y las ramas congeladas PASS de TEST05, 06, 07.

## Evidencia estática

CI:
https://github.com/serigrafiamdp-web/SIDPLAY64MIX/actions/runs/40441658572
PASS ensamblador 64tass, ambas variantes ocupan 1261 B incluida la
cabecera PRG, bajo el límite de `$1000` sin colisionar con SID activo.

El ensamblado TEST07 de referencia es idéntico al ejecutable anterior
de cada D64 TEST07. Se reconstruyeron **idénticos byte a byte** los
D64 originales de TEST07 con el empaquetador previo antes de generar
TEST08. Se conservaron sin alteración los otros seis PRG:
INSTA, RESIDENT, MIX_A, MIX_B, MIX_C, MIX_A2.
Las nuevas D64 son imágenes de 174848 B, cadenas de sectores y BAM
validadas por lectura circular de todos los archivos PRG.

- SHA256 TEST08 10s:
  `9b5329e9a6bac7ba9ab6e6c6d9f7b0bc5cdba838cb05489554457664055515a4`
- SHA256 TEST08 3:05:
  `fbef49c44df2ee3804f84c3917f005309912b9979281a909c29d5ae01c974020`

## Protocolo VICE

1. Reset completo VICE C64 PAL + 1541 True Drive Emulation.
2. Ejecutar `LOAD "*",8,1`, `RUN`.
3. Ver nombres de las tres canciones, modo N, timer MM:SS.
4. Mientras se ejecuta MINIMERCADO, estado Krill L, después R.
5. Observar estrella * avanzar a CHACABEZA y COMEME;
   el drive solo trabaja precargando, nunca en el handoff desde RAM.
6. Pulsar M cuando hay R: no debe avanzar tras vencer timer.
7. Pulsar N o RETURN: cambiar desde banco RAM sin esperar disco.
8. En caso de error registrar última canción marcada y estado L/R.
9. Si lo anterior funciona validar también la variante 03:05.

**No llamar PASS a TEST08 hasta que usuario lo confirme en VICE**.

## Próximo paso

A partir de TEST08 PASS, evaluar cómo usar la pantalla original de
Glenn y su dirbuffer ya preparado ANTES de instalar el protocolo Krill,
sin volver a mezclar KERNAL LOAD con la 1541 controlada por Krill.
