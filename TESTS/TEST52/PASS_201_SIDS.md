# MASTER TEST52 — 201 SID compatibles acumulados — PASS en VICE

**Fecha:** 2026-10-28. **Estado:** MASTER congelado después de prueba del usuario.

## Rama exacta y evidencia

Este MASTER deriva **exclusivamente de** `test/test52-9kb-7000-bank`, la versión original de TEST52. NO deriva de `test/test52v2-preserve-installer-tail` y NO incorpora el intercambio temporal de los seis bytes del instalador Krill implementado solo en V2.

El usuario volvió a cargar la imagen **`TEST52_9KB_2_SIDS_NUEVOS_VICE(1).d81`**, comprobó que funcionaban las canciones y respondió expresamente: «correcto estos funcionan». La imagen vuelta a subir fue cotejada byte a byte mediante SHA256 con la imagen original del TEST52: ambas son idénticas.

- SHA256 D81 comprobado: `df57fbf9c6088b9e7cb034295ad3d12b0b885e1b49b8be552a1723a8f48bf3ae`
- Tamaño imagen D81: 819200 bytes.
- Canciones nuevas **originales, sin modificar**: `hawkeye.sid`, `comicbakery.sid`.
- Referencia anterior en imagen: `capriphol.sid`.
- `hawkeye.sid`: LOAD=$7AE0, INIT=$7AE0, PLAY=$7AE3, cuerpo de 8768 bytes; fin exclusivo=$9D20.
- `comicbakery.sid`: LOAD=$7F00, INIT=$7F00, PLAY=$7F03, cuerpo de 8448 bytes; fin exclusivo=$A000.

## Funcionalidad y acumulado

- MASTER TEST51: 199 SID compatibles acumulados (en varios D81).
- TEST52 original: +2 SID con cuerpo de más de 8192 bytes.
- **Total acumulado: 201 SID compatibles**, NO implica 201 simultáneos en un solo D81; selector todavía no ampliado y bibliotecas largas verificadas previamente hasta 162 SID.
- Nueva ruta de 9216 bytes (36 páginas) para LOAD $7A00–$7FFF, staging $4000–$63FF, handoff a LOAD original y Krill residente $3C00. Las rutas de 8KB anteriores siguen presentes.
- Sin recodificar SID original; todas las canciones siguen con nombres minúsculos sin prefijos numéricos, `00player.prg` primero. Exclusiones `cool tune`, `and again` intactas.
- CI de la rama original TEST52: GitHub Actions run `40776312441` **SUCCESS** de compilación y regresiones estáticas. El **PASS funcional** proviene exclusivamente de la prueba del usuario en VICE.

## Lección de las pruebas

Hubo una primera ejecución fallida con pantalla negra y monitor mostrando el instalador Krill en $7753/$7750 con $3FF1=$11. Se investigó y se produjo una **V2 experimental** que protegía $7AE0–$7AE5, pero también se bloqueó en VICE. A continuación, el usuario volvió a probar **la primera imagen original**, cotejada con SHA256, y **confirmó que ambas canciones funcionan**. Por ello, V2 **NO se incorpora a MASTER**. No atribuir la causa de la primera pantalla negra a un bug corregido: su explicación no quedó demostrada. No afirmar que toda la biblioteca anterior se reprodujo en este TEST de 3 SID; las 199 compatibilidades anteriores provienen de sus PASS en las ramas anteriores.

## Trabajo siguiente

Continuar buscando familias de SIDs difíciles, especialmente las de carga mayor de 8KB o ubicaciones que permitan nuevas rutas de precarga sin pisar el player/IRQ. Hacer nuevas pruebas en ramas independientes y no alterar este MASTER. Ampliar el selector **al final** según la instrucción expresa del usuario.