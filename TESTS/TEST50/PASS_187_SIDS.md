# MASTER TEST50 — 187 SID compatibles acumulados — PASS de usuario

Fecha: 2026-10-28.

Rama congelada a partir de `test/test50-krill-resident-3c00`. El usuario probó el D81 corto `test50_monty_4_nuevos.d81` y confirmó expresamente **"pass"**.

## Compatibilidad acumulada

- MASTER TEST49: 183 SID confirmados en varios discos.
- TEST50: 4 nuevos candidatos difíciles que cargan música en RAM ocupada anteriormente por Krill residente:
  - `montyrun.sid` — original LOAD=$8000, final $95BF.
  - `montyrun2.sid` — original LOAD=$8000, final $9453.
  - `squamp.sid` — original LOAD=$9000, final $9D4A.
  - `galencia.sid` — original LOAD=$8000, final $996F.
- Total acumulado compatible: **187 SID**, repartidos entre discos de prueba. **NO** significa 187 SID simultáneos en un D81. El selector sigue sin ampliarse; hasta 162 SID por biblioteca validada.

## Mejora estructural

- El Krill v184 residente pasa del rango $9000-$91EE a $3C00-$3DEE mediante el script verificable `tools/test50_relocate_krill.py`. La transformación reemplaza 26 operandos absolutos tras verificar SHA256 del binario base.
- Antes del primer SID, el código copia el residente reubicado desde su respaldo original $8800–$89FF hacia $3C00–$3DFF.
- La precarga y el handoff se mantienen, y la música original puede ocupar $8000–$9FFF. Clase nueva válida sin parchear SID originales.
- `cool tune` y `and again` continúan excluidos. Nombres de SID en minúsculas, sin numeración; ejecutable `00player.prg`.
- Los restantes SIDs de la familia quedan pendientes de pruebas separadas.

## Validación y límites

- GitHub Actions run `40765927429`: compila programa ONEFILE y pasa comprobaciones estáticas.
- El usuario confirmó PASS en VICE para el disco de cuatro temas nuevos más referencia. Incluye prueba solicitada de reproducción y precarga; no afirmar verificación de hardware físico si no fue indicada.
- MASTER TEST49 y demás ramas anteriores permanecen congeladas.
- Próximo trabajo: probar otros candidatos originales del grupo LOAD=$8000-$9FFF contra este motor en un TEST51 independiente. **No ampliar selector todavía**, por indicación del usuario: primero recuperar familias de incompatibilidades.

Estado: MASTER de referencia, no modificar para experimentar.
