# MASTER TEST45 — 139 SID · PASS del usuario

Fecha: 2026-10-28.

Rama congelada a partir de `test/test45-unaligned-load`.
Confirmación del usuario para el TEST45: **"pass"**, luego de la prueba solicitada de reproducción, precarga y transiciones de los seis SIDs nuevos.

## Alcance

- 133 SIDs del MASTER TEST44, ya confirmados.
- 6 nuevos PSID con LOAD no alineado probados en TEST45:
  - `alltogether.sid` — LOAD $101B
  - `doubledragon.sid` — LOAD $1340
  - `mag_fields.sid` — LOAD $17B3
  - `layla_mix.sid` — LOAD $18D0
  - `playboy.sid` — LOAD $19F0
  - `s-express.sid` — LOAD $1035
- Total: **139 archivos SID** en la biblioteca integrada confirmada como PASS por el usuario.
- Se preservan los SIDs originales sin reescritura, y los nombres SID van en minúsculas sin numeración. El ejecutable ONEFILE se llama `00player.prg`.
- `cool tune` y `and again` continúan excluidos.
- Código TEST45 admite LOAD original $1000–$1FFF (incluidas direcciones no alineadas), siempre sujeto a límite de memoria de $3000 y validaciones de PSID. INIT y PLAY dinámicos permanecen dentro de $1000–$2FFF.

## Próximo experimento

Crear `test/test46-load-0fff` en rama separada para abordar LOAD=$0FFF, protegiendo los bytes previos a $1000 y evitando tocar la RAM de Glenn. No modificar esta rama MASTER.

Estado: PASS declarado por usuario; no atribuir verificación de hardware real o instrumentos automatizados si no se ejecutaron.
