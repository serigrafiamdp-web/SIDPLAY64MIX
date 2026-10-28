# TEST40 — Corrección del salto anticipado a la canción 1

## Síntoma y causa confirmada

En TEST38, al seleccionar manualmente una canción situada después del puesto 19, la reproducción del SID puede arrancar correctamente, pero a los 5 segundos el prefetch ejecuta `mix10_service` y calcula el siguiente SID con `cmp #19`. Para cualquier índice actual de 18 o superior selecciona `mix10_pending=0`, es decir la primera canción. El NEXT posterior confirma el salto a 1, aunque existan muchas más canciones.

La rutina de lista de Glenn `src/plt_function.tas` ya utiliza `maxfile`; **el límite es el del prefetch que introdujimos**. TEST39 había eliminado los valores literales 19/20; TEST40 refuerza el cálculo con `mix40_sid_count=maxfile-1`.

## Algoritmo

- `maxfile` cuenta el PRG de arranque y los SID del directorio.
- `mix10_current` es el índice musical actual, empezando por cero.
- `mix10_pending = (mix10_current+1) mod (maxfile-1)`.
- En la lista de 47 SID del D64 de regresión: 20->21, 35->36, 46->47, 47->1.
- En el SD2IEC de 72 SID sueltos: 60->61, 71->72, 72->1.

## Validación

- CI build GitHub Actions 40629243898: PASS (64tass + PuCrunch + pruebas estáticas sobre listas de 1 a 162 SID y todos los puntos de selección).
- Se generó localmente el D64 de prueba `TEST40_NEXT_47SID_VICE.d64` con 47 SID originales del lote fácil y un único PRG. Cada SID se preservó byte a byte. Los nombres de directorio se renumeraron 001..047 para facilitar las pruebas.
- SHA256 del D64: `b7ce3fb0ba8a62f461e7cb020e75e3676e56d5cc7431ca0f3c41413b724ce442`.
- D64 empaquetado mediante `tools/test31_pack.py` original, con lectura completa de los 48 archivos y verificación byte por byte; el binario de programa es exactamente el de TEST40 publicado por GitHub Actions.
- **VICE aún no probado por el usuario, TEST40 no es MASTER**.

## Inspección en VICE

`m $3ff4 $3ffa` muestra:
- $3FF4 índice 0-based del SID actual
- $3FF5 índice 0-based del siguiente SID precargado
- $3FFA cuenta de entradas del directorio (se espera $30=48 para D64)

Si selecciona la pista 30, al cargar la siguiente debe indicar current=$1D (29) y pending=$1E (30), sin volver a 0. Con la pista 47 pending=0 es correcto.

Continuar TEST38 PASS y TEST35 MASTER intactos; TEST39 y TEST40 siguen experimentales hasta probar VICE y SD2IEC físico.
