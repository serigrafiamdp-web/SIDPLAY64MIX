# TEST46 — original LOAD=$0FFF, INIT=$0FFF (NO ES PASS TODAVÍA)

Base congelada: `MASTER-TEST45-139SID-LOAD-NO-ALINEADO-PASS`, confirmada por el usuario para reproducción/precarga.

## Cambio genérico en código

- Reconocer el caso `PSID` con LOAD=`$0FFF` e INIT=`$0FFF`; PLAY legítimo `$1000–$2FFF`.
- Conservar byte 0 (primera instrucción, en esta muestra `$AA`) y, para los demás 8191 bytes, copiar desde `$53CD` a banco staging `$5000` sin convertir ni parchear el SID original.
- En el cambio de canción con IRQ deshabilitada, copiar banco a `$1000–$2FFF` y recuperar el primer byte en `$0FFF` ANTES de INIT.
- Mantener original Krill, temporizador y rama de carga no alineada TEST45 sin modificar.
- Para todos los demás LOAD, copia desde `$53CC` como antes.
- Límites: no habilitamos aún `LOAD<$0FFF`, alto `$3000+`, RSID/PLAY=0 ni conflictos memoria.

## SIDs originales para VICE

| Archivo incluido | Original | LOAD | INIT | PLAY | bytes de música |
|---|---|---|---|---|---:|
| `lethalweapon.sid` | `ALTA/gr-lethal_weapon.sid` | $0FFF | $0FFF | $1003 | 4676 |
| `acid_jazz.sid` | `ALTA/acid_jazz.sid` | $0FFF | $0FFF | $1003 | 5113 |
| `holy_daze.sid` | `ALTA/holy_daze.sid` | $0FFF | $0FFF | $1003 | 3549 |
| `nineoneone.sid` | `ALTA/nineoneone.sid` | $0FFF | $0FFF | $1003 | 7608 |

La comparación contra `2019.zip` confirma que estos 4 SIDs son byte a byte idénticos a sus originales.
- CI GitHub Actions SUCCESS (ensamblado 64tass, empaquetado PuCrunch, validación estática).
- Lanzador ONEFILE `00player.prg` SHA256 `7dd50562ae1ef47090eceda17e7c853a2e56732417fadff61bf0f813d41305b8`.
- D81 corto: 5 SIDs, hash `268fa4120d62093fc03c9ab293429661b1973482544f9bbd6377f217916cedc6`.
- D81 biblioteca: 143 SIDs, hash `1792175fae254cf6b8743c8ee20529913fb7fd56256821765b033c1b28ad92dd`.

**Estado: COMPILACIÓN PASS; VICE/hardware pendiente.** No cambiar MASTER antes de confirmación.
