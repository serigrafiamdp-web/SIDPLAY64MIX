# TEST47 — grupo difícil LOAD=$E000 (21 originales) — todavía NO PASS de VICE

Base inmutable: `MASTER-TEST46-143SID-LOAD-0FFF-PASS`, cuyo conjunto de 143 SID fue confirmado por el usuario.

## Hallazgo y alcance

En los 242 archivos del grupo `ALTA` de la galería original se encontraron **47 SID** con música en `$E000–$FFFF` (RAM debajo de ROM KERNAL).
- **21** tienen exactamente LOAD=$E000, el código musical termina en o antes de $F800, y INIT/PLAY dentro de $E000–$F7FF.
- Otros **3** terminan antes de $F800 pero empiezan con LOAD no estándar (E100/E8FF); no se incluyen aún.
- **23** restantes pueden entrar en la zona del font $F800–$FFFF, por lo que requieren otra estrategia.

## Implementación genérica

- Los 21 SID se conservan **idénticos byte a byte** a los contenidos del ZIP original `SID_GALERIA_FACIL_MEDIO_ALTA_SIN_DUPLICADOS.zip`.
- La rutina detecta la pareja original de LOAD (PSID header con palabra embebida $E000) y comprueba que INIT/PLAY apunten a $E000–$F7FF.
- Comprueba `fontpos==$f8`: la presentación debe tener charset situado en $F800.
- Sigue cargando la música con Krill en `$5300+` mientras el tema actual continúa sonando.
- Prefetch guarda exactamente 8KB en `$5000–$6FFF`; la nueva validación exige cero en `$6800–$6FFF`, para no escribir más allá del espacio musical seguro.
- En transición con IRQ detenido, pone $01=$35 (RAM bajo KERNAL y I/O visible) y copia solo 24 páginas desde `$5000–$67FF` a `$E000–$F7FF`; el charset $F800–$FFFF no se modifica.
- La rama anterior (`$0FFF`, `$1000–$1FFF`) conserva su código de transferencia previo.

## Imágenes D81

- `test47_e000_21_nuevos.d81` — 21 nuevos + `capriphol.sid` de referencia, 22 SID + `00player.prg`.
- `test47_biblioteca_162_sids.d81` — 143 PASS anteriores + **19** de los nuevos; los otros 2 están en el disco corto.
- Motivo: la biblioteca potencial de **164 SIDs** supera el máximo de 162 canciones validado en la lista del reproductor. No ampliar selector al mismo tiempo que la ruta de RAM alta.

## Estado y precauciones

- GitHub Actions compilación 64tass+PuCrunch y validaciones estáticas: SUCCESS en run 40754170609.
- D81 generados, directorio y BAM comprobados, extracción validada byte a byte. Archivo de referencia de salida: /mnt/data/test47_manifest.json.
- **NO** hay PASS de audio, portada, precarga o hardware. Esperar la prueba del usuario antes de integrar el MASTER.
- Nombres en minúsculas, sin numeración en SID; se conservan `cool tune` y `and again` fuera de la biblioteca.

## Candidatos que merecen prueba manual inicial

`ace_ii.sid`, `alloyrun.sid`, `auf_wieder.sid`, `krakout.sid`, `nefarious.sid`, `platou.sid`.
