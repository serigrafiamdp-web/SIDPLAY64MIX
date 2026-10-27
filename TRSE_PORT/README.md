# SIDPLAY64MIX — port limpio TRSE/OrgAsm

Estado: PORT01 — proyecto modelo, todavía sin reproductor portado.

## Fuente original y política

Conservamos en la rama master los fuentes originales de SIDPLAY64 v1.21 (sidplay64.tas, sidplay64.cfg, src/*.tas), escritos en 64tass. No editarlos en origen: adaptar los módulos al ensamblador OrgAsm de manera incremental.

El desarrollo nuevo vive en development/trse-port. Los anteriores TEST25 PASS y sus D64 son referencias funcionales, no la base de los parches nuevos.

## TRSE base

El paquete inicial PORT01 lleva exactamente los cinco archivos facilitados por el usuario: SIDMPLAY64.trse, main.ras, d64.paw, images/octopus.flf, images/neo_rider_by_the_diad.flf. Compila en el entorno del usuario para probar carga de Krill y alternancia de imagenes; todavía no es el reproductor SIDPLAY64.

El ZIP completo de cada PORT se entrega por la conversación, y puede reemplazar por completo los contenidos de la carpeta TRSE. No se guardan aquí todavía los binarios .flf del modelo.

## Reglas

- Portear ASM original por módulos; nunca realizar sustitución masiva de sintaxis 64tass/OrgAsm.
- Conservar créditos, scroller y comportamiento visual del original.
- Mapear direcciones de RAM, IRQ, bancos y áreas de música ANTES de integrar rutinas.
- Cargar SID originales con un lector genérico, sin duplicados MIX ni parches por canción.
- Objetivos de regresión: 5 segundos precarga, Manual y Next.
- No declarar PASS ni editar MASTER hasta confirmar el resultado en VICE.

## Hitos

PORT01: validar base TRSE/Krill del usuario.
PORT02: portar inicialización + interfaz/scroller original, sin música.
PORT03: directorio, cabecera PSID y selección.
PORT04+: init/play, precarga genérica y optimización.
