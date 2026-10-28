# ANALISIS POST-PASS — TEST35 (27/10/2026)

## Funcionalidades observadas / confirmadas

1. Krill se activa: en TEST34 el monitor mostraba `$3FF1=12`.
2. Temporizador inicia precarga a los cinco segundos: `$3FF2=03` cuando esta en curso.
3. El siguiente SID se elige por indice y nombre real, no por nombres `MIX_*`.
4. El flujo hace precarga y cambio de SID en la prueba VICE informada por el usuario.
5. TEST35 mantiene las IRQ de musica durante borrado de 27 paginas y copiado de 26 paginas de la memoria de precarga.
6. El usuario reporto que el microcorte desaparecio y marco PASS.

## Riesgos tecnicos — no son fallas confirmadas

- **Transiciones en modo Next:** `mix10_fast_next` aun utiliza `SEI` durante el copiado del banco de 26 paginas `$5000->$1000`. Si apareciera un corte perceptible en alguna transicion, medir esa seccion antes de cambiarla; hacer IRQ en el momento de escribir el propio codigo SID puede ser inseguro.
- **Indices y retornos:** validar seleccion manual de SID intermedio, ultimo (19) y retorno al primero, especialmente cuando ya existe una precarga.
- **Reintentos y errores de unidad:** comprobar manejo si falta disco, no encuentra un SID o falla el protocolo Krill, sin colgar la UI.
- **Proteccion de memoria:** el conjunto actual esta curado para PSID v2 con carga y llamadas compatibles; una coleccion general exige validar carga/init/play, tamanio, IRQ, buffers `$5000-$6DFF`, RAM de programa `$3000` y proteccion de pagina cero `$C0-$D5`.
- **Borde como diagnostico:** los colores amarillo/verde actualmente vienen del codigo de prueba. Decidir luego si deben ocultarse en una version de presentacion.
- **Temporizador de cinco segundos:** confirmar comportamiento si el usuario cambia varias veces rapidamente de SID y si la cancion termina antes de completar precarga.
- **Compatibilidad VICE/1541 real:** validar distintos modos de emulacion de unidad 8 y hardware real solo cuando haya recursos de prueba.

## Orden recomendado para proseguir

1. Conservar este MASTER.
2. TEST36 en rama aislada: matriz de pruebas M/N y repeticion de 19->1, cambios manuales durante precarga.
3. TEST37 solo si aparecen problemas: diagnosticos de ausencia de archivo/unidad desconectada y recuperacion.
4. Compatibilidad PSID mas generica por etapas, con corpus de pruebas real y sin romper 19 SIDs de referencia.

No se aplicaron cambios funcionales a la version PASS.
