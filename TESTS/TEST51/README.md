# TEST51 — Doce SID originales con memoria $8000–$9FFF

**Estado: pendiente de PASS en VICE.** Esta rama está hecha **directamente desde `MASTER-TEST50-187SID-KRILL-3C00-PASS`**; no cambia una instrucción del reproductor, Krill, ni el selector.

El D81 local `TEST51_12_SIDS_NUEVOS_VICE.d81` contiene:
- El `00player.prg` byte a byte idéntico al MASTER TEST50, SHA256 `34ee9eb8c4bdef43ae99a83a071eb86a29da1404351cc07bae78c5a1e3814ec9`.
- `capriphol.sid`, referencia ya comprobada.
- Los **12 SID originales** que completan la primera familia de 16 ($8000–$9FFF), junto con los cuatro ya PASS de TEST50.

| Nombre D81 | Original en ALTA | LOAD | Final exclusivo |
| --- | --- | --- | --- |
| bangkok.sid | bangkok_knights.sid | $8000 | $9081 |
| bangkokldr.sid | bangkok_knights_loader.sid | $90FA | $9C2E |
| dmcdemoiv2.sid | dmc_demo_iv_tune_2.sid | $9000 | $9B30 |
| foodfeud.sid | food_feud.sid | $9000 | $9CFF |
| kingsbeach.sid | kings_of_the_beach_ingame.sid | $9069 | $9B00 |
| maniax.sid | maniax.sid | $8400 | $940B |
| nineteen.sid | nineteen.sid | $9000 | $9DC4 |
| panther.sid | panther.sid | $9000 | $9D00 |
| phantoms.sid | phantoms_of_the_asteroid.sid | $9000 | $9FEA |
| revengeofdoh.sid | revenge_of_doh.sid | $8B00 | $9820 |
| storm.sid | storm.sid | $9000 | $99C2 |
| shape.sid | shape.sid | $9800 | $9F8B |

Cada archivo conserva sus bytes originales de PSID, incluyendo INIT y PLAY; solo cambia el nombre de directorio para respetar 16 caracteres. Ninguno repite firma de música del total 187 probado.

Verificación de la imagen: 819200 bytes, 14 entradas (ONEFILE + referencia + 12), 2 sectores de directorio, archivos y BAM reextraídos y comparados con originales. SHA256 `ed62fd40be413d2619fc4476d6f62b5e4242c72b1c5ba319b6cc4bc9554d3b56`.

**Prueba de usuario:** abrir D81 en VICE, iniciar `00player`, escuchar `capriphol` de referencia, navegar los 12 SIDs, comprobar prefetch al cabo de 5 segundos y NEXT. Solicitar PASS/FAIL para cada anomalía. Con PASS en esta familia, total acumulado **199 SID**, no necesariamente simultáneos en un D81; el selector no se ha ampliado.

El MASTER50 permanece congelado. No declarar MASTER51 hasta el PASS explícito del usuario.
