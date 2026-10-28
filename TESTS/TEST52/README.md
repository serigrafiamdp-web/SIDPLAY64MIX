# TEST52 — SIDs originales de más de 8 KB (banco seguro de 9 KB)

**Estado:** GitHub Actions 64tass + PuCrunch y regresiones estáticas **PASS**. Imágenes D81 con sectores y directorio verificados. **No confirmado en VICE**. El MASTER `MASTER-TEST51-199SID-KRILL-3C00-PASS` permanece intacto.

## Cuello de botella resuelto en este test
- El reproductor TEST51 conserva sus rutas y staging original de 8192 bytes en `$5000–$6FFF`.
- TEST52 añade una ruta separada para **PSID v2 LOAD=$7A00–$7FFF**, INIT/PLAY reales >=LOAD y bajo $A000, con **hasta 9216 bytes de código musical** (36 páginas de 256 bytes).
- El scratch de lectura Krill `$5300–$77FF` se limpia con 37 páginas (antes 33), sin tocar estas músicas cuyo LOAD real empieza en $7A00 o superior.
- PSID se carga tal cual y se extrae su cuerpo desde `$53CC`. Para esta clase se copian 36 páginas a un staging nuevo `$4000–$63FF`, copiando de menor a mayor dirección porque el destino es inferior al origen.
- En NEXT, IRQ apagada durante traspaso, se copian esas 36 páginas al LOAD real exacto usando ZP $FD/$FE y la rutina previa. Las colas no utilizadas se rellenan con cero dentro del scratch.
- El staging $4000–$63FF está por debajo de los nuevos LOAD y fuera del simbionte $3000-$3BFF, Krill $3C00, caché $3E00, y fuera de los bancos compatibles TEST43–51 (música $1000-$2FFF, $8000-$9FFF, $A000-$BFFF, $E000-$F7FF).
- Esta ruta **no generaliza todavía** a archivos arbitrarios de 30–40 KB ni garantiza automáticamente los PSID con LOAD por debajo de $7A00; esas clases exigen más análisis.

## Los dos SID originales de prueba
| Archivo D81 | Origen | LOAD | INIT | PLAY | Tamaño |
|---|---|---|---|---|---|
| `hawkeye.sid` | `ALTA/hawkeye.sid` | $7AE0 | $7AE0 | $7AE3 | 8768 bytes |
| `comicbakery.sid` | `ALTA/comic_bakery.sid` | $7F00 | $7F00 | $7F03 | 8448 bytes |

No hay duplicación de estos dos con los 199 SIDs anteriores (verificado con firma LOAD/INIT/PLAY/SHA del cuerpo original). Los SID en D81 conservan bytes idénticos a los ZIP originales; nombres minúsculos sin prefijos numéricos, dentro de 16 caracteres.

## Entrega experimental
- D81: `TEST52_9KB_2_SIDS_NUEVOS_VICE.d81` (819200 bytes)
- Contenido: `00player.prg` nuevo, referencia `capriphol.sid` ya PASS y los dos nuevos.
- SHA256 D81 `df57fbf9c6088b9e7cb034295ad3d12b0b885e1b49b8be552a1723a8f48bf3ae`.
- SHA256 ONEFILE `72454157b3caceffaf6214cf26e1eb26203093b622f3a14e2c7db058c9ea5041`.
- GitHub Actions run `40776312441`: SUCCESS, compilación y regresiones estáticas.

## Qué comprobar en VICE
1. Arrancar con `capriphol.sid`, verificar portada y audio.
2. NEXT a `hawkeye.sid`; escuchar que INIT/PLAY y sonido continúan.
3. Mantener Hawkeye sonando >5 segundos para precarga de `comicbakery.sid` y confirmar que no se interrumpe la reproducción.
4. NEXT a Comic Bakery; verificar inicialización/audio y su precarga del siguiente SID.
5. Volver a la referencia y verificar que el camino anterior de 8KB sigue sano.

**No actualizar la contabilidad hasta que el usuario confirme**. Si TEST52 completo PASS, serían **201 SIDs compatibles acumulados**, no todos simultáneamente en el mismo D81; el selector sigue sin ampliarse.
