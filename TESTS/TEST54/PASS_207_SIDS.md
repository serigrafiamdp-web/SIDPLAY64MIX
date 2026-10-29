# MASTER TEST54 — 207 SIDs compatibles acumulados — PASS del usuario

**Fecha:** 2026-10-28  
**Estado:** MASTER congelado; no modificar directamente.

## Origen y validación

Esta rama se congeló a partir de `test/test54-middle-2000-2fff` tras el mensaje explícito del usuario **«pass»** al probar `TEST54_6_SIDS_MEMORIA_INTERMEDIA.d81` en VICE.

- Base previa: `MASTER-TEST52-201SID-9KB-PASS` — **201** SID compatibles acumulados.
- TEST54: **6** SID originales nuevos confirmados.
- Total: **207 SID compatibles acumulados**, verificados en diferentes D81; **NO** implica 207 SID simultáneos en un único disco.
- La rama TEST53 de memoria alta sigue experimental y no forma parte de este MASTER.

## Seis SID de TEST54

| Nombre D81 | LOAD | INIT | PLAY | Fin exclusivo |
| --- | --- | --- | --- | --- |
| `danko.sid` | $2000 | $2029 | $2000 | $3000 |
| `redsnow.sid` | $2036 | $2036 | $203C | $2F03 |
| `trapsv2.sid` | $20F6 | $20F6 | $2103 | $2FEF |
| `sf2ryu.sid` | $2400 | $2400 | $2403 | $2D9F |
| `flower6.sid` | $28FA | $28FA | $2900 | $2FA2 |
| `bmxracers.sid` | $2E00 | $2F90 | $2E00 | $2F98 |

La imagen también incluye `capriphol.sid`, referencia previamente comprobada. Los seis archivos SID conservan los bytes originales de `MUSICIANS.zip`. D81 de TEST54: SHA256 `6c219d0a371a65c818e71dbccfd4645d461474715c2fbe0cdbe12260542d9ec6`.

## Cambio técnico

En `mix46_regular_load`, ampliar la validación de LOAD de `$1000–$1FFF` a `$1000–$2FFF`; conservar comprobaciones originales de INIT y PLAY en el banco y `mix44_align_staging` / `mix45_shift_low` que rechazan excedentes por encima de `$2FFF`.

Krill sigue residente en `$3C00`. Se mantiene la precarga en cinco segundos, las rutas previamente comprobadas de memoria alta y las de 9 KB, y el selector sin ampliación.

La auditoría de `MUSICIANS.zip` identificó **278 candidatos estructurales** en esta subfamilia de LOAD `$2000–$2FFF` y contenido íntegramente por debajo de `$3000`. **No confundir 278 candidatos con 278 reproducciones verificadas en VICE.** La confirmación del usuario incluye solo los seis de este disco.

CI de compilación/regresiones estáticas: GitHub Actions run `40792860448`, SUCCESS. PASS funcional declarado por el usuario.

## Próximos pasos

Continuar con las otras subfamilias del grupo de carga intermedia `$2000–$79FF`, especialmente las que se superponen con el simbionte `$3000–$3BFF`, el Krill `$3C00–$3DFF` o los búferes y el instalador. Trabajar en nuevas ramas experimentales, sin editar este MASTER.

**Acuerdo:** primero ampliar compatibilidad de SIDs; dejar la expansión máxima del selector para después.
