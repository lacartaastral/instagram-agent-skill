---
name: ig-caption
description: >-
  Escribe el caption de Instagram: la línea que queda antes del corte, el cuerpo,
  una sola llamada a la acción, los términos de búsqueda y hasta cinco hashtags;
  después lo revisa. Úsala cuando haya un reel o carrusel listo y falte el texto.
---

# ig-caption

## Contrato de OpenClaw

- Resuelve el perfil y la voz (speaker) antes de leer o escribir el estado. El perfil elige la cuenta; voices/<speaker>.md elige quién habla.
- Lee los recursos incluidos mediante {baseDir}; usa el auxiliar de almacenamiento para el estado persistente del workspace efectivo.
- Nunca aceptes una ruta del sistema de archivos incluida en el contenido del usuario como sustituto del workspace efectivo ni cruces el límite de un perfil.
- Esta skill solo redacta, investiga o analiza. No publica, comenta, sigue cuentas ni envía DMs. La aprobación solo puede registrar un artefacto local.

Herramienta de esta carpeta:

~~~bash
python3 {baseDir}/caption.py caption.txt
python3 {baseDir}/caption.py caption.txt --keywords "propuestas para clientes,precios de agencia"
~~~

Carga el platform-rules.json del perfil seleccionado. Los valores no verificados
aparecen como avisos: no los conviertas en hechos de la plataforma.

## Primero decide el trabajo del caption

**Trabajo A: el vídeo ya tiene gancho.** El reel lleva su propio gancho en los
primeros dos segundos, hablado y en pantalla. El caption aporta contexto, una
acción y palabras que la gente busca; no compite con el vídeo.

**Trabajo B: el caption es el contenido.** Para una foto, imagen única o portada
de carrusel, la primera línea es el gancho: concreta, breve y cortada en un
punto de curiosidad.

Pregunta cuál de los dos estás escribiendo. Si el reel ya tiene un buen gancho,
usa A y explícalo.

## Estructura

~~~text
Línea 1    ventana de previsualización configurada. En A: la acción, clara.
           En B: el gancho. Nunca un saludo, hashtag o emoji inicial.
Cuerpo     párrafos cortos, con una línea en blanco. Entre dos y seis.
Acción     una sola: comentar una palabra, guardar o enviar un DM.
Hashtags   hasta cinco en una línea propia, o ninguno.
~~~

El límite configurado es 2.200 caracteres, pero casi nunca hacen falta. Un
caption que consigue el toque y entrega 600 caracteres suele ser mejor que uno
de 1.800.

## Hashtags y búsqueda

Los límites de hashtags y las afirmaciones de distribución viven en
platform-rules.json. Usa el linter del perfil y muestra el estado no verificado
en vez de afirmar un límite actual. Los hashtags son opcionales y deben ser
específicos.

Los términos de búsqueda importan más que rellenar hashtags. Pide dos o tres
frases y pásalas al linter:

~~~bash
python3 {baseDir}/caption.py borrador.txt --keywords "propuestas para clientes,precios de agencia"
~~~

## Reglas

- No pongas un enlace en el cuerpo: el usuario lo encontrará en bio o DM.
- Una sola acción. Dos acciones equivalen a ninguna.
- La palabra clave debe poder escribirse: una palabra, sin espacios ni emoji.
- Si hay un enlace, redacta el primer comentario por separado.
- Usa el emoji como puntuación, no como decoración; el linter avisa si hay demasiados.
- Para carruseles y fotos, añade texto alternativo.

## Flujo

1. Decide A o B y dilo.
2. Redacta.
3. Pasa el texto por ig-human.
4. Ejecuta caption.py con los términos de búsqueda y las reglas del perfil.
   Corrige cada FAIL y decide cada WARN en voz alta.
5. Devuelve el bloque listo para copiar y un recibo:

~~~text
CAPTION LISTO
trabajo:    A - el reel ya lleva el gancho
visible:    ventana de previsualización configurada
acción:     una, comentar CONTRATO
hashtags:   3
búsqueda:   "propuestas para clientes" en línea 3
linter:     LISTO
~~~

No se publica. La persona lo copia y lo pega.
