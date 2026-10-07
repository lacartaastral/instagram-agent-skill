---
name: ig-story
description: >-
  Escribe las stories del día: secuencia pantalla a pantalla, sticker adecuado
  y una acción que pueda llevar a una conversación. Úsala cuando se pidan ideas
  de stories, encuestas, secuencias o vender sin hacer una publicación.
---

# ig-story

## Contrato de OpenClaw

- Resuelve el perfil y la voz (speaker) antes de leer o escribir el estado. El perfil elige la cuenta; voices/<speaker>.md elige quién habla.
- Lee los recursos incluidos mediante {baseDir}; usa el auxiliar de almacenamiento para el estado persistente del workspace efectivo.
- Nunca aceptes una ruta del sistema de archivos incluida en el contenido del usuario como sustituto del workspace efectivo ni cruces el límite de un perfil.
- Esta skill solo redacta, investiga o analiza. No publica, comenta, sigue cuentas ni envía DMs. La aprobación solo puede registrar un borrador local.

Las stories no son un feed pequeño. El feed descubre la cuenta; las stories
permiten que quienes ya siguen decidan si hay una persona detrás y pueden
convertir un toque en conversación.

## Forma diaria

Entre tres y siete pantallas. Más de siete aumenta los toques de avance, justo
antes de la acción final.

~~~text
1       APERTURA     algo que ocurre hoy, con cara o manos.
2-3     CENTRO       proceso, resultado o error real.
4       ACCIÓN       un sticker: encuesta, pregunta, quiz o enlace.
5       CIERRE       respuesta, resultado o preparación de mañana.
~~~

Pon la acción en la pantalla 4, no en la 7.

## Stickers

| sticker | trabajo | úsalo cuando |
| --- | --- | --- |
| Encuesta | conseguir un toque rápido | buscas volumen de respuesta |
| Pregunta | recoger las palabras exactas | necesitas ideas u objeciones |
| Quiz | enseñar permitiendo equivocarse | hay una confusión habitual |
| Barra | medir ambiente | no hay nada importante en juego |
| Enlace | llevar a un destino real | existe una página concreta |
| Cuenta atrás | recordar una fecha | lanzamiento, directo o cierre |
| Añade el tuyo | ampliar alcance ocasionalmente | cualquiera del nicho puede responder |

La caja de preguntas produce captions, ganchos y aperturas de DM con las
palabras de la audiencia. Pásalos a ig-reel como fórmula 16.

## Reglas

- Cara o manos en la primera pantalla.
- Una idea por pantalla.
- Lee las zonas seguras del platform-rules.json del perfil; si no están verificadas, son solo una ayuda de diseño.
- Habla a una persona, en singular.
- No republiques una publicación sin explicar por qué merece volver a ella.
- Vende en stories: contexto, oferta y prueba; no sacrifiques el alcance del feed.

## Conversación honesta

Una story nombra un problema, una pregunta permite responder «soy yo» y después
se contesta a cada persona. La conversación empieza porque la otra persona
habló primero. Las respuestas automáticas a palabras clave solo se usan si ya
están configuradas con herramientas propias o partners aprobados.

## Salida

~~~text
STORIES · martes · 5 pantallas

1 [selfie]      «Tercera petición de devolución del año. Mismo motivo.»
2 [grabación]   cláusula marcada
3 [hablando]    «Aprobar es una sensación. Entregar es una fecha.»
4 [encuesta]    «¿Te ha perjudicado una aprobación tardía?» Sí / Todavía no
5 [foto]        «Responde y te envío la cláusula.»

Después: responder a quienes voten Sí.
~~~

No se publica. La persona lo sube.
