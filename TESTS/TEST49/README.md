# TEST49 — PSID original LOAD $8000-$8FFF, sin tocar Krill en $9000

**Estado:** 64tass + PuCrunch compilación PASS y regresiones estáticas. **NO PASS de VICE todavía.**

## Baseline
MASTER congelado `MASTER-TEST48-177SID-BASIC-ROM-PASS`. Compatibilidad previa: 177 SIDs en varios discos de prueba; selector individual limitado a 162 SID probados.

## Nueva corrección de incompatibilidad compartida
Los SID con código en `$8000–$8FFF` pueden sobrescribir la copia de los 512 bytes iniciales del residente Krill que antes vivía en `$8800–$89FF`. En TEST49 se protege **antes de cargar el primer SID**, copiándola a `$3C00–$3DFF` (intervalo que no ocupa el simbionte TEST49 `$3000–$3BFF`, ni header `$3E00`). Durante activación inicial del cargador, se copia la imagen protegida a la dirección activa del residente Krill `$9000–$91FF`, sin depender de si el SID sobreescribió $8800.

Después de eso el loader reconoce PSID originales con LOAD en `$8000–$8FFF` e INIT y PLAY dentro de la música. Reutiliza desplazamiento virtual TEST44/45 (dirección virtual `LOAD-$7000`), protege el excedente en staging `$6000–$6FFF` y durante NEXT copia **exactamente 4096 bytes** a `$8000–$8FFF`, sin tocar el Krill activo desde `$9000`.

Todo SID conserva su contenido binario original, sin convertir cabecera, código o música. El resto de categorías TEST43–48 preserva sus propias rutas.

## Seis SIDs nuevos en TEST49
| Nombre D81 | Original | LOAD |
|---|---|---|
| `alfscatrap.sid` | `ALTA/alfs_cat_rap.sid` | $8000 |
| `battlebrit.sid` | `ALTA/battle_of_britain.sid` | $8000 |
| `blueorder.sid` | `ALTA/blue_order.sid` | $8000 |
| `bravestarr.sid` | `ALTA/bravestarr.sid` | $8006 |
| `eagles.sid` | `ALTA/eagles.sid` | $8000 |
| `sigmaseven.sid` | `ALTA/sigma_seven.sid` | $8000 |

Todos los cuerpos terminan a más tardar en $9000 (no sobrepasan $8FFF), y sus INIT/PLAY están dentro de sus propios cuerpos. Sin duplicados de música con los 177 anteriores.

## Discos
- `test49_8000_6_nuevos.d81`: 6 nuevos + 1 referencia comprobada; más `00player.prg`.
  SHA256 `f9c53b2f2769f63bc571cb421c6499e82f88427fcdd14982d1d087dc36c5915a`.
- `test49_biblioteca_162_sids.d81`: 162 SIDs seleccionados de las familias anteriores y nueva, el límite actualmente probado de lista, sin modificar el selector.
  SHA256 `893153e43587d07a4fd9b21b011858bf779448bffcafe6a594d454f1de58dda9`.
- `00player.prg` TEST49: 12912 bytes PRG PuCrunch.

Archivos en minúsculas, sin numeración de SID; `cool tune` y `and again` siguen excluidos.

**Precaución:** la confirmación del CI no acredita audio, portada, precarga ni transición. El usuario debe probar VICE antes de elevar a MASTER. El total potencial tras PASS sería **183 SIDs**, acumulados en varios discos, sin ampliar selector.
