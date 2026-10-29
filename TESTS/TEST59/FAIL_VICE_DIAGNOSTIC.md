# TEST59 — FAIL en VICE — NO PROMOVER A MASTER

**Fecha:** 2026-10-29. El usuario probó `TEST59_10_SIDS_0F80_REGRESION_UNIVERSAL.d81` y reportó explícitamente: **«fail no cargarn los sid»**.

**Estado:** TEST59 FAIL. **No contar ninguno de los diez nuevos como PASS.** El último MASTER universal confirmado sigue siendo `MASTER-TEST58-232SID-4000-4FFF-PASS`. `BUGGY.SID` sigue excluido por JAM de una prueba anterior.

## Verificación posterior al fallo

- El D81 original tiene 819200 bytes, directorio correcto, 20 archivos (00player + 19 originales).
- Se verificó extracción y firma de todos los PSID en el D81; los contenidos no están truncados.
- El `00player.prg` extraído del D81 coincide byte a byte con el ONEFILE original de la compilación CI (SHA256 `bfaac11797663c3bc98ed84da99c0b17b81530b1228c7b974d739e5deab52bc1`).
- El código compiló sin errores GitHub Actions run `40814507627`.
- Se reprodujo por simulación de copias de RAM el staging para `magnificent.sid`, `chopper.sid`, `lightspeed.sid` y `aurum.sid`: bytes restaurados en $0Fxx y $1000+ coinciden en una reconstrucción estática con el PSID original.
- Nada de eso demuestra que los 10 nuevos sean compatibles en VICE: **reproducción falló**, por lo que es necesario revisar la ejecución runtime y/o zonas de memoria.

## Cambio que intentó TEST59

Extender el prefijo del TEST57 desde 16 hasta 128 bytes para LOAD $0F80–$0FFE, con suma de 16 bits de puntero origen $53CC y copia de datos a $5000.

**Posibles líneas de investigación, NO diagnosticadas aún:** aceptación de cabecera, inicialización del SID bajo $1000, interferencia de RAM $0F80–$0FEF con código del reproductor, transición NEXT/manual y resultado del Krill. No afirmar una causa hasta tener traza de VICE.

## Para el próximo diagnóstico

Al seleccionar un SID que falle, abrir el monitor de VICE y capturar los registros de diagnóstico:
`m $3ff0 $3fff`
y opcionalmente `r`.
Valores que se escriben en $3FF7 al pasar por los estados de staging: $10 entró, $20 nombre listo, $30 scratch borrado, $40 antes de Krill, $50 retorno de Krill, $60 staging normal completado, $62 staging 9KB completado, $E0 fallo de validación o lectura. $3FF2 cambia a $FF tras el error, y $3FFC indica modo activo. Examinar esos bytes para diferenciar fallos de carga, cabecera, staging y ejecución.

No congelar esta rama ni incorporar candidatos hasta que haya una prueba real PASS. Mantener MASTER58 como baseline.


## Diagnóstico aportado por usuario (magnificent.sid)

Síntoma reproducido por usuario: selecciona `magnificent.sid`; intenta cargarlo, **no reproduce música y vuelve a la portada del player**.

Monitor de VICE inmediatamente después:

```text
(C:$c9b2) m $3ff0 $3fff
>C:3ff0  01 11 00 00  01 00 02 00
>C:3ff8  02 00 14 01  00 00 00 00
(C:$4000)
```

Significado basado en los **marcadores de la fuente exacta TEST59**:

- `$3FF0=$01`: `mix10_prepare` ejecutado (payload Krill preparado).
- `$3FF1=$11`: `mix10_activate` encontró el archivo inicial en directorio (`mix31_find_loaded_index`); todavía no alcanzó el marcador $12 de la instalación de Krill.
- `$3FF4=$01` y `$3FF6=$02`: se seleccionó canción índice 1, directorio índice 2: `magnificent.sid`.
- `$3FFA=$14`: 20 entradas de directorio detectadas (00player + 19 SID).
- `$3FFB=$01`: payload inicial preparado.
- `$3FFC=$00`: Krill todavía **no activo**.
- `$3FF7=$00`: no se ha iniciado `mix10_stage_pending` (que marca $10, $20, $30, $40, $50, $60, $E0).

**Conclusión diagnóstica acotada:** fallo ocurre **durante la carga inicial/instalación de Krill, ANTES del nuevo tratamiento TEST59 de prefijos**. El programa deja `$3FF1=$11` justo antes del `JSR $6000` del instalador; si este regresara normalmente, la rutina escribiría $12 (éxito) o $E0 (error). No alcanza ninguno. No afirmar causa física/raíz sin nueva evidencia.

**Próxima prueba discriminatoria SIN modificar nada:** reiniciar VICE con el D81 actual, seleccionar **`capriphol.sid` como primer tema** (primera entrada musical, ya PASS), comprobar si `$3FF1=$12` y `$3FFC=$01`; después seleccionar `magnificent.sid` y observar si se activa la rutina de precarga (`$3FF7` cambia). Esto separa el problema del instalador inicial de las rutas de carga posteriores. Si también falla con capriphol, volver a comparar ejecutable TEST58 vs TEST59 y la ubicación del instalador o tamaño total, antes de tocar la nueva ruta de prefijos.

**MASTER58 sigue intacto y válido; TEST59 sigue FAIL.**
