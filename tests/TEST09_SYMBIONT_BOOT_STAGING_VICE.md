# TEST09 — SIMBIONTE PREARRANQUE, GLENN ORIGINAL EXACTO

**Estado: CI 64tass PASS, D64 generado y revalidado, VICE aún sin probar.**  
**Fecha de preparación:** 27/10/2026.  
**D64:** `SIDPLAY64MIX_TEST09_SIMBIONTE_GLENN_STAGE.d64`  
**SHA256:** `01c8581eb340dc18c71dfa9cc43215b5406590b22799b2434bd48438efc5e336`.

## Hipótesis propuesta por el usuario

Durante el inicio original de Glenn Rune (elección de unidad,
segundo SID, RSID, opción de teclado/joystick, colores) se pueden
**preparar** los componentes Krill antes del directorio, pero
**NO activar el drive-code** mientras Glenn siga usando sus
lecturas IEC vía KERNAL.

`src/init.tas` llama `devicecheck`, preguntas y elección de color;
luego salta a `start` en `sidplay64.tas`, donde `src/dir-iec.tas`
usa `ROM_OPEN`, `ROM_CHKIN` y `ROM_CHRIN` antes de mostrar los archivos.
La reubicación dinámica del reproductor ocurre durante la carga de
un SID a través de `src/doheaderstuff.tas`. Instalar el protocolo
Krill **en el drive** antes de estas operaciones sin sustituir su
implementación ROM puede colgar Glenn.

## Implementación de este control (sin modificar Glenn)

Archivos fuente:
- `tests/test09_boot0.tas`, BASIC-compatible en `$0801`.
- `tests/test09_symbiont_stage1.tas`, cargado en `$7C00`.
- `.github/workflows/test09-symbiont-preboot.yml` compila con 64tass.

Secuencia:
1. BOOT carga SYMBIONT y ejecuta su código en `$7C00`.
2. SYMBIONT carga el residente Krill en `$9000`; copia
   512 bytes a `$8400` para no perderlo cuando Glenn empiece a
   descomprimir su ejecutable en `$9000`.
3. Carga INSTA en `$6000`; NO ejecuta todavía su entrada.
4. Carga el **PRG comprimido original exacto** `GLENN`
   mediante KERNAL a zona temporal `$3000` y lo copia a `$0801`.
5. Pone marca `SYM1` y banderas en `$8B00–$8B07`
   (son valores diagnósticos, NO un protocolo activo).
6. Salta a `$080D` y deja continuar TODO el programa original.

**No hay Krill en la 1541 todavía.** Es un control indispensable
antes de instalar el código de drive, enganchar el timer o realizar
prefetch; NO mejora aún tiempos de canción.

Precauciones: el destino `$8400` es candidato a staging solo para
esta prueba. El reproductor de Glenn se puede reubicar según las
cabeceras SID y podría sobrescribir esa memoria más adelante.
El TEST09 no afirma persistencia del residente con cualquier SID.
Además, los datos del residente deben volver a su dirección de
ejecución prevista antes de instalar Krill con la secuencia adecuada;
esta prueba no ejecuta dicho procedimiento.

## Verificación estática

- Compilación TEST09 en Actions:
  https://github.com/serigrafiamdp-web/SIDPLAY64MIX/actions/runs/40442878773
  **SUCCESS** (después de corregir ZP indirecto 6502).
- BOOT: 69 bytes, cabecera `$0801`.
- SYMBIONT: 237 bytes, cabecera `$7C00`.
- INSTA: 6.888 bytes con header `$6000`, región termina `$7AE5`.
- RESIDENT: 497 bytes con header `$9000`, cabe en 512.
- GLENN: **5.336 bytes idénticos byte a byte al TEST03A VICE PASS**,
  SHA256 `fa0f95481b5ad429227304919bbc620dca634789ac9d9bd8208bcf2ff24020f0`.
- D64: **35 pistas, 174.848 bytes, 24 entradas PRG, tres sectores de
  directorio y BAM correctos**; relectura de las 24 cadenas verifica
  cada byte, sin duplicaciones.
- **19 PSID** de TEST03A idénticos byte por byte, sin conversiones.
- 20 entradas del disco original (GLENN+19 SID) preservadas
  sin cambios de contenido y precedidas de cuatro archivos de bootstrap.

## Prueba VICE

1. Cerrar VICE, abrir C64 PAL con True Drive Emulation, montar el
   `SIDPLAY64MIX_TEST09_SIMBIONTE_GLENN_STAGE.d64`.
2. `LOAD "*",8,1` / `RUN`.
3. Observar carga inicial BOOT → SYMBIONT → RESIDENT, INSTA, GLENN.
4. Confirmar pantalla original y selección de unidad de Glenn.
5. Confirmar resto de opciones, colores y lectura de directorio.
6. Seleccionar MINIMERCADO.SID y comprobar música a tempo original.
7. Observar que el cambio automático según Glenn aún usa carga normal.
8. Si alguna etapa falla, hacer captura de VICE y revisar `$8B00-$8B0F`
   con monitor para localizar el punto de bloqueo.

**Es control de compatibilidad, no TEST09 de precarga completa.**
No atribuir PASS hasta que usuario pruebe VICE.

## Próximo paso

Con arranque PASS, instrumentar estado **DIR_READY** y después
**SONG_STARTED** en puntos seguros. Una vez el primer SID ya
esté cargado, habilitar protocolo Krill sin tocar los ROM OPEN
posteriores: Glenn debe utilizar una nueva capa de lectura de
directorios bajo Krill o una conmutación DOS segura. No reinstalar
ciegamente ni utilizar ROM_LOAD normal tras takeover. En esta
transición hay que mapear explícitamente: $9000 residente frente
al código del reproductor original, $8400 backup, $6000 installer,
$5000 stage y relocador de Glenn.

**MASTER y milestones TEST05/06/07 sin modificaciones.**
