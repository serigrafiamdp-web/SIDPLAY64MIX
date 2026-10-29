# TEST55 — Experimento aislado: recuperar música original $3000–$3BFF

**Estado:** compilación 64tass + PuCrunch PASS, regresiones estáticas y D81 íntegro verificados; **pendiente de confirmación de reproducción en VICE**. No elevar a MASTER todavía.

## Base y objetivo

- Base congelada `MASTER-TEST54-207SID-2000-2FFF-PASS`, que permanece intacta.
- Auditoría de `MUSICIANS.zip` (56.568 SID) encontró **610 archivos PSID** con código <=8192 bytes, INIT y PLAY dentro del payload y LOAD en `$3000–$3BFF`. De ellos, **152** tienen todo el código bajo `$3C00`; **151** son de una única SID según campos de cabecera y sin error. Cifras de compatibilidad potencial, no PASS.
- En el MASTER54, el simbionte ejecutable está en `$3000–$3BFF`, por lo que esta música lo sobrescribe y no se puede admitir ampliando simplemente el intervalo de LOAD.

## Método TEST55 (variante de laboratorio, NO definitiva)

1. Recompilar **solo en rama experimental** el simbionte completo en `$8000–$8BFF` con símbolos ensamblados a las nuevas direcciones. Así quedan libres `$3000–$3BFF` para la música seleccionada.
2. Evitar que su fuente coincida con la copia inicial de Krill: mover el backup de 495 bytes de `$8800–$89FF` a `$7C00–$7DFF`. La rutina `mix10_prepare` lo copia desde la nueva dirección a `$3C00–$3DEE` **antes del primer SID**, con Krill vivo idéntico en `$3C00`.
3. Detectar el PSID original LOAD $3000–$3BFF; validar sus INIT y PLAY dentro de esta región y no anteriores al LOAD.
4. Usar la alineación por página/byte de TEST44–45 con `virtual LOAD=real-$2000`, almacenar 8192 bytes en staging $5000–$6FFF y verificar **$5C00–$6FFF íntegramente cero**. Por lo tanto, la música real no puede alcanzar el Krill en $3C00.
5. Al hacer NEXT, transferir exactamente las 12 páginas de `$5000–$5BFF` a `$3000–$3BFF`. No se cambian los bytes de los originales.

### Advertencia esencial: esta variante NO es el reproductor universal

Como el simbionte está en $8000, **reproducir SIDs que usen $8000–$8BFF lo sobrescribiría**; estas familias habían pasado entre TEST49–51. Tampoco se ha comprobado la coexistencia con todos los SIDs grandes. El objetivo de este disco es **demostrar o refutar la reubicación de código para esta familia**. Un PASS permitiría estudiar una solución definitiva que seleccione dónde reside el simbionte según los conflictos de cada canción. **No afirmar 213 SIDs compatibles en una sola versión**, ni reemplazar el MASTER54 con esta rama.

## D81 experimental

Archivo: `TEST55_6_SIDS_SIMBIONTE_3000.d81`, 819.200 bytes, SHA256 `172f5cab4d54a83db2820987c44b3300a29f3b3365dfb03044f933fe521bccac`.

- `00player.prg`, SHA256 `1a9301af6e529450f3c2d03568b7c6e6384c9c286e80e44ced9896423fd0e855`.
- `capriphol.sid` de referencia ya confirmado.
- Seis SID originales de `MUSICIANS.zip`, sin modificar:

| D81 | LOAD | Fin exclusivo |
|---|---|---|
| `cybertron.sid` | $3000 | $3491 |
| `kungfumaster.sid` | $3038 | $314A |
| `spacetravel.sid` | $3100 | $38E6 |
| `lawntennis.sid` | $3200 | $3B67 |
| `budsintro.sid` | $3400 | $392A |
| `grogsrevenge.sid` | $3500 | $3B91 |

Los archivos se reextrajeron del D81 y compararon **byte a byte** con los originales; BAM y cadenas de sectores de 80 pistas/40 sectores verificadas. Nombres de 16 caracteres o menos, minúsculas y sin numeración.

Compilación CI GitHub Actions `40794309331`: SUCCESS, no prueba reproducción.

## Siguiente prueba de usuario

Arrancar VICE con el D81. Elegir primero `capriphol.sid` (regresión de entrada y activación de Krill); luego probar los seis nuevos, seleccionando manualmente y dejando al menos una transición automática/preload de 5 segundos. Informar cualquier pantalla negra, bloqueo o música muda.

Si PASS: preparar una arquitectura **con dos ubicaciones alternativas del simbionte** antes de integrar esta familia al MASTER. Si FAIL: monitor `r`, `m $3ff0 $3fff`.

MASTER54 sigue congelado; selector no se amplía.
