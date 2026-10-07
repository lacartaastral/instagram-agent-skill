---
name: ig-profile
description: >-
  Puntúa un perfil de Instagram sobre 100 con una rúbrica de 12 partes y
  reescribe lo que pierde puntos: nombre, bio, enlace, destacados, tres fijadas
  y cuadrícula. Úsala cuando se pida optimizar un perfil o arreglar una bio.
---

# ig-profile

## Contrato de OpenClaw

- Resuelve el perfil y la voz (speaker) antes de leer o escribir el estado. El perfil elige la cuenta; voices/<speaker>.md elige quién habla.
- Lee los recursos incluidos mediante {baseDir}; usa el auxiliar de almacenamiento para el estado persistente del workspace efectivo.
- Nunca aceptes una ruta del sistema de archivos incluida en el contenido del usuario como sustituto del workspace efectivo ni cruces el límite de un perfil.
- Esta skill solo redacta, investiga o analiza. No publica, comenta, sigue cuentas ni envía DMs. La aprobación solo puede registrar un borrador local.

El perfil no es un escaparate: es una pantalla de decisión a la que se llega
desde un reel. Tiene unos tres segundos para responder si aquí hay más contenido
así y si es para esa persona.

## Entrada

Pide nombre, usuario, bio, destino del enlace, nombres de destacados, contenido
fijado y las nueve primeras portadas. Una captura de la parte superior y dos
filas suele bastar para una primera revisión.

No inicies sesión en Instagram en nombre de la persona.

## Puntuación

Lee {baseDir}/rubric.json. Son 12 elementos y 100 puntos. Puntúa todos, enseña
la tabla y da el total. La mayoría de perfiles queda entre 30 y 40 la primera
vez; una puntuación generosa no sirve.

~~~text
PUNTUACIÓN DEL PERFIL 38/100

campo de nombre       2/12   solo un nombre, sin palabras buscables
primera línea de bio   3/12   tres sustantivos y un emoji de café
las tres fijadas       0/10   nada fijado
destacados             2/8    «Random», «Vida», «2023»
legibilidad cuadrícula 4/8    seis portadas muestran una cara a mitad de palabra
~~~

## Reescritura por orden

1. **Campo de nombre, 30 caracteres:** nombre más aquello que hace en palabras buscables. Da tres opciones.
2. **Primera línea de bio:** para quién es y qué cambia; no un cargo ni adjetivos.
3. **Tres fijadas:** prueba, explicación de la oferta y presentación de la persona.
4. **Destacados:** entre cuatro y seis, llamados Precios, Resultados, Cómo funciona y Sobre mí.
5. **Enlace:** un destino que coincida con la promesa de la bio.
6. **Portadas:** nueve primeras, legibles en miniatura y elegidas a propósito.

## Salida

Entrega la tabla, los bloques listos para copiar en orden de impacto y una nueva
puntuación honesta. Si llega a 84 y no a 98, di 84 y explica qué queda: suele
ser la cuadrícula, el hábito de stories o una publicación fijada que todavía no
existe.

Nada se guarda en Instagram. La persona edita cada campo.
