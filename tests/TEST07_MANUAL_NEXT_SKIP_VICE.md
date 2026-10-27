# TEST07 — Modo N/M y RETURN (sobre TEST06 PASS)

Fecha 26/10/2026. **TEST06 PASS confirmado por el usuario.** El usuario no
especificó si probó solo la variante de 10s o también la de 03:05:
la confirmación se registra para el mecanismo probado, sin atribuir
validación separada a ambas variantes.

## Congelación de lo que funciona

- TEST05 PASS: rama `milestone/test05-double-buffer-vice-pass-26oct2026`,
  commit `dac550bfff24fd20cd18ec34c983a02402d7f69b`.
- TEST06 PASS: rama `milestone/test06-tod-timer-vice-pass-26oct2026`,
  commit `7f8d41e0df8ff4658f8627a407be93f06a2d45b1`.
- El TEST07 está basado en TEST06, manteniendo intactos el
  cargador Krill v184, rutina de ISR PLAY, buffers A=$1000 / B=$5000,
  y los originales 3 PSID.
- El programa autónomo **NO es la interfaz completa de Glenn**.
  Test07 añade el comportamiento M/N/Skip que necesitaremos integrar.

## Cambios acotados de TEST07

- Inicializa por defecto **N**, modo automático.
- **M**: pasa a Manual, el reloj sigue avanzando pero la transición
  no se dispara sola al vencer.
- **N**: vuelve a Next, por lo que si el tiempo ya venció y existe
  NEXT_READY, el cambio ocurre de inmediato.
- **RETURN**: fuerza NEXT de inmediato cuando el próximo SID
  está READY, independientemente del modo.
- Sólo explora teclado cuando Krill ha terminado de precargar,
  para evitar interferencias con la comunicación IEC durante lectura.
- Se usa directamente CIA1 (sin llamadas KERNAL, pues los ROMs
  están desconectados): PA4=$EF, PB4=tecla M, PB7=N;
  PA0=$FE, PB1=RETURN. Se verifica con tabla de teclado C64:
  https://www.c64-wiki.com/wiki/keyboard
- Muestra pantalla simple: modo M/N y contador TOD MM:SS;
  línea con ayuda "N NEXT   M MANUAL  RET SKIP".
- Dos variantes `TEST07_10S_CONTROL_M_N.d64` y
  `TEST07_3M05_CONTROL_M_N.d64`; contenido de loader y canciones
  idéntico al TEST05 PASS en ambas.

## Seguridad de la entrega

Workflow:
https://github.com/serigrafiamdp-web/SIDPLAY64MIX/actions/runs/40441003703

CI con 64tass compiló ambos TEST07, más baseline TEST05 y TEST06.
Al empaquetar localmente se comprobó:
- SHA del D64 TEST05 PASS:
  `0083b5ae769d57c4937260e113ed2a09ef54d9523100c2f35ea9d4715f4c765d`.
- El `TEST05_REFERENCE.PRG` reproducido en el CI es idéntico al
  primer ejecutable del D64 TEST05 PASS.
- El `TEST06_10S_REFERENCE.PRG` compilado es idéntico a la versión
  incluida en el D64 TEST06 de 10s.
- Ambas compilaciones TEST07 quedan por debajo de $1000.
- Conservan EXACTOS seis archivos del TEST05 (INSTA, RESIDENT,
  MIX_A, MIX_B, MIX_C, MIX_A2). El primer archivo es TEST07.
- D64 174848 B, 35 pistas, BAM, cadenas de sectores y cargas PRG
  verificadas mediante relectura de cada archivo.

**VICE: TEST07 todavía no está validado.**

## Cómo probar en VICE

1. VICE PAL con True Drive Emulation (reiniciar VICE).
2. D64 TEST07 de 10 segundos.
3. Cargar `LOAD "*",8,1` + `RUN`.
4. Mientras una canción se reproduce, la siguiente se carga por Krill.
5. Una vez que el borde esté verde (READY), pulsar M.
6. Al pasar `00:10`, la canción debe seguir sonando, modo M.
7. Pulsar N; debe iniciar canción siguiente desde RAM, sin carga
   de disco durante la transición.
8. En READY probar RETURN; debe saltar al siguiente tema.
9. Repetir con variante 03:05 tras validar versión rápida.
10. Si N/M/Return no responde, comprobar CIA1 port A/B y
    configuración de joystick/teclado en VICE. Esta versión
    puede ignorar teclas mientras Krill está físicamente leyendo.

## Próximo paso

En caso de PASS, introducir ventana/gui original de Glenn reutilizando
la pila de carga y control probados, sin reinstalar Krill ni activar
el avance de playlist antes de la primera canción.

**Master, TEST05 y TEST06 conservados.**
