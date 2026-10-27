# Arquitectura propuesta — SIDPLAY64MIX sin espera entre canciones
Fecha: 2026-10-26 | Estado: **investigación, sin firmware nuevo ni PASS en VICE**  
Repositorio: https://github.com/serigrafiamdp-web/SIDPLAY64MIX  
**Master sin cambios. TEST03A, TEST02C, TEST02D intactos.**

## Meta exacta

Eliminar **la espera de disco al cambiar de canción**. El timer original
de Glenn elige siguiente tema; cuando llegue el instante de cambio,
el próximo SID ya debe estar completamente disponible en RAM y preparado
para INIT/PLAY. La lectura del disco no puede ser parte del camino crítico.

En una C64 con un solo chip SID, una transición INIT a otro tema puede
hacer reset de voces y envolventes, de modo que «no esperar al drive»
no garantiza crossfade musical sin discontinuidad. Distinguimos:
1. cambio sin accesos de disco (meta obligatoria);
2. cambio dentro de 1 frame/tick de música (meta de calidad);
3. crossfade verdadero entre dos temas (fuera de alcance con un solo SID).

## Por qué fallaron nuestras integraciones

1. El TEST03A tuvo **PASS del usuario**: GUI original, canciones a
   velocidad original y avance normal del timer; **NO había precarga**.
2. TEST02C y TEST02D tuvieron **PASS del usuario** en el motor
   autónomo Krill + IRQ + 3 SID. Se demostró que música puede sonar
   mientras se cargan datos de disco.
3. En TEST03B se instalaron rutinas Krill dentro de la GUI original,
   donde ya había dependencias de KERNAL, vídeo, relocación y IRQ.
   TEST03B-1 bloqueó incluso la primera canción.
4. TEST03B-2 consiguió primera canción normal, pero al entrar en modo N
   un fragmento del código fuerza `plt_flag=2` (manual) y por tanto
   bloquea su propio avance. La instalación con `SEI` también coincide
   con ralentización auditiva; duración y causa exacta sin instrumentar.
5. TEST03B-3/C/D: varios bloquearon el inicio y la lectura del directorio,
   incluso sin Krill activo. Por tanto **no se puede concluir que toda
   falla restante sea de Krill**; conviene medir el estado de VICE y
   rutina exacta antes de parchear.
6. El modo N desde el principio es peligroso en el código Glenn:
   `src/displayfiles.tas` cae al código de timer `checkdigits`
   incluso durante lectura incremental del directorio;
   `plt_advance` salta al cargador normal. Si N está activo demasiado
   pronto, puede actuar antes de que haya canción/lista estable.
   Es **hipótesis causal**, no se ha medido el PC en VICE.
   Debe existir estado PLAYLIST_READY separado del indicador N.
7. El PRG descomprimido original usa el entorno de instalación cerca
   de $9000; el Krill residente experimental también $9000. No
   solapar ambos sin un plan de vida útil y memoria.

## Arquitectura recomendada: precarga por bancos (NO Krill inicialmente)

### Experimento A: playlist finita 3-4 temas sin esperar al disco

1. **Antes de emitir la primera nota**, cargar y verificar varios
   SID *independientes* en regiones de RAM no solapadas.
2. **No cambiar de programa musical mediante la carga KERNAL**.
   El timer de Glenn selecciona próximo índice en tabla RAM.
3. En cada cambio, el motor:
   - detiene llamadas PLAY del tema saliente por un instante;
   - ajusta la tabla de punteros INIT / PLAY / frecuencia por canción;
   - llama INIT de la nueva canción con su subtune;
   - restablece sus llamadas PLAY y continúa el reloj de GUI;
   - **no toca la unidad 1541** durante la transición.
4. El modo N se marca en la interfaz al comenzar, pero el detector de
   timer queda deshabilitado hasta que haya un tema activo y lista
   precargada válida.
5. Para la prueba, las canciones son las conocidas MINIMERCADO,
   CHACABEZA y COMEME de `SIPLAY.d64`; todos los PSID de ese disco
   empiezan originalmente en $1000 y comparten INIT $1000/PLAY $1003,
   por lo que **NO se pueden ejecutar a la vez desde sus direcciones
   originales**. Deben reexportarse/reubicarse.

### Cómo conseguir direcciones independientes

Opción preferida si existe el proyecto original en SidTracker64:
SidTracker64 permite desde Settings elegir el **SID file start address**.
Reexportar tres SID con load-address diferentes, por ejemplo $1000,
$3000, $5000, y verificar:
- que cada .sid tiene load/init/play corregidos;
- que realmente reproduce bien aisladamente;
- que código y datos no escriben fuera del bloque elegido;
- que no pisan la GUI, charset, stack, directory y ZP.
Fuente oficial:
https://apps.apple.com/us/app/sidtracker64/id955421205
(historial: 'Set sid file start address from settings menu').

Si NO están los proyectos .s64, usar herramienta SIDReloc, que
reescribe referencias internas de código y opcionalmente Zero Page.
No prometer soporte de todos los SIDs; autor indica que puede fallar
con código comprimido o accesos especiales.
Fuente primaria: https://www.linusakesson.net/software/sidreloc/

Tabla de slots **candidata** para una prueba restringida:

| Banco candidato | Rango | Condición |
|---|---|---|
| SID A | $1000-$2FFF | Sí, actual A dentro de este rango |
| SID B | $3000-$4FFF | Reexportar/reubicar y comprobar integridad |
| SID C | $5000-$6FFF | Reexportar/reubicar y comprobar integridad |
| SID D futuro | $7000-$8FFF | Solo si hace falta y mapa de memoria PASS |

**NO asumir que se pueden agregar dos más en $9000 o $B000**:
el arranque de Glenn y rutinas cargadoras han usado $9000;
regiones con ROM/IO y el driver reubicado/GUI necesitan tratamiento
explícito. El número 6 es posible para algunos reproductores
y archivos pequeños, no es garantía para SID arbitrarios.

Incluso cuando varias canciones están en RAM, solo se activa una
rutina PLAY en cada tick (hardware 1 SID). Al llamar INIT el motor
puede resetear SID; para experimentar con cambio perceptualmente
continuo, medir diferencia en ciclos y estados SID.

### Experimento B: sin proyectos reexportables

Si todas las canciones comparten dirección $1000 y fallan en la
reubicación, guardar SID B/C como datos en bancos separados
(previamente cargados, pero SIN ejecutarlos), y copiar al área
ejecutable $1000 cuando vence el timer. Esto evita **espera de
disco**, pero una copia de ~6 KiB consume ciclos y puede generar
una interrupción perceptible; NO afirmar cambio imperceptible.
Mejorar copia ASM o precalcular escenarios; medir en VICE.

## Arquitectura final: playlist ilimitada y precarga concurrente

Una vez confirmado el experimento A (cambio sin disco):

1. **Capa de almacenamiento separada**: conjunto de bancos/slots
   READY, PLAYING, LOADING, ERROR, FREE, con identidad del archivo,
   rango de RAM, CRC, INIT/PLAY/clock/tempo y subtune.
2. Reproducir A, cargar B a un slot libre **antes de vencer timer**.
3. Si B está READY al vencer timer, activar B sin ningún disco.
4. Mientras B suena, cargar C al slot reutilizado; repetir.
5. Si B todavía NO está READY, no forzar salto de ROM que cuelgue:
   política explícita (continuar A y reintentar hasta READY, o error).
6. No confundir búsqueda/posición del cursor con canción efectivamente
   tocando ni precargar un candidato Random diferente del elegido.
7. El loader debe ser compatible con el IRQ de PLAY (Krill con
   contexto de ZP y memoria separado, o loader IRQ alternativo).
8. Mantener una ABI: directorio/glenn UI en una capa; subsistema
   de reproducción/IRQ en otra; driver/loader en una tercera.
   Instalar el drive-code al comienzo solo cuando el disco ya
   esté en un estado preparado, y no usar ROM OPEN/LOAD sobre
   el mismo drive sin un protocolo de uninstall/reinstall.
9. Evaluar REU opcionalmente para biblioteca mayor, NO exigir REU
   para lograr primera prueba de 3 temas sin espera.

**No integrar Krill aún:** su demostración en TEST02 fue correcta
de forma aislada; primero hay que conseguir el switch RAM desde
el reproductor sin carga, después la precarga concurrente.

## Prueba auditiva + instrumentación requeridas

- VICE C64 PAL, True Drive Emulation ON, reiniciar C64 y 1541.
- Tres pistas exportadas/reubicadas con dirección confirmada.
- Comprobar en el monitor / debugger:
  a) rangos sin solapamiento; b) INIT/PLAY por canción;
  c) precisión y cadencia del IRQ; d) número de accesos al drive
  *entre* las transiciones (debe ser cero en experimento A);
  e) duración en ciclos de cada cambio; f) actividad de IRQ
  y SID $D400-$D418; g) M/N/R y estado PLAYLIST_READY.
- Variación de velocidades exportadas desde SidTracker64:
  soporta 25-240 Hz y valor estándar 50 Hz; no forzar divisor
  de llamadas PLAY global. La etiqueta PSID VBI/CIA no expresa
  todas las velocidades arbitrarias.
- Protocolo PASS: A→B→C→A desde RAM a su velocidad musical
  correcta, sin destellos/errores ni luz de la unidad durante
  transiciones. El GUI no debe entrar en lectura de directorio
  por arrancar en N.

## Bibliografía primaria

- Glenn: `sidplay64.tas`, `src/init.tas`,
  `src/dir-iec.tas`, `src/load-iec-serial.tas`,
  `src/plt_function.tas`, `src/doheaderstuff.tas`,
  `src/irq.tas`, `sidplay64-readme.txt` (este repositorio).
- SidTracker64, historial oficial y frecuencia 25-240 Hz:
  https://apps.apple.com/us/app/sidtracker64/id955421205
- Linus Åkesson, SIDReloc (relocación de código y ZP):
  https://www.linusakesson.net/software/sidreloc/
- Krill Loader v184, instalación/compatibilidad, contexto IRQ:
  https://csdb.dk/release/?id=189130&show=notes
- HVSC, especificación SID/PSID, campos de velocidad y reubicación:
  https://hvsc.c64.org/faq
- C64 OS, manejo de SID/colisiones RAM/ZP en un sistema real:
  https://www.c64os.com/c64os/programmersguide/?s=usinglibraries_sidplay

**Criterio de decisión:** primero implementar y comprobar con GUI
original que tres SID preexistentes con direcciones independientes
se disparan A→B→C desde RAM; solo después retomar fastloader.
