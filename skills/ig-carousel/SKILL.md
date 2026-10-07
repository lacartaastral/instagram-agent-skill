---
name: ig-carousel
description: >-
  Construye un carrusel de Instagram: portada que gana el deslizamiento, texto
  diapositiva a diapositiva y recursos preparados según las reglas del perfil
  para una carga manual. Úsala cuando se pida un carrusel, diapositivas o
  convertir una idea en carrusel.
---

# ig-carousel

## Contrato de OpenClaw

- Resuelve el perfil y la voz (speaker) antes de leer o escribir el estado. El perfil elige la cuenta; voices/<speaker>.md elige quién habla.
- Lee los recursos incluidos mediante {baseDir}; usa el auxiliar de almacenamiento para el estado persistente del workspace efectivo.
- Nunca aceptes una ruta del sistema de archivos incluida en el contenido del usuario como sustituto del workspace efectivo ni cruces el límite de un perfil.
- Esta skill solo redacta, investiga o analiza. No publica, comenta, sigue cuentas ni envía DMs. La aprobación solo puede registrar un artefacto local.

Los carruseles favorecen el tiempo de lectura porque deslizar es una interacción
y desplazarse no. También pueden mostrarse otra vez empezando por una
diapositiva posterior, por lo que la segunda debe sostenerse sola.

El formato premia una idea dividida en pasos y castiga un caption partido en
pedazos.

## Cuándo usarlo en lugar de un reel

Usa carrusel cuando la idea tenga secuencia y necesite releerse: pasos, marco,
antes y después o una lista que merezca una captura. Usa reel si necesita
movimiento, una cara o un resultado que deba verse.

Si solo hay una afirmación, no es ninguna de las dos cosas: pásala a ig-reel.

## Estructura

Entre 6 y 10 diapositivas. El máximo técnico puede ser 20, pero 20 suele ser un
libro que nadie termina. Con menos de 5 no empieza el deslizamiento.

~~~text
1       PORTADA    gancho de seis palabras o menos y una promesa debajo.
2       APUESTA    por qué importa, en una frase. También debe funcionar como segunda portada.
3 a N   UNA IDEA POR DIAPOSITIVA. Título de 3-7 palabras y hasta 25 debajo.
N+1     RESUMEN    todo en forma de lista; es la diapositiva para capturar.
ÚLTIMA  CTA        una acción: guardar, comentar una palabra o seguir.
~~~

## Reglas del texto y del diseño

- La portada es la mayor parte del resultado: seis palabras, grande y legible en miniatura.
- Lee canvas y recorte del platform-rules.json del perfil; marca como ayuda de revisión lo que no esté verificado.
- Numera las diapositivas (3/8) para que se vea el final.
- Si una diapositiva necesita un párrafo, divídela.
- El resumen debe poder capturarse y entenderse sin contexto.
- Pon el usuario en una esquina de cada diapositiva.
- Añade texto alternativo como mínimo a la portada.

## Construir los archivos

Lee canvas, recorte y número de elementos del perfil. Si algún valor no está
verificado, indícalo. Puedes preparar HTML local:

~~~html
<!-- una section por diapositiva y page-break-after: always -->
<!-- usa un renderizador local ya disponible; no añadas un servicio de publicación -->
~~~

Usa las dimensiones del perfil, un solo color de acento y una tipografía legible
en móvil. Si existe una identidad visual, respétala y no inventes una paleta.

## Salida

Primero entrega el texto de cada diapositiva como lista numerada. Después el
caption, que aquí realiza el trabajo B de ig-caption. Pasa ambos por ig-human y
construye archivos solo después de que la persona apruebe el copy.

~~~text
CARRUSEL · 8 diapositivas

1  PORTADA   LA CLÁUSULA DE 18.000 €
              Una línea que ahora pongo en cada contrato.
2  APUESTA   Aprobé el trabajo. Nueve días después pidieron devolver el dinero.
3            QUÉ DICE
              Pago a la entrega, no al aprobar.
7  RESUMEN    Las cuatro líneas, en orden.
8  CTA        Comenta CONTRATO y te envío la cláusula completa.

Caption: trabajo B, gancho en línea 1, una acción y tres etiquetas.
~~~

No se sube nada. La persona lo publica manualmente.
