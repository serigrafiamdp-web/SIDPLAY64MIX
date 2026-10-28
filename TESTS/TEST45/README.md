# TEST45 — original LOAD no alineado (PRUEBA, NO PASS)

Base: MASTER-TEST44-133SID-LOAD-ALINEADO-REPRODUCCION-PASS (usuario acaba de confirmar que los 15 nuevos se reproducen CON PRECARGA, 28-10-2026).

Cambios TEST45:
- Mantiene intactos código, timing e IRQ del TEST44 cuando el LOAD termina en 00 (nuevo low=0, exit temprano).
- Acepta PSID originales con LOAD desde $1000 hasta $1FFF (incluido, sin alineación a páginas), INIT/PLAY originales dentro del banco $1000-$2FFF.
- Tras el desplazamiento por páginas de TEST44, comprueba el excedente superior y desplaza entre 1 y 255 bytes hacia arriba, copiando los 8192 bytes de atrás hacia adelante y con IRQ activo.
- El cambio de canción mantiene la misma copia $5000->$1000 y el mecanismo Krill existente.
- No se convierte, reescribe ni parchea el archivo SID.
- Excluidos cool tune y and again. Nombres externos todos minúsculos, sin número en nombres SID.
- Candidatos sin alinear nuevos para primera prueba: all_together_tune_2, double_dragon, gr-magnetic_fields, layla_mix, playboy_the_game, s-express.

**Limitaciones:** no se admite todavía LOAD=$0FFF ni LOAD alto que invada Krill/UI, ni el caso RSID PLAY=0. No afirmar PASS antes de probar en VICE. Algunos SIDs pueden modificar RAM/IRQ de forma incompatible aun teniendo cabecera aceptada.
