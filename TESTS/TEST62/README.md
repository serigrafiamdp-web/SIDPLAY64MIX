# TEST62 — 167 SIDs aleatorios SOLO de familias con soporte existente

**Estado:** D81 generado y verificado estructuralmente; **pendiente de prueba real en VICE**. No aumentar automáticamente el número de SIDs PASS. Fecha 2026-10-29.

## Entrada y reproductor

- Entrada: la colección persistente **MUSICIANS.zip depurada**, con **56.518 SIDs** (quitados 49 de la firma motor Pitfall/Mr Monster y Buggy separado por JAM). No usar la versión anterior de 56.568 para este experimento.
- ONEFILE: exactamente **el de TEST60 B** (derivado de TEST59 experimental), SHA256 `bfaac11797663c3bc98ed84da99c0b17b81530b1228c7b974d739e5deab52bc1`. No se modificó código ni se aumentó soporte.
- Selección reproducible con `random.Random(202610291347)`. 1 SID anterior PASS **capriphol.sid** como primer archivo y 166 candidatas aleatorias de la colección filtrada. Nombres de archivos originales basenames en minúsculas, ASCII <=16 bytes, únicos en directorio.
- Familia TEST55 original $3000–$3BFF excluida: no convive en este ONEFILE. Tampoco RSID, versiones/cabeceras inesperadas, múltiples SID chips, carga original fuera de rutas implementadas, INIT/PLAY fuera del cuerpo o referencias JSR/JMP directas a $5000-$73FF (filtro preventivo conservador).

## Disco

- `TEST62_ALEATORIOS_SOLO_FAMILIAS_SOPORTADAS_167SID.d81`
- Tamaño D81 **819.200 bytes**
- SHA256 `9715704f621f9c848a0f1b3ed2f22f8c866c21dede4c32f5e74b4d96aec8c81a`
- 168 archivos totales = **00player.prg + 167 SID**. Límite del selector del reproductor: `maxentries=168` (incluido PRG).
- 21 sectores de directorio (40/3 .. 40/23), 3 sectores 1581 BAM/header, **2.338 sectores de datos** en pistas 1–39 y 41–80. Espacio libre en D81 aunque límite lógico de cantidad de archivos completo.
- Validadas todas las cadenas de bloques (254 bytes/sector), todos los nombres, el orden, cada byte reextraído del D81 contra el original y el conteo de sectores libres reconstruido en BAM. No es confirmación de compatibilidad musical.

## Familias incluidas

| Familia LOAD | Nº SID |
|---|---:|
| $1000–$1FFF | 60, incluido `capriphol.sid` PASS |
| $2000–$2FFF | 18 |
| $4000–$4FFF | 16 |
| $7A00–$7FFF, ruta 9KB | 7 |
| $8000–$9FFF | 14 |
| $A000–$BFFF | 12 |
| $E000–$F7FF | 12 |
| $0FFF | 5 |
| $0F80–$0FFE | 23 |
| **TOTAL** | **167** |

Los originales provienen de un grupo de 4.693 candidatos conservadores encontrados dentro de los 56.518 SIDs depurados. Ningún candidato elegido de una familia sin soporte. No confundir selección estructural con PASS individual.

## Archivos adicionales

- `TEST62_ALEATORIOS_LISTADO_167_SIDS.csv`: incluye orden, nombre en el D81, ruta original en MUSICIANS, familia y LOAD/INIT/PLAY y tamaño, y si se había confirmado previamente.
- `TEST62_ALEATORIOS_LEEME.txt`: instrucciones.
- `TEST62_ALEATORIOS_D81_Y_LISTADO.zip`: D81 + CSV + instrucciones.

## Prueba en VICE

1. Montar D81 en dispositivo 8 y arrancar `00player.prg`.
2. Iniciar con `capriphol.sid` (primer SID del selector, ruta original PASS) para activar Krill.
3. Recorrer canciones con NEXT/preload de 5 segundos; probar Enter a mitad de lista y al final, especialmente índices >60 y >130.
4. En caso de fallo, indicar la posición exacta del CSV, SID que sonaba, seleccionado, si fue Enter o NEXT, JAM o retorno sin carga; monitor `m $3ff0 $3fff`.

**No promover TEST62 ni cambiar MASTER58** antes de resultados de usuario. Los 167 son candidatas, NO 167 nuevas confirmadas.
