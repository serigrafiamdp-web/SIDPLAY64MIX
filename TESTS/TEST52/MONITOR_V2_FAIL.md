# TEST52 V2 FAIL: VICE C64 y unidad 8, 28/10/2026

Monitor recibido del usuario después de pantalla negra y detención del disco:

```
(C:$7750) r
.;7750 c3 ff 00 f6 2f 36 11110000 219 002 235885799
(C:$7750) m $3ff0 $3fff
>C:3ff0 01 11 00 00 01 00 02 00
>C:3ff8 02 00 04 01 00 00 00 00
(C:$4000) dev 8:
(8:$b125) r
.;b119 ff 03 fe 8f 00 00 10100001 478833475
```

Análisis:
- PC $7750 del C64 permanece dentro del instalador Krill v184, en espera de CIA2/IEC (`BIT $DD00`, `BVS`).
- $3ff1=$11: se llamó al instalador pero no regresó a $12. $3ffc=0: todavía no activado. El código no alcanzó la precarga ni el handoff de 9 KB.
- $3ff4=1 identifica índice 1 (base cero), Hawkeye como pista inicial seleccionada. El directorio tiene `capriphol.sid` de referencia en posición 1, `hawkeye.sid` en posición 2, `comicbakery.sid` en posición 3.
- CPU unidad 8 aparece en torno a $B119; sin desensamblado de ROM y memoria del drive, no se puede atribuir causa definitiva.
- V2 restauró los seis bytes $7AE0-$7AE5 del instalador antes del JSR; como el PC queda dentro del instalador esperando IEC, esa restauración NO resolvió el bloqueo.
- Primero probar **arrancar seleccionando capriphol.sid**, pista de carga baja ya validada, y después cambiar manualmente a Hawkeye. Este test separa el conflicto de primera instalación de los problemas del nuevo buffer/precarga de 9KB, sin compilar otro PRG.
- Según resultados, diseñar TEST52 V3. No afirmar que Krill instalado desde $3C00 haya fallado: el fallo es antes de completar JSR $6000.
- MASTER-TEST51-199SID-KRILL-3C00-PASS inalterado.
