# TEST54 — Primera subfamilia del grupo más numeroso de MUSICIANS.zip

**Estado:** Compilación GitHub Actions PASS; D81 verificado; **pendiente de PASS en VICE del usuario**.
Base congelada: `MASTER-TEST52-201SID-9KB-PASS`. No modificar MASTER ni selector. La rama experimental `test/test53-high-e100-e8ff` es independiente; TEST54 se derivó directamente de MASTER52.

## Auditoría del ZIP grande

Archivo original del usuario: `MUSICIANS.zip`, 56.568 SID. El grupo de carga intermedia PSID LOAD $2000–$79FF es el mayor de los obstáculos de ubicación detectados en auditoría.

Primera subfamilia recuperable sin mover memoria residente:
- **278** SID PSID originales tienen LOAD $2000–$2FFF, INIT y PLAY dentro de su payload y cuerpo que termina antes o exactamente en $3000. Cabecera versión 2 con offset $007C, LOAD de cabecera $0000, cuerpo <=8192 bytes, un SID, vectores no cero.
- Esta métrica es **cobertura estructural potencial**, no 278 PASS.
- Los demás casos de RAM $2000–$79FF serán objeto de otras pruebas: no se desbloquean por este simple cambio, porque pueden invadir el simbionte $3000-$3BFF, Krill residente $3C00-$3DFF, buffers $4000-$77FF o el instalador $6000-$7AE5.

## Modificación TEST54

Se amplía exclusivamente el límite superior de LOAD en `mix46_regular_load`, de `$1FFF` a `$2FFF`:
`cmp #$20` -> `cmp #$30`.
La región real de destino y límite de INIT/PLAY sigue siendo $1000-$2FFF. Los algoritmos de TEST44/45 desplazan páginas y bytes en el banco de staging $5000–$6FFF, y rechazan cualquier byte de código que exceda $2FFF. No tocar Krill residente $3C00, buffer 9KB TEST52, PSID, directorio ni temporizador de cinco segundos.

## Primer D81

`TEST54_6_SIDS_MEMORIA_INTERMEDIA.d81`: 819200 bytes, SHA256 `6c219d0a371a65c818e71dbccfd4645d461474715c2fbe0cdbe12260542d9ec6`.

Incluye `00player.prg` del TEST54, `capriphol.sid` referencia anterior y seis SID originales sin modificaciones tomados directamente de MUSICIANS.zip:

| Archivo | LOAD | INIT | PLAY | Fin exclusivo |
|---|---:|---:|---:|---:|
| danko.sid | $2000 | $2029 | $2000 | $3000 |
| redsnow.sid | $2036 | $2036 | $203C | $2F03 |
| trapsv2.sid | $20F6 | $20F6 | $2103 | $2FEF |
| sf2ryu.sid | $2400 | $2400 | $2403 | $2D9F |
| flower6.sid | $28FA | $28FA | $2900 | $2FA2 |
| bmxracers.sid | $2E00 | $2F90 | $2E00 | $2F98 |

Todos los contenidos PSID originales fueron preservados byte a byte, y sus firmas musicales no estaban repetidas en imágenes D81 anteriores de pruebas. Nombres en minúsculas, <=16 chars. El disco se construyó con BAM nativa D81, pista 40 directorio, verificando cadena completa de sectores, nombre, contenido, bitmap y contador de free sectors por pista. El ONEFILE lo compiló CI con 64tass y PuCrunch.

CI run **40792860448**: PASS de compilación y regresiones estáticas, no acredita reproducción.

### Prueba inicial sugerida

Abrir en VICE, elegir `capriphol.sid` de referencia al inicio, pasar por las seis nuevas con selección manual y NEXT automático. Comprobar audio y la precarga después de 5 segundos, especialmente `danko.sid` que termina exactamente en $3000 y `redsnow.sid` / `trapsv2.sid` / `flower6.sid` con LOAD desalineado.

Si el usuario reporta PASS completo: acumulado **207 SIDs originales confirmados**, no 278. Solo entonces congelar nuevo MASTER.

No ampliar selector hasta agotar categorías rentables.
