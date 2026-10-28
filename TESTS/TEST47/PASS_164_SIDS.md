# MASTER TEST47 — 164 SID compatibles · PASS del usuario

Fecha: 2026-10-28.
Congelado desde la rama experimental `test/test47-high-e000-banked` después de la confirmación explícita del usuario: **"pass"**.

## Resultado
- MASTER TEST46: **143 SID** confirmados previamente.
- TEST47: **21 nuevos SID** con LOAD original en `$E000`, INIT/PLAY en `$E000-$F7FF`, confirmados por el usuario después de recibir los D81 de prueba.
- **Total acumulado: 164 SID compatibles** en el conjunto de pruebas.

## Límite de biblioteca actual
El reproductor de lista larga se ha probado hasta **162 SID por disco**, por lo que todavía no debe afirmarse que los 164 están reunidos en **un solo** D81 operativo:
- `test47_e000_21_nuevos.d81`: 21 nuevos + 1 referencia conocida.
- `test47_biblioteca_162_sids.d81`: 143 anteriores + 19 de los nuevos.
Los otros 2 nuevos se incluyen en el disco corto. Pendiente: investigar/ampliar el selector si se quiere una biblioteca única de 164 o más archivos.

## Cambio técnico
- Detección de PSID con LOAD original en `$E000`.
- Prefetch Krill al banco `$5000-$6FFF`; validación de longitud y cola no nula.
- Copia en handoff a RAM bajo ROM KERNAL en `$E000-$F7FF`, protegiendo el charset en `$F800-$FFFF`; detección de `fontpos=$F8`.
- Conserva las rutinas de LOAD de TEST46: `$0FFF`, `$1000-$1FFF`.
- SIN modificación del contenido de los archivos SID, nombres sin numeración y en minúsculas.
- `cool tune` y `and again` siguen excluidos.

**Estado:** PASS informado por el usuario para TEST47 después de las pruebas en VICE; no equivaler a confirmación de hardware físico independiente ni afirmar que la biblioteca única de 164 está validada.

**Instrucción de mantenimiento:** dejar esta rama MASTER intacta; toda mejora debe ir en rama TEST posterior.
