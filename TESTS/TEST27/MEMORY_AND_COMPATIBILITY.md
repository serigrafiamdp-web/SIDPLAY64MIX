# TEST27 — Mapa de memoria y compatibilidad

ESTADO: 1 PRG autentic Glenn+Krill compilado; prueba de VICE PENDIENTE. No es PASS.
TEST19 y TEST25 permanecen como referencias congeladas.

## RAM por fases
- Música de los 19 SID conocidos: $1000–$2922, LOAD/INIT=$1000, PLAY=$1003.
- Hooks del symbiont: $3000–$35FF, residentes. Riesgo si un SID ocupa estas páginas.
- Buffer de precarga: $5000–$69FF y lectura temporal aproximadamente hasta $6DFF.
- Instalador Krill: $6000–$7AE5, utilizado SOLO durante la instalación. Comparte temporalmente área con futuro buffer; esto es válido si las fases no coinciden.
- Backup residente Krill: $8800–$89EE hasta copiarlo a $9000.
- Residente Krill activo: $9000–$91FF cuando se utiliza el lector de disco.
- Pantalla y caracteres originales: $C400 y $E000, con código reubicado alto.
- ZP, pila, vectores ($0000–$03FF): preservar la propiedad de cada componente y los cambios de música.

## Compatibilidad incremental sin parches por SID
1. Analizar cabecera PSID v1-v4: dirección efectiva LOAD, INIT, PLAY, offset real, subtunes y speed flags. No asumir $1000/$1003.
2. Calcular rango de ejecución efectivo; detectar cruces con todas las regiones residentes. Detener seguro cuando no haya memoria en lugar de bloquear la C64.
3. Ruta rápida: usar Krill con precarga a los cinco segundos SOLO si música actual y próxima no se pisan con el buffer ni el motor.
4. Ruta de compatibilidad: si el SID no admite doble buffer, desactivar solo la precarga y cargar tras detener la música previa.
5. Ruta avanzada para RSID, BASIC, IRQ propietario, o 2-3 chips SID: requiere manejo específico o hardware. Mostrar no soportado antes que ejecutar a ciegas.
6. Probar diferentes cargas, distintos INIT/PLAY, múltiples subsongs, PAL/NTSC y SID físicos.

No se puede garantizar todos los SID con una sola configuración fija de 64 KB: los SID son código de máquina que puede sobrescribir vectores, zero page, rutina residente e I/O.

## VICE TEST27 aceptación
Arranque frío; preguntas y scroller del Glenn real; SID inicial; precarga a 00:05 en Manual y Next; cambios por RETURN; IRQ/tempo; ningún borde rojo inesperado ni BASIC/JAM.
TEST27 es prueba experimental hasta confirmación funcional del usuario.

El ZIP de TEST27 NO incorpora EXE Windows; solo fuentes y ejecutables Commodore 64. Si Windows detecta amenaza, no desactivar antivirus: investigar nombre de detección.