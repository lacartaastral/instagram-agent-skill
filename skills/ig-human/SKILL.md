---
name: ig-human
description: >-
  Quita la huella mecánica de un borrador: rayas largas, palabras de relleno,
  caracteres invisibles y estructuras repetitivas. Después lo puntúa con cinco
  comprobaciones antes de enseñarlo. Úsala cuando un texto suene a IA o antes de
  mostrar un caption, guion, comentario, respuesta o DM.
---

# ig-human

## Contrato de OpenClaw

- Resuelve el perfil y la voz (speaker) antes de leer o escribir el estado. El perfil elige la cuenta; voices/<speaker>.md elige quién habla.
- Lee los recursos incluidos mediante {baseDir}; usa el auxiliar de almacenamiento para el estado persistente del workspace efectivo.
- Nunca aceptes una ruta del sistema de archivos incluida en el contenido del usuario como sustituto del workspace efectivo ni cruces el límite de un perfil.
- Esta skill solo redacta, investiga o analiza. No publica, comenta, sigue cuentas ni envía DMs. La aprobación solo puede registrar un artefacto local.

Hay dos herramientas en esta carpeta y ambas funcionan. Úsalas; no hagas una
revisión visual a ojo:

~~~bash
python3 {baseDir}/humanize.py borrador.txt --report        # limpia y muestra cambios
python3 {baseDir}/detect.py borrador.txt                    # puntúa cinco señales
python3 {baseDir}/detect.py antes.txt despues.txt           # muestra la diferencia
~~~

Ambas leen {baseDir}/slop.json: palabras y frases prefabricadas, caracteres
invisibles, sustituciones tipográficas y señales estructurales. El archivo se
puede editar. Si elimina una palabra que la persona usa de verdad, quítala del
lexicón.

## Qué corrige automáticamente

1. **Caracteres invisibles:** espacios de ancho cero, separadores, guiones
   blandos, marcas Unicode y espacios no separables.
2. **Tipografía:** raya larga por coma, raya corta por guion, comillas curvas
   por rectas, elipsis por tres puntos y viñetas por guion.
3. **Lexicón de relleno:** vocabulario grandilocuente y fórmulas de apertura o
   cierre que hacen que un caption parezca una plantilla.

## Qué solo marca

Las señales estructurales necesitan criterio humano:

- «No es solo X, es Y».
- «No solo X, sino también Y».
- tríos de regla de tres;
- preguntas retóricas de una palabra;
- prólogos de vídeo;
- listas de emojis;
- tres o más palabras en mayúsculas seguidas;
- muros de hashtags;
- llamadas genéricas a seguir, etiquetar o comentar.

Reescribe cada línea marcada conservando el significado y vuelve a ejecutar
 detect.py. Esa parte no debe hacerla una sustitución automática.

## Las cinco comprobaciones

La herramienta puntúa de 0 a 100, donde más alto significa más natural:

| comprobación | mide | aspecto mecánico |
| --- | --- | --- |
| RITMO | variación de longitud de frases | todas tienen el mismo tamaño |
| CONCRECIÓN | nombres, cifras y señales concretas | sustantivos abstractos |
| RELLENO | coincidencias del lexicón | vocabulario de plantilla |
| HUELLA | caracteres invisibles y tipografía | texto demasiado perfecto |
| VOZ | persona, contracciones y estructuras | revelaciones preparadas |

El veredicto usa la media al 60 % y la comprobación más débil al 40 %. LISTO
requiere una media de 70 o más y ninguna señal por debajo de 55.

## Decirlo con honestidad

Son heurísticas locales inspiradas en señales públicas. Se ejecutan en el equipo
del usuario y no suben el texto. No son detectores comerciales, no llaman a sus
APIs y no pueden prometer sus veredictos. No digas nunca que un texto es
indetectable.

## Orden de trabajo

1. humanize.py borrador.txt -o limpio.txt --report
2. Lee las señales estructurales y reescríbelas a mano.
3. detect.py borrador.txt limpio.txt para mostrar el antes y el después.
4. Si no está LISTO, corrige la señal más débil y repite. Dos rondas son normales; cinco indican que hay que cambiar el borrador.
5. Enseña el texto limpio y la puntuación, nunca la puntuación sola.
