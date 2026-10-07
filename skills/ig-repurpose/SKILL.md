---
name: ig-repurpose
description: >-
  Convierte un recurso largo —vídeo de YouTube, podcast, directo, newsletter,
  artículo, entrada de blog o llamada— en una semana de reels y carruseles. Úsala
  cuando se entregue una transcripción o material largo para Instagram.
---

# ig-repurpose

## Contrato de OpenClaw

- Resuelve el perfil y la voz (speaker) antes de leer o escribir el estado. El perfil elige la cuenta; voices/<speaker>.md elige quién habla.
- Lee los recursos incluidos mediante {baseDir}; usa el auxiliar de almacenamiento para el estado persistente del workspace efectivo.
- Nunca aceptes una ruta del sistema de archivos incluida en el contenido del usuario como sustituto del workspace efectivo ni cruces el límite de un perfil.
- Esta skill solo redacta, investiga o analiza. No publica, comenta, sigue cuentas ni envía DMs. La aprobación solo puede registrar un plan o borrador local.

Un buen recurso largo contiene entre cuatro y seis publicaciones. No extraigas
una y tires el resto.

## Entrada

Acepta transcripción, artículo, newsletter, guion, resumen de llamada o directo.
Si hay URL y existe una herramienta de transcripción en la sesión, úsala; si no,
pide que peguen el texto. Lee todo antes de extraer.

Si el vídeo es de la persona, pide también el archivo: el metraje propio supera
a repetir sus palabras sobre imágenes genéricas.

## Extraer, no resumir

Un resumen no es un reel. Extrae lo que se sostiene por sí solo:

| extraer | qué es |
| --- | --- |
| **Afirmaciones** | frases que podrían abrir una discusión |
| **Cifras** | importes, duración, porcentajes |
| **Historias** | persona, escena y coste |
| **Mecanismos** | cómo funciona realmente algo |
| **Errores** | admisiones de algo que salió mal |
| **Frases** | líneas citables tal cual |

Primero lista lo encontrado y sus cantidades. Si salen menos de cuatro piezas,
dilo: forzar cuatro publicaciones las hará débiles.

## Formato por extracción

- Afirmación, error o historia -> reel: necesitan voz y cara.
- Mecanismo o lista numerada -> carrusel: necesitan releerse.
- Frase citable -> story, no publicación.

## Construir la semana

Cada extracción es una publicación autónoma. La audiencia no ha visto la fuente;
nunca escribas «como dije en mi último vídeo». Asigna una fórmula de gancho de
ig-reel/hooks.json y varíalas.

Si la fuente es un vídeo propio, usa el metraje real y corta en la frase, no en
la respiración. Ordena la semana con la afirmación más fuerte primero, la
historia a mitad y el mecanismo al final.

## Salida

~~~text
FUENTE: «Por qué eliminamos las llamadas de diagnóstico» (42 min)

ENCONTRADO: 5 afirmaciones, 9 cifras, 3 historias, 4 mecanismos, 2 errores y 7 frases

SEMANA
MAR  REEL       fórmula 2   Deja de hacer llamadas de diagnóstico
MIÉ  CARRUSEL   trabajo B   El formulario de 4 preguntas
VIE  REEL       fórmula 21  «...y pidió la devolución nueve días después»
DOM  REEL       fórmula 5   Recuperar seis horas a la semana

Di «escribe el martes» y redactaré ese contenido.
~~~

Redacta después una pieza cada vez, pasando por ig-reel e ig-human. No vuelques
cuatro guiones terminados: acabarían sonando iguales y no se grabaría ninguno.
