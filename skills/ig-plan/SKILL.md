---
name: ig-plan
description: >-
  Organiza la semana de Instagram: qué publicar, en qué formato, cuándo y con
  quién interactuar. Úsala cuando se pida un calendario, una planificación
  semanal o ideas para publicar.
---

# ig-plan

## Contrato de OpenClaw

- Resuelve el perfil y la voz (speaker) antes de leer o escribir el estado. El perfil elige la cuenta; voices/<speaker>.md elige quién habla.
- Lee los recursos incluidos mediante {baseDir}; usa el auxiliar de almacenamiento para el estado persistente del workspace efectivo.
- Nunca aceptes una ruta del sistema de archivos incluida en el contenido del usuario como sustituto del workspace efectivo ni cruces el límite de un perfil.
- Esta skill solo redacta, investiga o analiza. No publica, comenta, sigue cuentas ni envía DMs. La aprobación solo puede registrar un plan local.

Es la sala de control del paquete. Conviene ejecutarla una vez por semana, el
mismo día.

## Entrada

Lee mediante shared/storage.py, si existen, brand.md, facts.md, offers.md,
voices/<speaker>.md, swipe.md y log.md del perfil seleccionado. El archivo de
referencias contiene evidencia de ig-viral y el registro evita repetir temas de
las dos últimas semanas.

Si faltan, pregunta y registra:

1. Qué vende la persona y a quién.
2. Tres o cuatro temas por los que quiere ser conocida.
3. Qué ocurrió esta semana: llamada, cifra, error, cosa construida o discusión.
4. Diez cuentas ante las que merece la pena ser visible.

## Qué publicar

Usa hechos del perfil y evidencia reciente para elegir un ritmo sostenible. No
presentes como hechos actuales las afirmaciones de distribución: consulta
platform-rules.json y la auditoría de la cuenta.

Alterna durante la semana:

| tipo | frecuencia | trabajo |
| --- | --- | --- |
| **Prueba** | 1 por semana | algo que ocurrió, con una cifra; reel |
| **Enseñanza** | 1 o 2 por semana | algo que se pueda hacer hoy; reel o carrusel |
| **Opinión** | 1 por semana | una postura que pueda restar seguidores; reel |
| **Historia** | 1 cada dos semanas | una escena con un coste; reel |
| **Oferta** | 1 cada dos semanas | lo que se vende, de forma clara; carrusel o stories |

Para cada hueco indica tema, ángulo concreto basado en lo ocurrido, formato y
fórmula de gancho de ig-reel/hooks.json. «IA» no es un plan; «perdimos la
propuesta porque el borrador tenía una raya larga» sí lo es.

## Cuándo publicar

Como punto de partida, publica cuando la audiencia esté despierta y no
trabajando: primera hora de la tarde-noche para consumo y primera hora de la
mañana para público profesional. Si la zona horaria de la audiencia difiere,
usa la suya.

Dilo con claridad: **la hora importa mucho menos que los dos primeros
segundos**. Si los ganchos no funcionan, optimizar horarios es pulir lo
secundario.

## Ronda de interacción

Veinte minutos al día, antes de publicar:

- 5 cuentas de alcance, donde un buen comentario se vea;
- 3 pares del mismo sector y tamaño;
- 2 posibles compradores, sin vender en el comentario.

Entrega la lista a ig-comment.

## Salida

~~~text
SEMANA DEL 15 DE SEPTIEMBRE

LUN  solo interacción (20 min)
MAR  19:30  REEL       PRUEBA       fórmula 5 · de 5 h a 20 min
MIÉ  solo stories + interacción
JUE  19:00  CARRUSEL   ENSEÑANZA    desglose de una cláusula
VIE  19:30  REEL       OPINIÓN      deja de hacer llamadas de diagnóstico
SÁB  -
DOM  18:00  REEL       HISTORIA     el correo de devolución

STORIES cada día, 3 a 5 pantallas.
INTERACCIÓN 5 alcance / 3 pares / 2 compradores.

Di «escribe el martes» y redactaré ese contenido.
~~~

Resuelve plan.md con shared/storage.py y escríbelo solo si la persona pide el
registro local. No se programa ni publica nada: es un plan que ejecuta la
persona.
