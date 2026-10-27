# Baseline original antes del port TRSE

Fecha: 2026-10-27

La referencia de código fuente auténtico se conserva sin modificaciones en la rama `baseline/glenn-sidplay64-v1.21-original`, apuntando al commit `aa607572dfdd09838456ca4a7033f5c97fc00a2e` (15/01/2018).

## Objetivo

**Primero reproducir SIDPLAY64 v1.21 original y después aplicar las mejoras de SIDPLAY64MIX.** La apariencia de la pantalla o la detección de PSID no equivalen a portar el programa.

## Etapas obligatorias

1. Compilar la fuente original 64tass tal cual: `sidplay64.tas`, `sidplay64.cfg`, módulos `src/*.tas`, recursos `bin/*.o64`. Usar `makeall.bat` (crea `timedate.clk`) y herramientas 64tass + PuCrunch. Crear un D64 de referencia con `c1541.mak` donde corresponda.
2. Ejecutar el binario original en VICE y verificar: selección real de disquetera (F1/F2/RETURN), preguntas originales, scroller y créditos, lectura de directorio, carga, reproducción, teclado, IRQ, y comportamiento de vuelta al menú.
3. Mapear direcciones y bancos de memoria y comparar el proceso del original con el modelo TRSE/OrgAsm, prestando especial atención al conflicto de zona $0200 cuando se instala Krill.
4. Adaptar módulos ASM reales de 64tass a OrgAsm, sin dibujar pantallas nuevas para reemplazarlos. Cada paso tiene que conservar la funcionalidad de referencia.
5. Solo después integrar mejoras: precarga de 5 segundos, M/N y carga genérica de SID originales sin archivos MIX. Usar TEST25 PASS solamente como referencia externa, no como nueva base de código.

## Entregables

Cada test TRSE debe ser un ZIP **autosuficiente** con la configuración .trse, main.ras, d64.paw y carpetas originales de recursos. No aceptar dependencias implícitas de una versión anterior. Adjuntar el status correcto: compilación en TRSE / ejecución VICE / pendientes.

## Nota

PORT02-04 son experimentos de pantalla y teclado; **no** se consideran un port correcto del programa original.
