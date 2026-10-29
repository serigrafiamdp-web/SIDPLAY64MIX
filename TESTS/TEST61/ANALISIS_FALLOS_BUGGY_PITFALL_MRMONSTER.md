# Auditoría de SIDs problemáticos — 29/10/2026

**Datos:** análisis byte a byte de los tres originales PSID en `MUSICIANS.zip` del usuario, contrastando el original con sus dos archivos subidos: `BUGGY.SID.prg` y `MRMONSTER.SID.prg`, ambos idénticos a la versión HVSC del ZIP. No modificar originales.

## Tres SID FAIL confirmados por usuario

| SID (ruta HVSC) | Tamaño PSID | LOAD | INIT | PLAY | Songs | Video declarado | Resultado |
|---|---:|---|---|---|---:|---|---|
| `F/Fulton_Douglas/Buggy.sid` | 2.316 B | $40FE | $40FE | $41B1 | 1 | NTSC | JAM |
| `D/DeMeo_Alex/Pitfall.sid` | 2.860 B | $0F88 | $0F96 | $102D | 7 | NTSC | FAIL |
| `D/Del_Priore_Fabian/Mr_Monster.sid` | 2.544 B | $0F94 | $0F94 | $102D | 5 | PAL | FAIL |

Todos PSID v2, LOAD embebido después del offset $007C, un chip, menos de 3 KB, INIT y PLAY separados, nombres de videojuegos. **NO atribuirles una causa común única por esas propiedades.** En el ZIP, **14.340 de 56.568 PSID/SID** ocupan menos de 3.000 bytes en total: descartar por tamaño excluiría muchos otros sin evidencia.

## Firma común Pitfall / Mr. Monster — SOLAPAMIENTO CON STAGING

- Desde RAM **$0F9E** ambos contienen **1.795 bytes consecutivos idénticos** en exactamente las mismas direcciones. Sus entry points PLAY son ambos **$102D** y el código allí coincide byte a byte.
- INIT copia datos mediante `STA $5027,X`, `STA $5115,X`, `STA $5202,X`, `STA $5750,X`, `STA $5800,X`, entre otras escrituras, generando rutinas/datos fuera del intervalo LOAD original.
- En PLAY se observan `JSR $9DD2`, `JSR $50B3` y `JSR $5755`.
- **El staging del reproductor universal ocupa $5000–$73FF**, y su proceso de prefetch también limpia $5300–$77FF antes de Krill. Por lo tanto **las rutinas activas de música en $50xx y $57xx están dentro de buffers que serán sobrescritos**, conflicto estructural real. La ubicación exacta temporal del fallo en VICE todavía no fue instrumentada, pero la incompatibilidad de memoria está suficientemente fundamentada para clasificar esta familia como «riesgo alto; dejar fuera de nuevos tests por ahora».
- También se detecta la escritura `STA $FC75,X` (posible superposición con charset $F800–$FFFF), pero su efecto aún no está determinado.

## Buggy SID: NO es el mismo motor

- LOAD **$40FE**, PLAY **$41B1**; no contiene la firma anterior.
- INIT escribe en registros CIA de temporizador como `STA $DC04`, `STA $DC05` y mantiene estado en RAM/ZP. Esta característica puede interferir con la reproducción/timing, pero **no demuestra la causa del JAM**. Conservar exclusión explícita mientras no se investigue.

## Rastreo de la firma de Pitfall/Mr. Monster en todo MUSICIANS.zip

Firma de 18 bytes: `BD 48 10 9D 27 50 BD 36 11 9D 15 51 BD 23 12 9D 02 52`.

- Aparece en **49 archivos SID** de `MUSICIANS.zip`.
- Todos esos 49 usan LOAD en página $0F.
- **`Chopper.sid` y `Anthem.sid` del TEST61 también presentan la firma**. Marcar como «alto riesgo; pendiente», no como FAIL musical confirmado.
- Los **otros SIDs** de TEST61 no heredan automáticamente esta clasificación.
- **No excluir de la biblioteca canciones previamente PASS solo porque una búsqueda encuentre la firma**; conservar estado individual PASS/FAIL/PENDIENTE y nunca afirmar que los 49 fallaron.

## Política para siguientes pruebas

1. Lista explícita **FAIL/excluidos de próxima selección**: `Buggy.sid`, `Pitfall.sid`, `Mr_Monster.sid`.
2. Lista **en cuarentena técnica**, pendiente de prueba dedicada: los 49 originales que contienen la firma (especialmente `Chopper.sid`, `Anthem.sid`), excepto cualquier SID ya verificado como PASS.
3. **No quitar archivos de MUSICIANS.zip, no modificar el ONEFILE MASTER58/TEST59** por el momento.
4. **No descartar todos los SID de videojuegos ni todos los de tamaño reducido**; usar indicadores concretos de uso de buffers y resultados reales de VICE. La ampliación de candidatos continuará con aquellos sin estas señales de conflicto.

Este análisis es estático en los binarios originales y NO significa que se haya ejecutado el código bajo VICE para aislar el fallo CPU.
