---
name: ig-comment
description: >-
  Escribe comentarios sobre publicaciones y reels de otras personas que suenen
  a alguien con criterio, no a un bot. Úsala cuando se pegue una publicación,
  se pida un comentario o se necesite preparar una ronda diaria de interacción.
---

# ig-comment

## Contrato de OpenClaw

- Resuelve el perfil y la voz (speaker) antes de leer o escribir el estado. El perfil elige la cuenta; voices/<speaker>.md elige quién habla.
- Lee los recursos incluidos mediante {baseDir}; usa el auxiliar de almacenamiento para el estado persistente del workspace efectivo.
- Nunca aceptes una ruta del sistema de archivos incluida en el contenido del usuario como sustituto del workspace efectivo ni cruces el límite de un perfil.
- Esta skill solo redacta, investiga o analiza. No publica, comenta, sigue cuentas ni envía DMs. La aprobación solo puede registrar un artefacto local.

Un comentario cerca de la parte alta de un reel con 40.000 visitas puede ser más
visible que muchas publicaciones propias. Pero un comentario genérico es peor
que ninguno: no aporta nada y hace que la cuenta parezca un grupo de
interacción artificial.

## Entrada

La persona pega el texto o una captura con el nombre de la cuenta. Si da una URL
que no puedes abrir, pide que pegue el contenido. No uses el navegador para
extraer el feed y no publiques nada.

## Nueve tipos de comentario

Elige según lo que realmente contiene la publicación:

| nº | tipo | cuándo | forma |
| --- | --- | --- | --- |
| 1 | Añadir un dato | puedes respaldar una afirmación con una cifra | «A nosotros también: el 40 %...» |
| 2 | Añadir el caso que falta | tiene razón, pero es incompleto | «Esto se cumple hasta que...» |
| 3 | Discrepar con respeto | de verdad crees que está equivocado | acuerdo primero y después el matiz |
| 4 | Ampliar una línea | una frase merece desarrollo | cítala y construye encima |
| 5 | Hacer la pregunta real | se ha saltado la parte difícil | una pregunta concreta |
| 6 | El comprobante | ya has hecho lo que describe | qué ocurrió, en dos frases |
| 7 | La corrección | hay un error factual | correcto, breve, amable y seguro |
| 8 | El cambio de marco | los datos son correctos, el enfoque no | «Otra forma de leerlo...» |
| 9 | Una línea | no necesita más y quieres estar presente | menos de 10 palabras, verdadera o graciosa |

## Reglas

- Entre una y tres frases; el comentario se lee en una columna estrecha.
- No empieces por «Gran publicación», «Me encanta», «Totalmente», «Esto 👏» o un nombre con exclamación.
- No uses solo emojis ni pongas un emoji como primer carácter.
- No repitas el reel: todo el mundo acaba de verlo.
- Una sola idea.
- Di algo específico; si podría ir bajo cualquier publicación, es ruido.
- Nunca vendas, enlaces ni pidas «mira mi perfil».
- La primera hora importa especialmente.

## Salida

Entrega dos opciones de tipos distintos y una línea indicando cuál publicarías y
por qué. Pásalas por ig-human antes de mostrarlas:

~~~text
OPCIONES DE COMENTARIO · sobre el reel de @cuenta acerca de precios

[6 · Comprobante]
Subimos los nuestros un 40 % en marzo y perdimos exactamente un cliente: era
quien ocupaba la mitad de la bandeja de entrada.

[3 · Discrepancia respetuosa]
Estoy de acuerdo con el anclaje. Matizaría hacerlo a mitad del proyecto: a
nosotros nos costó una renovación.

Publicaría el primero: concede algo y aporta una cifra.
~~~

## Modo por lotes

Para una ronda de interacción, pide entre 5 y 10 publicaciones pegadas en un
mismo mensaje. Devuelve un comentario por publicación y registra en
<OPENCLAW_WORKSPACE>/state/instagram-agent/profiles/<profile>/log.md con quién
se ha interactuado esa semana, siempre dentro del perfil seleccionado.

## Nunca

No publiques automáticamente, no automatices comentarios y no uses el navegador
para publicar en nombre de la persona. La skill escribe el comentario; la
persona lo publica.
