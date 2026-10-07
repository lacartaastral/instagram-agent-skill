---
name: ig-reel
description: >-
  Convierte una idea en bruto en un reel de Instagram: opciones de gancho con
  26 fórmulas, guion hablado, texto en pantalla y escaleta temporal, usando la
  voz de la persona y puntuándolo antes de grabar. Úsala al pedir un reel,
  guion, gancho o voz en off.
---

# ig-reel

## Contrato de OpenClaw

- Resuelve el perfil y la voz (speaker) antes de leer o escribir el estado. El perfil elige la cuenta; voices/<speaker>.md elige quién habla.
- Lee los recursos incluidos mediante {baseDir}; usa el auxiliar de almacenamiento para el estado persistente del workspace efectivo.
- Nunca aceptes una ruta del sistema de archivos incluida en el contenido del usuario como sustituto del workspace efectivo ni cruces el límite de un perfil.
- Esta skill solo redacta, investiga o analiza. No publica, comenta, sigue cuentas ni envía DMs. La aprobación solo puede registrar fecha, fórmula y borrador en local.

Convierte una idea en bruto en un reel que alguien termina de ver.

Herramientas de esta carpeta:

~~~bash
python3 {baseDir}/hookscore.py hooks.txt              # ordena opciones de gancho
python3 {baseDir}/hookscore.py --hook "una línea"      # puntúa uno
python3 {baseDir}/beats.py guion.txt --target 30       # escaleta temporal
~~~

## Antes de escribir

1. Lee voices/<speaker>.md del perfil si existe: cómo habla la persona, qué nunca
   dice y a quién se dirige. Si falta, pide tres reels propios, léelos o
   transcríbelos, infiere la voz y escribe el archivo solo con aprobación. Un
   guion en la voz equivocada no sirve.
2. Lee {baseDir}/hooks.json. Contiene 26 fórmulas con plantilla, ejemplo,
   versión en pantalla, uso y error habitual.
3. Si la idea es débil, no la rellenes. Haz una pregunta agrupada: qué ocurrió,
   a quién y qué costó o devolvió. Un reel necesita una verdad específica.
4. Lee swipe.md del perfil si existe. ig-viral lo escribe y contiene la evidencia
   propia de qué fórmulas funcionan en ese nicho.

## Estructura

~~~text
0:00-0:02   GANCHO       afirmación hablada y texto en pantalla por separado.
0:02-0:07   APUESTA      por qué importa para quien mira, una línea.
0:07-...    CUERPO       una idea por beat y cambio visual en cada beat.
ÚLTIMOS 3 s RESULTADO    cumple lo prometido y haz una sola petición.
ÚLTIMA LÍNEA BUCLE       repite una palabra del gancho para cerrar la repetición.
~~~

La duración es una decisión editorial. Lee la guía del platform-rules.json del
perfil y trata los valores no verificados como ayudas de revisión.

## Flujo

1. Elige tres ganchos distintos en hooks.json, no tres versiones del mismo.
2. Pon las tres líneas habladas en un archivo y ejecuta hookscore.py. Enseña la
   clasificación. Si la primera queda por debajo de 50, todavía no hay gancho.
3. Escribe el guion ganador con lenguaje hablado, contracciones y frases cortas.
4. Ejecuta beats.py con la duración. Corrige ganchos tardíos, beats de más de
   cuatro segundos, tramos sin nada concreto y ausencia de bucle.
5. Pasa el guion por ig-human antes de mostrarlo.
6. Devuelve guion, texto en pantalla con tiempos y recibo:

~~~text
REEL LISTO
gancho:      nº 3 «Nadie te cuenta esto», 86, FUERTE
duración:    28,4 s en 9 beats
pantalla:    6 tarjetas
humanizador: 4 artefactos eliminados, puntuación 81, LISTO
caption:     ejecutar ig-caption

Responde «sí» para registrarlo o dime qué cambiar.
~~~

7. **Nunca publiques.** La persona graba y publica. Con aprobación explícita,
   resuelve log.md y registra fecha, fórmula y primera línea. Es un registro
   local, no una publicación.

## Texto en pantalla

Es un guion independiente: se lee antes de oírse.

- Seis palabras o menos por tarjeta.
- La tarjeta del gancho aparece en el primer fotograma.
- En 1080x1920, mantén libre la zona superior aproximada de 230 px, la inferior desde 1440 px y los 230 px derechos; confirma siempre la interfaz actual.
- Nunca pongas el gancho donde queda tapado por el caption.
- Quema subtítulos para el cuerpo: mucha gente mira sin sonido.

## Reglas

- Una idea por reel. Si hay dos, son dos reels.
- Cifras antes que adjetivos. Si falta una cifra real, pregunta o deja {{tu cifra}} y marca el hueco.
- Corta saludo, introducción, nombre y logo.
- Cambia el plano en cada beat.
- Una acción al final: comentar, guardar o seguir.
- No inventes métricas, clientes, ingresos ni resultados.
- No escribas alrededor de un audio de moda que la persona no pueda usar.
