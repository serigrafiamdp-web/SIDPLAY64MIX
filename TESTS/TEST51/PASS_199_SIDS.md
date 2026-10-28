# MASTER TEST51 — 199 SID compatibles acumulados — PASS usuario

Fecha: 2026-10-28. Congelado desde `test/test51-12-sids-krill3c00` después de probar `TEST51_12_SIDS_NUEVOS_VICE.d81` y recibir confirmación explícita del usuario: **«pass»**.

## Resultado confirmado
- MASTER TEST50: **187 SID** compatibles acumulados, repartidos en discos de prueba.
- TEST51: **12 SIDs originales adicionales** compatibles con el mismo ONEFILE de TEST50, sin cambiar motor, Krill ni selector:
  `bangkok.sid`, `bangkokldr.sid`, `dmcdemoiv2.sid`, `foodfeud.sid`, `kingsbeach.sid`, `maniax.sid`, `nineteen.sid`, `panther.sid`, `phantoms.sid`, `revengeofdoh.sid`, `storm.sid`, `shape.sid`.
- **Total acumulado: 199 SID compatibles** (187+12), NO montados simultáneamente en un único D81. Selector todavía sin ampliación; biblioteca individual probada de hasta 162 SID.

## Detalles reproducibles
- ONEFILE de TEST51 **idéntico byte a byte** al de MASTER TEST50; SHA256 `34ee9eb8c4bdef43ae99a83a071eb86a29da1404351cc07bae78c5a1e3814ec9`.
- TEST51 D81 contiene `00player.prg`, una canción de referencia `capriphol.sid` y doce SIDs originales; SHA256 `ed62fd40be413d2619fc4476d6f62b5e4242c72b1c5ba319b6cc4bc9554d3b56`.
- Krill v184 sigue residente en `$3C00–$3DEE`, dejando `$8000–$9FFF` libre para SIDs de esa familia. Los originales permanecen inalterados.
- SIDs con nombres en minúsculas sin prefijos numéricos. `cool tune` y `and again` excluidos.
- El usuario reportó PASS de esta imagen; no extrapolar a pruebas físicas ni decir que los 199 conviven en un disco.

## Próxima etapa
Buscar otros grupos de SID difíciles (mayores a 8 KB, carga dentro de otras zonas del player, bajo ROM altas o RSID). Probar cada mejora en rama experimental independiente sin tocar masters congelados. **Ampliar selector al final**, por acuerdo expreso del usuario.

**Estado: MASTER congelado.**