# TEST63 — Límite real del selector y fallo en cadena de precarga

**Estado:** tres imágenes D81 generadas con validación de contenido, estructuras 1581 y BAM; **pendientes de prueba en VICE**. **No se modificó el ONEFILE**, ningún SID ni el MASTER58.

## Error detectado en TEST62

En `sidplay64.tas`, el compilado de TEST59 / ONEFILE TEST62 usa `defset=4` (SD2IEC, IEC, SIN REU), por lo que:

- `dirpos=$D000`
- `lastpos=$DA30`
- `maxentries=(lastpos-dirpos)/16=163` **archivos en total**, verificable también en `SIDPLAY64MIX.labels` generado por 64tass en CI. **El tope fiable es 162 SID más el 00player.**
- `flengde=$DA31` y `static_code_start=$DAED`. Las direcciones posteriores ya están reservadas para flags y subrutinas; cambiar a 200 sin rediseñar memoria/selector sobrescribiría esas regiones.
- El D81 del TEST62 tenía 168 entradas: 00player + 167 SID. **Sobrepasa en cinco entradas la capacidad anunciada por el ejecutable.** La implementación revisada comprueba `cpx #maxentries` y puede truncar lectura, por lo que **no se ha demostrado que haya escrito fuera de RAM**; tampoco podemos imputar los FAIL de posiciones 7–154 automáticamente a ese límite. Corregir la base del test antes de sacar conclusiones.

## Segundo posible problema: error de precarga persistente

`mix10_service` retorna sin intentar más cargas cuando `mix10_ready != 0`. En `mix10_service_failed`, escribe `mix10_ready=2` y borde rojo. Mientras no se reinicie ese estado (por ejemplo con una selección manual), la precarga deja de avanzar. Esto puede hacer que **un primer SID con fallo parezca arrastrar una larga cadena de SIDs**, aunque esos otros archivos suenen en un D81 diferente. Es una hipótesis fuerte fundada en código, no una prueba de causalidad hasta verificarla con VICE.

## Evidencia del usuario

En TEST62 con 167 SID, el usuario apartó **31 canciones que no cargaban o provocaban JAM**. Al armar otro disco dedicado con esas mismas canciones, indicó que **sí funcionaban**. Por tanto no clasificar los 31 individualmente como incompatibles ni borrarlos de `MUSICIANS.zip`. La distribución de FAIL en TEST62 incluye grupos consecutivos en posiciones 18–28 (11) y 45–50 (6), consistente con un error en cascada / secuencia (no demuestra causa exacta).

## Tres D81 de diagnóstico

Todos hechos a partir del D81 original del TEST62 reextrayendo los **bytes idénticos de cada archivo**, con encabezado BAM recomputado, cadena de sectores y directorio revalidados, y exactamente el mismo ONEFILE experimental TEST60 B / TEST59 de los discos anteriores. No se agregan canciones; no se revierte el filtro anterior de 50 SIDs.

| D81 | SIDs | SHA256 | Objetivo |
|---|---:|---|---|
| `TEST63_CONTROL_162_SIDS.d81` | 162 | `7bf3bfafa4f9c29f49f71027124addaef92c0158bc4e73c7a1c65099c1fe2be7` | Primeras 162 SIDs TEST62 en mismo orden: comprobar límite |
| `TEST63_GRUPO_A_84_SIDS.d81` | 84 | `0d41964bf106ef07296a49a282603e6686cd0d4af2feddea456846160b6fbfe6` | Posiciones impares originales, incl. capriphol |
| `TEST63_GRUPO_B_84_SIDS.d81` | 84 | `5230ed2394313cc0b4495f1a09bf2a1688ae76ae48431808d76b3bbe3a355b04` | capriphol inicial + posiciones pares |

La unión de los dos grupos de 84 incluye los **167 SID únicos de TEST62**, con capriphol duplicado expresamente como referencia de inicio. Cada D81 mide 819200 bytes, directorio <=163 archivos totales, BAM, cadenas y todos los archivos reextraídos PASS. `TEST63_LISTADO_MATRIZ.csv` relaciona posiciones originales y nuevas. `TEST63_TRES_D81_DIAGNOSTICO.zip` incluye todo.

## Interpretación de prueba VICE

1. Iniciar VICE de cero con CONTROL 162: comparar posiciones de fallos ya observados en TEST62. Si sigue fallando en posiciones <163, **el exceso de entradas no explica por sí solo los fallos**.
2. Iniciar VICE de cero con GRUPO A y luego B. Ambos están muy por debajo del tope de memoria del directorio y cambian las parejas adyacentes: si funcionan, investigar continuidad, precarga y estados del motor.
3. Anotar primer fallo, canción anterior, modo Enter/NEXT, borde, CPU JAM o simple no-carga. Opcional monitor `m $3ff0 $3fff`; los estados `$3FF2=$FF` y `$3FFD=02` indican error de precarga persistente.
4. **No incrementar compatibilidad ni borrar más SIDs antes de corregir la causa.**

## Futuro: más de 162 SIDs por D81

Una ampliación real del selector requiere **bancarizar/paginar el directorio** o reubicar tabla de 16 bytes/entrada y datos auxiliares fuera de la región `$D000–$DAED`; solo subir `maxentries` no es seguro. Mantener también en cuenta límites de 8 bits `maxfile`, `pos_cursor`, `offs_cursor`, `mix10_current` y `mix40_sid_count`. Recomendación: primero resolver los FAIL en cascada y comprobar TEST63; después diseñar un selector paginado manteniendo compatibilidad universal.
