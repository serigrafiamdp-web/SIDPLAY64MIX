# SIDPLAY64MIX — TEST01 / preparación de precarga

Estado: **ASSETS PASS (análisis y empaquetado)**. **RUNTIME PENDIENTE.**
Rama: `test/test01-preload-staging`. No modificar `master` hasta validar en VICE.

## Objetivo real

No tocar el timer de Glenn Rune. Mantener `checkdigits -> plt_advance`
para escoger el tema, pero sustituir la operación de disco en el límite
de tiempo por un **handoff desde RAM**, y realizar la siguiente carga
mientras PLAY del SID actual sigue ejecutándose.

Secuencia deseada:

1. SID A reproduciendo; precargar B mediante IRQ-loader.
2. Cuando vence el timer A: deshabilitar IRQ brevemente, copiar B al
   espacio de ejecución, aplicar metadatos PSID, INIT B, rearmar PLAY.
3. Durante PLAY B, precargar C (usando de nuevo el mismo buffer).
4. Repetir indefinidamente. Si la precarga no terminó, fallback
   al cargador original y mantener el estado de playlist consistente.

## Lo verificado del disco SIPLAY.d64

- 20 PSID; un ejecutable `SIDPLAY64-SD2IEC`.
- Los 20 PSID de esta imagen tienen load=$1000, init=$1000, play=$1003.
- Todos son de una subtune. El mayor payload es 6435 B.
- El perfil inicial A/B/C comparte speed bits `FFFFFFFF`.
- Estas propiedades **no son universales**; son una limitación explícita
  de TEST01. No transformar otros PSID silenciosamente.

Perfil inicial de archivos:

| rol | PSID del disco | bytes | carrier |
| --- | --- | ---: | --- |
| A | MINIMERCADO.SID | 3672 | MIX_A.PRG ($1000) |
| B | CHACABEZA.SID | 4442 | MIX_B.PRG ($5000) |
| C | COMEME (1).SID | 4737 | MIX_C.PRG ($5000) |

## Herramienta de staging entregada

```bash
python tools/preload_assets.py SIPLAY.d64
python tools/preload_assets.py SIPLAY.d64 --tracks 1 2 3 --output build/test01
```

La primera orden lista la colección y rechaza perfiles no compatibles.
La segunda crea los tres archivos PRG con una cabecera C64 estándar
de 2 bytes y el payload puro, más `TEST01_MANIFEST.json`.
El D64 original NO se modifica.

Estos PRG son **recursos de carga**, no un reproductor ejecutable.
El loader del futuro TEST02 podrá cargar B y C en una ventana fija
`$5000-$6FFF`, y el cambio de banco los copiará a `$1000-$2FFF`
en el límite del timer. El programa real no está conectado todavía.

## Contratos de SIDPLAY64 identificados

- `sidplay64.tas`, `checkdigits`: compara tiempo TOD con el límite.
- `src/plt_function.tas`, `plt_advance`: selección playlist;
  ahora termina en `jmp (wjp_load)`.
- `src/load-iec-serial.tas`: abre y lee cabecera PSID con KERNAL.
- `src/doheaderstuff.tas`: relocation y parámetros INIT/PLAY.
- `src/irq.tas`: IRQ CIA/PLAY, copia de ZP de 9 bytes.
- `restartTune` realiza limpieza de CIA/ZP y reinicialización.

**No insertar KrillLoad delante de la ejecución sin proteger estas
rutinas:** el player es autorreubicable y SIDPLAY mantiene estado
musical en `playbuf` / `editbuf` y vectores IRQ.

## Contratos SCUMM-PET-C64 comprobados

Referencia: `engine/main.ras` y
`docs/SCUMM_HIBRIDO_LOG.txt` de SCUMM-PET-C64.

- IRQ musical continuo con sincronización de Krill al raster $20.
- Un SID ejecutándose en $1000-$27FF, segundo preparado en
  banco independiente; handoff e INIT probados.
- Estado ZP separado del intérprete (en SCUMM usa $F0-$FF,
  en SIDPLAY el estado relevante es diferente).
- FADE en $D418 documentado, **no forma parte del TEST01**.
- BANK16B/C/D/E = FAIL por KrillLoad adicional en ciertas fases;
  no asumir que cualquier otra carga es segura.
- Krill's Loader ofrece fallback KERNAL para SD2IEC; verificar
  firmware, interrupciones y velocidad, no presumir soporte nativo.

## Próximos TESTS de runtime (todavía no PASS)

**TEST02 — IRQ LOADER ACTIVE:** instalar loader de Krill con el mapa
RAM real de SIDPLAY64, cargar B en $5000 mientras SID A sigue sonando,
revisar VICE (PLAY ticks y audio) y comprobar hash de RAM.

**TEST03 — IMMEDIATE HANDOFF:** conectar `plt_advance` con
`NEXT_READY`, conservar selección, ZP, INIT/PLAY y pantalla,
y activar B desde buffer sin tocar disco en el instante del timer.

**TEST04 — LOOP A→B→C:** reutilizar $5000 después del handoff,
precargar C durante B y repetir; verificar pausas y fallo del loader.

## Criterio de PASS

1. PLAY del SID actual se llama sin pérdida de ticks durante KrillLoad;
   sin clicks ni glitches atribuibles al loader.
2. B está íntegro y con checksum correcto ANTES del límite.
3. El cambio A→B al cumplir el timer NO inicia lectura física.
4. B→C vuelve a funcionar con el mismo buffer.
5. El timer, las teclas, selector N/R/M y el cargador convencional
   mantienen el comportamiento original si no existe NEXT_READY.

Ninguna de estas cinco condiciones puede declararse PASS solo por
haber preparado los PRG.
