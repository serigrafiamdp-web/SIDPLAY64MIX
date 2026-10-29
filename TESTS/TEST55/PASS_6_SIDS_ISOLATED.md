# TEST55 — PASS del usuario (variante de memoria AISLADA)

**Fecha:** 2026-10-28

La prueba de usuario en VICE con `TEST55_6_SIDS_SIMBIONTE_3000.d81` obtuvo respuesta expresa **«pass»**. El disco contenía seis SID originales de la colección MUSICIANS.zip y una referencia previamente confirmada, compilados con la variante TEST55.

## Seis nuevos PASS de la clase LOAD=$3000-$3BFF

- cybertron.sid
- kungfumaster.sid
- spacetravel.sid
- lawntennis.sid
- budsintro.sid
- grogsrevenge.sid

El código musical de estos SID se mantiene original. En esta variante el simbionte se recompila en $8000-$8BFF en lugar de $3000-$3BFF, el backup de Krill se traslada a $7C00-$7DFF y Krill activo permanece en $3C00-$3DEE; el staging usa banco virtual con comprobación estricta de cola y el handoff copia hasta $3BFF.

## Recuento con alcance preciso

- MASTER54 **207 SID PASS** en la línea universal previa.
- TEST55 **6 SID PASS** de la nueva clase con una variante AISLADA.
- **213 SID distintos PASS acumulados entre diferentes variantes**. No supone 213 compatibles con el mismo ejecutable.

**ADVERTENCIA CRÍTICA:** TEST55 pone el simbionte en $8000, incompatible con los SIDs que cargan en $8000-$8BFF (familia previamente PASS de TEST49-51). No promover esta rama como sustituta del MASTER54 ni anunciar compatibilidad universal 213 hasta resolver coexistencia. Mantener `MASTER-TEST54-207SID-2000-2FFF-PASS` intacto. El selector no se ha ampliado.

## Próximo paso

Diseñar una estrategia de reubicación del simbionte sin sacrificar músicas $8000-$9FFF, por ejemplo elegir banco de código según requisitos de la pista (con revisión de punteros, instalación y handoff) o trasladar a zona alternativa verificada. Repetir regresiones con pistas de las dos familias en **un solo** reproductor antes de congelar un nuevo MASTER universal.

Imagen ensayada: SHA256 `172f5cab4d54a83db2820987c44b3300a29f3b3365dfb03044f933fe521bccac`.
Compilación CI `40794309331` SUCCESS; confirmación musical provino del usuario.
