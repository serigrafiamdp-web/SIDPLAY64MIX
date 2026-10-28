# TEST44 — PASS de reproducción confirmado por usuario (28-10-2026)

Rama congelada de referencia: `MASTER-TEST44-133SID-LOAD-ALINEADO-REPRODUCCION-PASS`.

La persona que prueba en VICE confirmó: **"funcionan esos 15 nuevos"**.
- Biblioteca anterior: 118 SID reproducidos (TEST43 PASS).
- Nuevos SID TEST44 con LOAD alineado por página: 15, reproducción confirmada.
- Total: 133 canciones de la biblioteca de prueba.
- Se conservan el banco de 8192 bytes, Krill y vectores INIT/PLAY del PSID.
- Sin alterar los SID originales.
- Los SID se nombran en minúsculas, sin numeración. El programa es `00player.prg`.
- `cool tune` y `and again` permanecen excluidos.

**Límite de la validación:** la frase de confirmación corrobora reproducción de los 15 SID. No se ha confirmado de manera independiente, en esta prueba, la precarga sin microcortes, la navegación manual/NEXT ni todas las transiciones en la colección de 133. No confundir compilación y prueba estática con PASS de audio.

**Siguiente etapa TEST45** (en rama independiente): LOAD no alineado, p.ej. $1340 y $18D0, y luego $0FFF con protección explícita. Mantener esta rama intacta.
