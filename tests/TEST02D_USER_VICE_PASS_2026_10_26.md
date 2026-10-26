# TEST02D — Resultado auditivo observado en VICE (26 octubre 2026)

**Estado: PASS funcional de secuencia A → B → C; calibración de tempo pendiente.**

Reporte directo del usuario al probar `SIDPLAY64MIX_TEST02D_50PCT_KRILL.d64` en VICE:

- La secuencia llega a reproducir varios SID.
- Se observa actividad de carga de SID entre pantallas/transiciones y las canciones suenan.
- Las primeras canciones del disco se oyen más lentas al usar el divisor global al 50%.
- La canción final, que corresponde al checkpoint de pantalla **K**, tiene
  una velocidad perceptualmente más próxima a la correcta.
- El usuario valora la precarga y el cambio de SID como el éxito principal.
- No se midieron todavía con contador de VICE las llamadas efectivas a
  PLAY ni se compararon muestras de audio con el reproductor de Glenn.

## Interpretación y próximos pasos

No asumir que el divisor de frecuencia 1/2 aplica a todo SIDTracker64,
ni que la velocidad oficial de cada canción es 30 Hz sin medirla.

**Conservar dos referencias independientes:**
- TEST02C PASS: A→B→C con tasa inicial CIA 60 Hz.
- TEST02D PASS funcional: A→B→C con PLAY cada 2 IRQ (~30 Hz).
  Preferencia auditiva: canciones A/B en TEST02C más cercanas que en
  TEST02D; tercera canción C, asociada a K, más cercana en TEST02D.

**No tocar el timer de playlist original del SIDPLAY64.**
Para integración TEST03 el disparador correcto sigue siendo
`checkdigits -> plt_advance`. Se debe conservar su lógica de
selección next/random y hacer handoff desde buffer solo cuando
`NEXT_READY`, cargando el sucesor en segundo plano. El perfil de
frecuencia se decidirá por SID, una vez medido.

**Riesgos que faltan resolver en integración:**
- autorreubicación del reproductor según páginas libres del SID;
- prueba de convivencia de Krill y IRQ/Zero Page de Glenn;
- precarga antes del timer sin pisar música o pantalla;
- metadatos PSID (INIT/PLAY, subtunes, speed, PAL/NTSC);
- manejo de FIN/SID incompatibles y fallback sin perder playlist;
- garantizar que el siguiente candidato elegido para RANDOM sea el
  mismo que se precargó.
- SD2IEC real versus unidad 1541 con emulación.

El PASS indicado es **observado por el usuario en VICE** para el
harness autónomo, no certifica integración en el SIDPLAY64 original.
