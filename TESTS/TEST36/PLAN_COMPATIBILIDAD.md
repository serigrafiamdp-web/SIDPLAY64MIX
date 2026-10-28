# TEST36 — Plan incremental de compatibilidad de SIDPLAY64MIX

Fecha: 27-10-2026. **Sin cambios en el MASTER TEST35.**

## Lo que sí sabemos de los 19 SID del MASTER

Todos son PSID v2 con \`dataOffset=$007C\`, dirección de carga embebida \`$1000\`, INIT \`$1000\`, PLAY \`$1003\`, 1 subtune, 1 chip SID; el mayor payload mide 6435 bytes. En TEST35 se usa un buffer de 26 páginas (6656 bytes) y el cambio automático copia siempre a \`$1000\`. Por eso el MASTER funciona con ese conjunto homogéneo. Un archivo ajeno con INIT/PLAY/carga diferentes puede requerir una ruta totalmente distinta.

## TEST36 (presente): detector, sin cambiar el reproductor

\`python3 tools/test36_sid_audit.py archivo.sid\`

\`python3 tools/test36_sid_audit.py lote.zip --json reporte.json\`

\`python3 tools/test36_sid_audit.py TESTS/TEST35/SIDPLAY64MIX_TEST35.D64 --json reporte_master.json\`

El resultado clasifica en:
- \`TEST35_LAYOUT_CANDIDATE\`: coincide con el formato y el mapa actuales. No promete sonido correcto hasta probarlo en VICE.
- \`TEST37_DYNAMIC_ADDRESS_CANDIDATE\`: PSID aparentemente compatible con el espacio de memoria, pero necesita LOAD/INIT/PLAY variables, cambio de datos de cabecera o parser.
- \`NEEDS_NEW_ENGINE\`: RSID, tune que administra interrupciones, payload grande, mapeo potencialmente conflictivo, MUS, múltiples chips, etc.
- \`INVALID\`: cabecera no válida o corrupta. Versiones SID futuras no conocidas se marcan prudentemente como no soportadas por este auditor, aunque pueden ser válidas en otro reproductor.

**La clasificación es conservadora y estática**: un SID puede modificar registros, memoria compartida o IRQ en tiempo de ejecución y fallar pese a que la cabecera parezca válida.

## TEST37 (siguiente): motor de dirección dinámica por SID

1. Capturar para el archivo siguiente el encabezado completo: versión, \`dataOffset\`, LOAD efectivo (campo o palabra little-endian tras cabecera), INIT efectivo, PLAY, speed, canciones, modelo, reloj y datos de relocación.
2. La precarga Krill seguirá iniciándose a los 5 segundos, pero almacenará **metadatos junto a los bytes**. No tocar la canción activa.
3. En el cambio de canción, dejar de copiar siempre los 26 bloques a \`$1000\`: copiar solo el rango real al destino LOAD, respetando mapa de memoria y el aislamiento de IRQ. Bloquear de forma segura si ese rango pisa la GUI, Krill, el motor o el banco de precarga.
4. Antes de llamar a \`wjs_restartTune\`, actualizar los vectores \`initMus\` y \`playMus\`, el encabezado relevante, speed/tune y direcciones del nuevo SID. Asegurarse de que el buffer sobrevivió al cambio.
5. Sostener compatibilidad con PSID de carga embebida y con LOAD especificado en cabecera; offset v1 \`$76\` y v2+\`$7C\`. No copiar la cabecera como datos ejecutables.
6. Probar los 19 originales como regresión más un corpus variado de al menos 10 SID reales antes de marcar PASS.

## TEST38+: ampliar zonas protegidas y requisitos complejos

- Multi-subtunes y selección de pista.
- Tamaños y LOAD fuera de \`$1000-$2FFF\`, con estrategia de memoria/relocación más avanzada.
- Detectar PAL/NTSC, requerimientos de SID 6581/8580 y número de chips.
- \`PLAY=0\` / RSID con interrupciones propias solo mediante aislamiento de rutinas y entorno C64 real; **no es seguro tratarlos como un PSID normal**.

## Invariantes

- MASTER TEST35, sus 19 SID y el MASTER TEST19 no se modifican.
- Preservar \`N\` y \`M\`, 5 segundos, la precarga sin microcorte, y el orden de lista.
- No volver a introducir \`SEI\` largo durante carga/precarga.
- Compilar solo no equivale a PASS en VICE. Aislar los experimentos por rama y archivar cada regresión.

## Corpus necesario para avanzar

Subir un ZIP con 10–20 archivos SID variados, **sin convertir**, idealmente PSID v1/v2/v3/v4, diferentes direcciones de LOAD e INIT/PLAY, uno con varias subtunes y, aparte, RSID. El auditor seleccionará casos para TEST37 y separará los que necesitan un motor nuevo.
