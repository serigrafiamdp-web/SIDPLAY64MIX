# TEST50 — Caso difícil: Monty on the Run y colisión de Krill en $9000

**Estado: COMPILACIÓN PASS; reproducción, portada y precarga en VICE SIN CONFIRMAR.**

MASTER congelado: `MASTER-TEST49-183SID-8000-KRILL-PASS`.

## Diagnóstico real del conflicto
El Krill v184 que usamos en TEST49 ejecuta código residente en $9000–$91EE. Cuatro archivos PSID originales de esta prueba tienen código musical en esa misma región:

| Archivo en D81 | Fuente original de la galería | LOAD | INIT | PLAY | último byte |
|---|---|---|---|---|---|
| montyrun.sid | ALTA/monty_on_the_run.sid | $8000 | $8000 | $8012 | $95BF |
| montyrun2.sid | ALTA/monty_on_the_run__88764e25.sid | $8000 | $8000 | $8003 | $9453 |
| squamp.sid | ALTA/squamp.sid | $9000 | $9000 | $9006 | $9D4A |
| galencia.sid | ALTA/galencia.sid | $8000 | $8000 | $8003 | $996F |

## Solución experimental genérica
- El binario Krill v184 original de 495 bytes se obtiene **sin alterar el MASTER TEST19**. La nueva herramienta `tools/test50_relocate_krill.py` exige SHA256 original exacto y realiza **26 sustituciones verificadas de operandos absolutos**: $90xx->$3Cxx y $91xx->$3Dxx; los opcodes, direcciones ZP y saltos relativos permanecen idénticos.
- La copia original que aparece en $8800 al descomprimir el ONEFILE ahora contiene el Krill relocalizado. `mix10_prepare` la transfiere en $3C00–$3DFF **antes del primer SID de disco**, por lo que el primer SID puede pisar $8800–$89FF y $9000.
- El Krill reside en $3C00–$3DEE, bajo el límite del simbionte (<$3C00) y antes del caché de cabeceras $3E00–$3E7B.
- Toda llamada a carga en segundo plano pasa por `JSR $3C00` en vez de $9000; el instalador original en $6000 y el protocolo de disco conservan sus bytes.
- Clase de LOAD admitida: $8000–$9FFF, con INIT/PLAY reales dentro de música y destino <$A000. Se reutiliza la lógica virtual $1000–$2FFF y los desplazamientos por byte/página de TEST44/45; el handoff copia 8192 bytes a $8000–$9FFF, sin modificar SID.
- Los caminos TEST43–49 permanecen presentes. ESTE TEST puede causar regresiones que deberán verificarse en VICE por la relocalización del Krill global.

## Verificaciones estáticas
- GitHub Actions run 40765927429: **SUCCESS** 64tass+PuCrunch, regresiones de código.
- SHA256 del original Krill residente (495 bytes): `79de0781d2c846ed42bea02b6611dafad97ed9c4494baaca7765bae4a1cafb6c`
- SHA256 del Krill rebajado a $3C00: `01bd090b47dd72a721ab0d5f6e8b001af0f7cbea1e8ab69d04c376eee16ca493`
- SHA256 ONEFILE: `34ee9eb8c4bdef43ae99a83a071eb86a29da1404351cc07bae78c5a1e3814ec9`
- `test50_monty_4_nuevos.d81` contiene `00player.prg` + `capriphol.sid` PASS de referencia + cuatro SID originales. Se verificó directorio, contenido binario, cadenas de sectores y BAM. SHA256 `b8f4e8c907226a28252ee154d2c1e574851b9212c565ef6e3e989dcd34901163`

## Prueba solicitada en VICE
1. Probar `capriphol.sid` al arrancar (regresión del Krill trasladado).
2. Pasar a `montyrun.sid`, luego `montyrun2.sid`; escuchar la precarga de cinco segundos y transición continua.
3. Probar `squamp.sid` (LOAD/INIT exactos $9000) y `galencia.sid`.
4. Si se cuelga: registrar qué pista y si falla al iniciar, a los cinco segundos, o al pasar a siguiente.

Hay **16 candidatos identificados en ALTA** que cumplen la clase LOAD $8000–$9FFF con final <$A000: cuatro integrados en este D81 y **12 pendientes** para una segunda tanda. No se integran los doce hasta comprobar el núcleo.

**NO declarar TEST50 PASS ni modificar MASTER49** sin el resultado del usuario.
