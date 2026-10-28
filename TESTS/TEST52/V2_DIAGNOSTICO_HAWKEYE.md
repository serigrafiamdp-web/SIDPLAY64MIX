# TEST52 V2 — Hawkeye se detiene dentro del instalador Krill

**Estado:** compila con 64tass/PuCrunch y pasa verificaciones estáticas; **NO PASS de reproducción en VICE**. El usuario informó que el TEST52 original mostró pantalla negra al intentar arrancar Hawkeye.

## Diagnóstico del monitor VICE recibido

- `PC=$7753`, `A=$C3`, `X=$FF`, `Y=$00`, `SP=$F6`, `$01=$36`.
- `$3FF0=$01` original PRG preparó payload Krill.
- `$3FF1=$11` activación iniciada justo antes de `JSR $6000`; no llegó a `$12` (instalación completada).
- `$3FFC=$00` aún no activado.
- `$3C00` tiene código de Krill rebajado, tal como TEST50.
- `PC=$7753` pertenece al instalador v184, a una espera de líneas IEC ($DD00). Esto **no demuestra por sí solo** que el fallo sea en el installer, pero confirma que la CPU no pasó a música o NEXT.

## Conflicto de RAM identificado

Binario instalador **6886 bytes** ocupa `$6000–$7AE5`; Hawkeye original carga código musical desde `$7AE0`, superponiéndose con los **últimos seis bytes**. En la copia original del instalador son `30 30 2E 38 36 00` (cadena final de versión). La sobreescritura está confirmada por la intersección de rangos, pero su causalidad sobre la espera IEC aún es una hipótesis y debe validarse.

## Solución TEST52 V2

1. `mix10_prepare` preserva seis bytes $7AE0–$7AE5 del instalador antes de la primera carga DOS.
2. En `mix10_activate`, guarda temporalmente los seis bytes del SID original, restaura los seis del instalador, llama `JSR $6000`, preserva el estado de CPU y vuelve a restaurar los bytes de música antes de INIT.
3. No modifica ningún SID, sus cabeceras, Krill residente en $3C00, ni los caminos de precarga de las 199 músicas anteriores. Este test permanece experimental.

## Imagen de VICE

- D81 `TEST52_V2_2_SIDS_REPARACION_KRILL.d81`: `00player.prg` recién compilado, referencia `capriphol.sid`, `hawkeye.sid` (8.768 bytes), `comicbakery.sid` (8.448 bytes).
- PRG: SHA256 `cfc6039d1325f3cc9d70f432d14af76a08de56ccd3cdf88859219c44486f206a`, 13.002 bytes.
- D81: SHA256 `31381d71d35cc3870cb583a34f38665ce2dd5fa6e029e705b7eb11a5b65207ea`, 819.200 bytes, BAM/directorio/extracción verificados.
- CI GitHub Actions `40781705366`: SUCCESS (solo compilación y chequeos estáticos).

**Prueba sugerida:** reiniciar VICE, montar D81 V2, iniciar `00player.prg`, seleccionar Hawkeye; observar audio, pasar a Comic Bakery, verificar NEXT y precarga. Si persiste pantalla negra, enviar `r`, `m $3ff0 $3fff` y `m $7ae0 $7ae5`. No declarar PASS sin confirmación.

MASTER congelado `MASTER-TEST51-199SID-KRILL-3C00-PASS` permanece intacto.
