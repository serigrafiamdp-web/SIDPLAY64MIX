# MASTER TEST46 — 143 SID — PASS confirmado por usuario

Fecha: 2026-10-28. Congelado desde `test/test46-load-0fff`.

El usuario informó **"pass"** para el TEST46 luego de probar el disco con los cuatro SIDs originales `LOAD=$0FFF`, `INIT=$0FFF`, `PLAY=$1003`.

## Canciones de prueba integradas

- `lethalweapon.sid`
- `acid_jazz.sid`
- `holy_daze.sid`
- `nineoneone.sid`

La biblioteca tenía 139 SIDs confirmados previamente en TEST45; con estos cuatro nuevos: **143 SIDs PASS**.

## Implementación

- Reconocer clase de PSID con LOAD/INIT en $0FFF y PLAY $1000-$2FFF.
- Conservar byte original en $0FFF y cargar el resto de los bytes en $1000-$2FFF.
- Mantener precarga de Krill y vectores INIT/PLAY originales.
- No cambiar ni convertir el contenido de ningún archivo .sid.
- Los nombres de SID siguen todos en minúsculas, sin numeración añadida. El único archivo con prefijo numérico es el ejecutable `00player.prg`.
- `cool tune` y `and again` excluidos.
- La versión anterior MASTER TEST45 de 139 SIDs se conserva congelada.

**Estado:** PASS reportado por usuario en VICE para TEST46. No equivale a validación documentada en hardware real. Esta rama debe permanecer intacta para la próxima exploración en TEST47.

Nota histórica mencionada por el usuario: estos cuatro SIDs pertenecen al compositor del SIDPLAY64 original, Glenn Rune Gallefoss.
