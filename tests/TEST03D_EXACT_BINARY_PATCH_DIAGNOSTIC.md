# TEST03D — parche binario mínimo sobre TEST03A PASS

**Estado:** armado binario y D64 verificados localmente; **VICE pendiente**.

## Reporte del usuario

- TEST03A en VICE: interfaz, audio normal y cambio por timer **PASS**.
- TEST03B-1: se cuelga ya en primera carga; **FAIL**.
- TEST03B-2: primera canción carga y suena, al pulsar N ralentiza,
  enciende drive brevemente y no cambia al vencer timer; **FAIL**.
  El código forzaba `plt_flag=2` durante Krill (Manual).
- TEST03B-3: pantalla con "Press 0-9 for colors", drive encendido y
  acceso continuo, sin cargar; **FAIL**.
- TEST03C: mismo bloqueo, pese a eliminar Krill y modificar el arranque;
  **FAIL**.

## Por qué cambia el método

En las pruebas B3 y C se recompiló código de arranque, se incorporaron
helpers distintos o se alteró `def_attractmode`. Aunque 64tass informa
PASS, eso no demuestra que el runtime de VICE funcione.

En este TEST03D **no se reensambla ni se reorganiza el código**.
Se reprodujo byte por byte el `SIDPLAY64_TEST03_SD2IEC.PRG` original
de TEST03A aprobado por el usuario:

`SHA256 fa0f95481b5ad429227304919bbc620dca634789ac9d9bd8208bcf2ff24020f0`
(tamaño 5336 bytes).

Se aplicó una diferencia de **dos bytes en el .o64 sin comprimir**,
en `start=$C81E`:

| Instrucción | TEST03A PASS | TEST03D |
|---|---|---|
| `LDX #imm` | `#2` Manual | `#0` Next |
| `LDA #imm` | `#$4D` ('M') | `#$4E` ('N') |

`STX plt_flag` y `STA plt_letter` conservan exactamente los mismos
operandos y direcciones. Todos los demás bytes son idénticos antes
de comprimir. La CI falla si el .o64 no coincide con el SHA del
TEST03A, o si el PRG reproducido con PuCrunch no coincide exactamente.

### Reconstrucción del D64

El D64 se **parcheó en el sitio** sobre el archivo
`SIDPLAY64MIX_TEST03A_ORIGINAL_UI.d64` (que había funcionado en VICE),
sin cambiar los 22 sectores asignados al reproductor, directory, BAM
ni siquiera cadenas track/sector o nombres. El nuevo PRG ocupa 5336
bytes, los mismos que TEST03A. **Los 20 SID se conservan byte por byte**.

D64 resultante:
- Tamaño: **174848 bytes**.
- SHA256: `57d274669cfb8096199130f8a56d710ae6729060dd3f0e0863c492adb0caaac2`.
- Solo **696 bytes del disco** difieren del D64 TEST03A,
  dentro de los sectores del primer PRG (PuCrunch recompresor).
- Conserva el arranque / pantalla de selección de colores original
  de TEST03A. **No** se saltea esa pantalla.
- **NO integra Krill**. Cambio de SID en modo N sigue usando
  carga tradicional de Glenn.

## Procedimiento comparativo de VICE

1. Cerrar VICE completamente (no solo soft-reset del C64)
   para restablecer también la unidad 1541.
2. Montar `SIDPLAY64MIX_TEST03D_BASE_PASS_NEXT.d64`.
3. `LOAD "*",8,1`, `RUN`.
4. Avanzar la pantalla de colores como se hacía con TEST03A PASS.
5. En el directorio, N debe aparecer ya seleccionado.
6. Cargar MINIMERCADO.SID y dejar que expire el timer.

**Si aún se cuelga leyendo el directorio:** repetir exactamente el
mismo proceso con el D64 original `TEST03A` sin modificaciones.
Si ambos fallan en la misma sesión, investigar estado de VICE y
protocolo del drive; si TEST03A funciona pero TEST03D falla, el cambio
de `plt_flag` a N en `start` altera algún flujo de directorio
antes de la primera canción y debe trasladarse a **después** del
primer carga/selección de canción.

No atribuir automáticamente todo bloqueo a Krill sin ese control.

## Archivos

- `tools/test03d_bytepatch.py`: script de parche binario SHA-gated.
- `.github/workflows/test03d-bytepatch-next.yml`: CI, compilación
  reproducible y PuCrunch comparativo.
- GitHub Actions run:
  https://github.com/serigrafiamdp-web/SIDPLAY64MIX/actions/runs/40430287486

NO fusionar a master sin validación VICE.
