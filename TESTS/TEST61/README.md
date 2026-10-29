# TEST61 — nueve SIDs nuevos del TEST59 + regresiones A/B PASS

**Estado:** D81 armado y auditado; **PENDIENTE de PASS auditivo en VICE**.

**Base de código de reproducción:** ONEFILE exacto del `TEST60_B_TEST59_EXPERIMENTAL_MATRIZ_SID.d81`, **sin modificación del motor ni del archivo SID original**. El usuario ya confirmó `TEST60 B` PASS: reproducción de los 12 SIDs, incluido `magnificent.sid` LOAD $0F80 y `hawkeye.sid` 9 KB. El nuevo D81 comienza con `capriphol.sid` para activar Krill por la ruta previamente aprobada. Se excluye `BUGGY.SID` (JAM histórico en TEST58).

## Imagen D81 y validación de bytes

`TEST61_9_NUEVOS_Y_REGRESION_UNIVERSAL.d81`

- Imagen 1581 de **819.200 bytes**. SHA256: `4802405e86a6cddf7472c2615791b06c52784760fe9d88bef8769d73a771b421`.
- `00player.prg` experimental exacto: SHA256: `bfaac11797663c3bc98ed84da99c0b17b81530b1228c7b974d739e5deab52bc1`.
- 21 archivos: **un ONEFILE + 20 SIDs**; 3 sectores de directorio; BAM reconstruido completamente a partir de los sectores realmente ocupados, eliminando marcas heredadas del D81 plantilla; 417 sectores reservados/ocupados en total; verificación de las cadenas, tamaños y sectores libres realizada.
- Los nueve archivos pendientes se copiaron byte a byte del D81 del TEST59 (sin convertirlos). Las otras referencias se copiaron del TEST59 o del TEST60 B. Reextracción de los 21 archivos desde el nuevo D81 y comparación byte a byte de todos ellos PASS.
- ZIP `TEST61_D81_Y_LEEME.zip` contiene la imagen y las instrucciones.
- Esta validación es únicamente **estructural**, NO confirma ejecución ni prefetch en VICE.

## Matriz de 20 SIDs en orden exacto

| Pos. | Archivo | LOAD | Estado previo |
|---:|---|---|---|
| 1 | `capriphol.sid` | $1000 | PASS; activar Krill |
| 2 | `magnificent.sid` | $0F80 | PASS TEST60 B |
| 3 | `chopper.sid` | $0F87 | NUEVO pendiente |
| 4 | `hawkeye.sid` | $7AE0 (9 KB) | PASS regresión |
| 5 | `pitfall.sid` | $0F88 | NUEVO pendiente |
| 6 | `humanoid.sid` | $4000 | PASS regresión |
| 7 | `mrmonster.sid` | $0F94 | NUEVO pendiente |
| 8 | `montyrun.sid` | $8000 | PASS regresión |
| 9 | `anthem.sid` | $0F9C | NUEVO pendiente |
| 10 | `lethalweapon.sid` | $0FFF | PASS regresión |
| 11 | `aisledance.sid` | $0FAD | NUEVO pendiente |
| 12 | `vortex.sid` | $E008 | PASS regresión |
| 13 | `tuneseven.sid` | $0FD0 | NUEVO pendiente |
| 14 | `danko.sid` | $2000 | PASS regresión |
| 15 | `lightspeed.sid` | $0FE0 | NUEVO pendiente |
| 16 | `illusion.sid` | $0FF0 | PASS regresión |
| 17 | `vampireintro.sid` | $0FE5 | NUEVO pendiente |
| 18 | `alloyrun.sid` | $E000 | PASS regresión |
| 19 | `aurum.sid` | $0FEB | NUEVO pendiente |
| 20 | `arkpandora.sid` | $A000 | PASS regresión |

**Nuevos pendientes = 9:** chopper, pitfall, mrmonster, anthem, aisledance, tuneseven, lightspeed, vampireintro, aurum. `magnificent` ya es el 233.º SID universal confirmado.

## Cómo probar

1. Lanzar TEST61 en VICE desde cero y **comenzar con capriphol**, para activar Krill.
2. Recorrer **toda la lista** con reproducción y precarga/NEXT, sin omitir canciones. El nuevo SID y su referencia de regresión posterior alternan para comprobar convivencia.
3. Probar la **selección manual por Enter** de nuevas pistas tras activación de Krill; prestar especial atención a las transiciones `chopper → hawkeye`, `pitfall → humanoid`, `vampireintro → alloyrun`, `aurum → arkpandora`.
4. Si se produce fallo, anotar último SID reproducido, SID seleccionado, mecanismo (NEXT o Enter), borde de pantalla y en monitor: `m $3ff0 $3fff`. No asumir JAM si solo vuelve a portada.
5. Si todos PASS, **242 SID en la línea universal = 232 MASTER58 + magnificent + 9 nuevos**. **No crear MASTER59/61 ni subir recuento hasta PASS explícito**.

La rama `MASTER-TEST58-232SID-4000-4FFF-PASS` permanece **congelada y sin cambios**. TEST59 queda experimental con incidencias históricas y TEST55 aislado sigue separado.
