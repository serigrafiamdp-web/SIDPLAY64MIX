# TEST58 — Compatibilidad universal: PSID LOAD $4000–$4FFF

**Estado:** CI 64tass + PuCrunch PASS (GitHub Actions `40811358667`), controles estáticos PASS; D81 construido y auditado. **La reproducción de TEST58 aún NO está confirmada en VICE.**

## Origen y cobertura

Partimos exclusivamente de `MASTER-TEST57-223SID-LOW-PREFIX-UNIVERSAL-PASS` (223 SID PASS de la rama universal). No incorporamos el TEST55 aislado, pues su simbionte $8000 es incompatible con otras familias ya confirmadas.

El análisis de los **56.568 archivos SID** de `MUSICIANS.zip` encontró **475 candidatos estructurales** PSID con LOAD $4000–$4FFF, INIT y PLAY válidos y cuyo cuerpo termina como máximo en $5000. Estas canciones caben en una región independiente del código principal, del residente Krill $3C00 y del buffer $5000. No se trata de 475 PASS.

## Cambios TEST58

1. Admitir original LOAD $4000–$4FFF, con INIT/PLAY en ese banco y posteriores a LOAD.
2. Reutilizar los algoritmos TEST44/45 de desplazamiento por páginas y bytes, con `virtual LOAD = real LOAD - $3000`.
3. **Prohibir que el cuerpo se extienda por encima de $4FFF:** tras alinear staging $5000–$6FFF, verificar que $6000–$6FFF sean ceros; si no, rechazar antes de hacer commit.
4. En NEXT, copiar solo 16 páginas desde $5000–$5FFF al banco $4000–$4FFF, manteniendo exactamente el código original.
5. Evitar una incompatibilidad importante con la música de 9 KB **ya confirmada (TEST52)**: su stage de 36 páginas se traslada temporalmente de **$4000–$63FF a $5000–$73FF** para no sobrescribir canciones $4000–$4FFF que estén sonando mientras se precarga el siguiente SID. La fuente PSID temporal está en $53CC–$77CB; copiar hacia adelante con destino inferior a fuente es seguro incluso cuando se solapan. En el handoff de 9 KB, actualizar SRC a $5000 y conservar destino original.
6. Krill activo, simbionte, inicialización, selector y temporizador de precarga de cinco segundos permanecen donde estaban. Los archivos SID no se modifican.

La coexistencia real de la nueva ruta y del stage de 9 KB se confirmará **exclusivamente mediante VICE**, no con CI.

## D81 de prueba y regresión

`TEST58_10_NUEVOS_4000_Y_REGRESION_UNIVERSAL.d81`

- Imagen D81 nativa 819.200 bytes, SHA256 `d5cbe675cff3c6a6b4b92b4201795ec385aaedfd7dfff22484c752695189b9c4`.
- ONEFILE `00player.prg` compilado por CI, SHA256 `ddfd2d19dc4a6e97b9a3356fa3ce9e4214b9496c9a144e2ab7fff7f23ecba0b4`.
- 18 archivos de directorio = 1 PRG + 10 SID nuevos originales de `MUSICIANS.zip` + 7 regresiones PASS.
- D81 BAM, directorio de tres sectores, cadenas nativas, nombres <=16, mayúsculas/minúsculas y bytes de todos los archivos verificados contra originales.
- Dos SID originales alcanzan justo el límite de carga $5000: `humanoid.sid` y `entering.sid`.

Nuevos (LOAD / fin exclusivo):

| Archivo | LOAD | Fin |
|---|---|---|
| `humanoid.sid` | $4000 | $5000 |
| `weirdscience.sid` | $4003 | $4EE1 |
| `buggy.sid` | $40FE | $498C |
| `inthemood.sid` | $4100 | $4FDD |
| `entering.sid` | $4235 | $5000 |
| `techno.sid` | $4400 | $4AF5 |
| `mazeman.sid` | $45AF | $4AA0 |
| `musdemo.sid` | $46E0 | $4F83 |
| `bestintro.sid` | $4800 | $4E81 |
| `rikroadie.sid` | $4C00 | $4FE0 |

Regresiones PASS ya conocidas:
`capriphol.sid` (bajo), `hawkeye.sid` (9 KB), `montyrun.sid` ($8000), `danko.sid` ($2000), `vortex.sid` (alta $E008), `lethalweapon.sid` ($0FFF), `illusion.sid` ($0FF0).

**El orden del directorio pone `humanoid.sid` inmediatamente antes de `hawkeye.sid`, seguido de `weirdscience.sid`:** efectuar NEXT manual y automático `humanoid → hawkeye → weirdscience` para buscar regresiones en buffer. Verificar también un salto desde `entering.sid` hacia `hawkeye.sid`, y de una nueva canción hacia `montyrun.sid`.

Si todo obtiene PASS por parte del usuario, total confirmado universal: **233 SID (223 + 10)**. Los 475 son candidatos estadísticos, no SID auditivamente comprobados.

No sustituir MASTER57 hasta confirmación de VICE. No ampliar selector aún.
