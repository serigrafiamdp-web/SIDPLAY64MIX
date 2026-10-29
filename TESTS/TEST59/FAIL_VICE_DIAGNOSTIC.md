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
