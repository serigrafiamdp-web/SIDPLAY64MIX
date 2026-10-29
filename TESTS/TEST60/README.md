# TEST60 — Matriz de regresión A/B con un SID por familia

**Estado: imágenes D81 generadas y verificadas byte a byte; PENDIENTE de prueba musical en VICE.**
Fecha 2026-10-29. Esta rama experimental nace de `MASTER-TEST58-232SID-4000-4FFF-PASS`, que permanece inmutable.

## Motivo

El usuario informó que TEST59 no reproducía música inicialmente y volvía a la portada. El monitor mostró `$3FF1=$11`, `$3FFC=00`, `$3FF7=00` al seleccionar `magnificent.sid`. Luego reportó que el programa sí funcionó con otras canciones hasta que una selección manual con Enter de `hawkeye.sid` produjo borde rojo y bloqueo. No se ha demostrado la causa exacta. TEST59 sigue FAIL y `BUGGY.SID` de TEST58 sigue excluido por JAM.

**Objetivo TEST60**: no añadir otra nueva familia ni tocar el motor antes de medir incompatibilidades. Dos D81 con exactamente los mismos SID en idéntico orden; solo cambia el ONEFILE.

## Imágenes A/B

- **A (CONTROL):** `TEST60_A_MASTER58_CONTROL_MATRIZ_SID.d81` — SHA256 `7fd689d2da58a833c0c8fa5b50647350fd423ac480b89b471ec053295279c1b9`. ONEFILE extraído intacto del TEST58 previamente validado: SHA256 `ddfd2d19dc4a6e97b9a3356fa3ce9e4214b9496c9a144e2ab7fff7f23ecba0b4`. Solo se espera soporte de canciones históricas; el último `magnificent.sid` LOAD $0F80 NO está habilitado expresamente en MASTER58.
- **B (EXPERIMENTAL):** `TEST60_B_TEST59_EXPERIMENTAL_MATRIZ_SID.d81` — SHA256 `5cf75bfac5517929b2d95e78f1b566b5a4627819de23b87a5691064aa6db0ee9`. ONEFILE extraído intacto de TEST59: SHA256 `bfaac11797663c3bc98ed84da99c0b17b81530b1228c7b974d739e5deab52bc1`. Solo este reproductor incluye la nueva protección de 128 bytes bajo $1000. **Es experimental, ya tuvo FAIL en otro D81 y no sustituye el control.**

Ambos discos: **819.200 bytes**, BAM nativa D81 (80 pistas × 40 sectores), 2 sectores de directorio, 13 archivos (ONEFILE + 12 SID originales), cadenas de sectores completas, todos los contenidos reextraídos y comparados byte por byte con SID procedentes de D81 previamente comprobados o de TEST59. Los primeros **81 sectores físicos** del control coinciden byte a byte con TEST58: incluyen todo el ONEFILE y `capriphol.sid`. Ningún SID se modificó, convirtió ni renombró internamente. No hay `buggy.sid`.

## Matriz (mismo orden exacto en A y B)

| N.º | Archivo | LOAD | Familia | Situación |
|---:|---|---|---|---|
| 1 | capriphol.sid | $1000 | básica | PASS anterior |
| 2 | airwolf.sid | $1800 | desplazamiento por página | PASS anterior TEST44 |
| 3 | lethalweapon.sid | $0FFF | prefijo de 1 byte TEST46 | PASS anterior |
| 4 | illusion.sid | $0FF0 | prefijo de 16 bytes TEST57 | PASS anterior |
| 5 | danko.sid | $2000 | memoria $2000–$2FFF TEST54 | PASS anterior |
| 6 | humanoid.sid | $4000 | memoria $4000–$4FFF TEST58 | PASS anterior |
| 7 | montyrun.sid | $8000 | Krill residente reubicado TEST50 | PASS anterior |
| 8 | arkpandora.sid | $A000 | RAM bajo BASIC ROM TEST48 | PASS anterior |
| 9 | alloyrun.sid | $E000 | RAM bajo KERNAL ROM TEST47 | PASS anterior |
| 10 | vortex.sid | $E008 | alta no alineada TEST56 | PASS anterior |
| 11 | hawkeye.sid | $7AE0 | stage 9 KB TEST52/TEST58 | PASS anterior |
| 12 | magnificent.sid | $0F80 | nuevo prefijo de 128 bytes TEST59 | **NO PASS; solo diagnóstico** |

## Orden de prueba recomendado

1. Cargar **A CONTROL** desde VICE recién iniciado. Verificar que los **primeros 11 SID** reproducen mediante ENTER y NEXT; probar `vortex → hawkeye`, `humanoid → hawkeye`. El archivo `magnificent` (12.º) puede fallar en el control, no contarlo como regresión del MASTER58.
2. Reiniciar VICE y cargar **B EXPERIMENTAL**. Ejecutar **exactamente el mismo recorrido** con los primeros 11 y comparar el primer fallo observado.
3. Probar `magnificent` **solo después** de que ya sonó `capriphol` y Krill fue activado. Si suena, elegir `hawkeye` con Enter; este cruce busca reproducir el bloqueo reportado en TEST59.

En caso de borde rojo, congelamiento o retorno a portada, abrir monitor e informar `m $3ff0 $3fff` y si es posible `r`, además del último SID que sonaba y el elegido. Los markers `$3FF1`, `$3FF2`, `$3FF7`, `$3FFC` permiten distinguir inicialización, staging y actividad Krill.

**No convertir control MASTER58 en FAIL por una canción nueva no admitida. No congelar TEST59 ni sumar nuevos SIDs hasta PASS de usuario.**

### Notas de reproducibilidad

No se modificó el código en la rama TEST60, porque la finalidad de esta prueba es aislar una regresión entre DOS binarios preexistentes. Las imágenes son datos de ensayo; pueden reconstruirse a partir de los D81 previamente confirmados; están preparadas para VICE o 1581 y no requieren archivos SID sueltos. Nunca alegar que VICE pasó solo por verificaciones estáticas.
