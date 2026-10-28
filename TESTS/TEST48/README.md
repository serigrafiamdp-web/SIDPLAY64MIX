# TEST48 — PSID en RAM bajo BASIC $A000–$BFFF

**Estado:** compila, genera ONEFILE y directorios D81 verificados; **NO PASS musical todavía**.

**Base congelada:** `MASTER-TEST47-164SID-E000-PASS`, que conserva los 164 SIDs comprobados en distintos discos (selector actual validado hasta 162 por imagen).

## Mejora genérica de compatibilidad

El reproductor detecta las cabeceras PSID originales con LOAD entre $A000 y $BFFF, INIT/PLAY originales en el mismo rango y rango de datos enteramente antes de $C000. El cuerpo original del SID se preserva byte por byte.

Durante precarga Krill el banco se prepara en $5000–$6FFF. Se reutilizan los desplazamientos por página de TEST44 y por byte de TEST45: se representa transitoriamente el LOAD con una dirección relativa equivalente `LOAD - $9000`. La música se copia finalmente al destino real $A000–$BFFF con $01=$35 (RAM bajo BASIC, I/O disponible) durante el cambio de canción.

Los caminos ya confirmados (LOAD=$0FFF y $1000–$1FFF, y $E000–$F7FF bajo KERNAL) permanecen separados; no se modifica el contenido de los SID en disco.

## 13 archivos nuevos

| Nombre D81 | Archivo original |
|---|---|
| arkpandora.sid | ALTA/ark_pandora.sid |
| bumpspike.sid | ALTA/bump_set_spike.sid |
| cosmonut.sid | ALTA/cosmonut.sid |
| cybernoid.sid | ALTA/cybernoid.sid |
| cybernoidii.sid | ALTA/cybernoid_ii.sid |
| doubledens.sid | ALTA/double_density_commercial.sid |
| hunterpatrol.sid | ALTA/hunter_patrol.sid |
| intkarate.sid | ALTA/international_karate.sid |
| kentilla.sid | ALTA/kentilla.sid |
| nibbly92.sid | ALTA/nibbly_92.sid |
| oceanload3.sid | ALTA/ocean_loader_3.sid |
| starpaws.sid | ALTA/star_paws.sid |
| thinktwice3.sid | ALTA/think_twice_iii.sid |

Todos son PSID con cuerpo de hasta 8192 bytes, LOAD real en BASIC RAM, final <=$C000 y INIT/PLAY dentro de su propio código. Los 13 son distintos por contenido musical, nombres en minúsculas y sin numeración. Las exclusiones de `and again` y `cool tune` se mantienen.

## Imágenes creadas

- `test48_basic_rom_13_nuevos.d81`: `00player.prg` + una referencia TEST43 + 13 candidatos originales (14 SID).
- `test48_biblioteca_162_sids.d81`: `00player.prg` + 143 SIDs TEST43–46 + seis SID TEST47 ya comprobados + 13 nuevos (162 SID). **No excede el selector validado**.
- `00player_test48.prg`: ONEFILE compilado por GitHub Actions 64tass y PuCrunch.
- Hash ONEFILE SHA256: `188165735253d28c8276d481c4b3ef8e224b3d85e0cdabb393713797133a543f`
- Hash D81 corto SHA256: `ffa5bdfa877f47488756fa23a0c945c4bdc7cbff749ea4c45f97aa9c93b5a3c5`
- Hash D81 mixto SHA256: `8508795cec5062732b6aa4aa7b2e81d3256bbcca3bc6e9ff024bd16a22961221`

Se validaron contra los ZIP originales el contenido y nombre de los SID, no duplicidad, cadenas de sectores y BAM del D81. CI GitHub Actions SUCCESS `40756188029` **solo acredita compilación y regresiones estáticas**, no funcionamiento en VICE.

**Siguiente prueba recomendada:** probar inicialmente `cybernoid.sid`, `cybernoidii.sid`, `intkarate.sid`, `oceanload3.sid` y precarga automática en el D81 corto. Si PASS, 177 candidatos compatibles en total (no todos en una sola imagen), y mantener rama MASTER TEST47 inalterada.
