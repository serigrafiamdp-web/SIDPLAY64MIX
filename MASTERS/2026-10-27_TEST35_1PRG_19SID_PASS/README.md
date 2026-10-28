# MASTER SIDPLAY64MIX — TEST35 — 27/10/2026

**Estado: PASS en VICE reportado por el usuario el 27/10/2026.**

Este es el checkpoint **1 PRG + 19 SID originales** con el reproductor original Glenn Rune Gallefoss SIDPLAY64 y Krill fastloader, precarga de la siguiente cancion a los 5 segundos y reproduccion sin microcorte perceptible en la prueba realizada.

## Entregables congelados

- `SIDPLAY64MIX_TEST35.D64`: disco de 174848 bytes, 1 PRG + 19 archivos SID originales.
- `SIDPLAY64MIX_TEST35_PROYECTO_COMPLETO.zip`: fuentes ASM, recursos Krill, PRG, D64, mapa de simbolos, informe y scripts de construccion.
- `REPORT.json`: reporte original de integridad de la compilacion (dice "VICE UNTESTED" porque se genero **antes** de la validacion humana).
- `SHA256SUMS.txt`: huella del D64 exacto archivado.

### Validacion

- El usuario confirmo expresamente **PASS, anda perfecto** en VICE, despues de observar precarga, cambio automatico y ausencia del microcorte previo.
- El GitHub Action de TEST35 termino SUCCESS (verificado estaticamente); la compilacion automatica NO sustituye la prueba en VICE.
- D64 SHA-256: `994e59747e497c7adf2e0b22851a7ddc7ced1e5b55f6998b311ac9e13ac5e040`.
- Los 19 SID y sus cadenas de sectores son identicos a los del MASTER TEST19.
- Codigo fuente y artefactos proceden del commit probado `49ae0cb7efe10f75236a2991c3feaa5f61d5403f`, rama `test/test35-irq-friendly-prefetch`.

### Limites actuales y reglas de conservacion

- PASS funcional para la secuencia probada; **NO implica** validacion exhaustiva de todos los SID ni formatos arbitrarios.
- Conservar intacto el MASTER previo `MASTERS/2026-10-27_PASS/` (TEST19, multiples archivos).
- Nunca editar estos artefactos del MASTER ni trabajar directamente sobre sus binarios. Crear ramas `test/TEST36...` para cualquier cambio futuro.
- No volver a introducir largas regiones `SEI` durante preparacion/precarga de 27 paginas y copia de 26 paginas: TEST35 permitio las IRQ del SID durante esas tareas.
- Preservar modo Manual (M), Next (N), seleccion de cualquier archivo, ciclo ultimo SID -> primero y carga de siguiente a los 5 segundos.

## Proxima auditoria

Revisar sin cambiar este MASTER: (1) recorrido completo de M/N y selector manual; (2) borde/cursor al cambiar automaticamente; (3) carga repetida de 19->1; (4) invariantes RAM/ZP de IRQ durante Krill; (5) compatibilidad de futuros PSID con otros load/init/play; (6) pruebas de stress con multiples ciclos.

**Este registro se creo despues del PASS en VICE y no altera el D64.**
