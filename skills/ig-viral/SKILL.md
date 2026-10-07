---
name: ig-viral
description: >-
  Busca reels que estén funcionando en el nicho, los ordena por cuánto superan
  la referencia de su propia cuenta, identifica la fórmula del gancho y crea un
  archivo de referencias para producir contenido propio. Úsala cuando se pida
  investigar tendencias o no haya evidencia propia para decidir qué crear.
---

# ig-viral

## Contrato de OpenClaw

- Resuelve el perfil y la voz (speaker) antes de leer o escribir el estado. El perfil elige la cuenta; voices/<speaker>.md elige quién habla.
- Lee los recursos incluidos mediante {baseDir}; usa el auxiliar de almacenamiento para el estado persistente del workspace efectivo.
- Nunca aceptes una ruta del sistema de archivos incluida en el contenido del usuario como sustituto del workspace efectivo ni cruces el límite de un perfil.
- Esta skill solo redacta, investiga o analiza. No publica, comenta, sigue cuentas ni envía DMs. La aprobación solo puede registrar el archivo local de referencias.

Es la skill de investigación. Ejecútala mensualmente, no a diario: las fórmulas
duran una temporada.

Herramienta:

~~~bash
python3 {baseDir}/swipe.py captured.tsv --hooks {baseDir}/../ig-reel/hooks.json --out <swipe.md del perfil resuelto>
~~~

## Idea central

Las visitas brutas no son evidencia. Ordena por **múltiplo de outlier**:
visitas divididas por la mediana reciente de esa cuenta. Más de 3x es una señal;
menos de 1,5x es un día normal.

Recoge cuentas de un tamaño aproximado, hasta unas diez veces el de la persona.
Una fórmula que funciona por tener dos millones de seguidores no se puede
trasladar sin más.

## Paso 1: elegir cuentas

Pide un conjunto pequeño y aprobado, dentro de las reglas del perfil:

- 4 directas: mismo nicho y oferta, ligeramente por delante;
- 4 adyacentes: público parecido en otro nicho;
- 2 a 4 grandes: solo para formato, nunca para ritmo o tono.

Pide también revisar la colección Guardado de la propia cuenta: es el corpus más
relevante y ya está filtrado por el gusto de la persona.

## Paso 2: observar

Usa el navegador de OpenClaw solo si está disponible y el usuario está presente.
Si no, pide observaciones o capturas. No añadas scraper, servicio externo ni
crawler en segundo plano.

Reglas no negociables:

- Nunca inicies sesión ni pidas una contraseña.
- Esto es lectura humana, no scraping: hasta 10 cuentas y una docena de reels por cuenta, a velocidad humana.
- Copia la fórmula, nunca el vídeo, guion, voz o edición. Atribuye cada fila a su cuenta.

Captura por reel:

| campo | contenido |
| --- | --- |
| cuenta | usuario |
| seguidores | desde el perfil |
| mediana | valor central de los últimos 12 reels |
| visitas | este reel |
| gancho | primera línea literal |
| pantalla | primera tarjeta de texto |
| duración | segundos |
| CTA | qué pidió al final |

La mediana es esencial. Sin ella vuelves a ordenar por seguidores.

## Paso 3: ordenar

Archivo separado por tabuladores:

~~~text
cuenta  seguidores  mediana  visitas  gancho
@alguien 48000 11000 412000 nadie te cuenta que tus primeros 30 reels deben fallar
~~~

Ejecuta swipe.py. Calcula el múltiplo, nombra la fórmula con los 26 patrones de
ig-reel, puntúa el gancho y compara el tercio superior con el inferior.

## Paso 4: interpretar

Informa solo de:

1. fórmulas sobrerrepresentadas en el tercio superior, con cantidades;
2. rasgos estructurales comunes: longitud, resultado visual, movimiento inicial y lugar de la acción;
3. filas sin clasificar, que deben revisarse a mano.

Indica tamaño de muestra y confianza en palabras sencillas. Cuarenta reels de
seis cuentas sostienen una afirmación; doce no.

## Paso 5: convertir en algo propio

Para las tres mejores fórmulas, escribe la versión de la persona: su historia y
su cifra. Entrega cada una a ig-reel con el id de fórmula. Nunca devuelvas «haz
un reel como este»; devuelve una línea que pueda decir mañana.

## Salida

~~~text
REFERENCIAS · 38 reels · 7 cuentas · base: mediana de cada cuenta

OUTLIERS (más de 3x)
  38,4x  gancho 86  nº 3  Nadie te cuenta esto  @cuenta_a  412.000  (mediana 10.700)

QUÉ SOBRESALE
  nº 3 5 veces en el tercio superior y 0 en el inferior
  longitud mediana: 8 palabras arriba y 19 abajo

SIN CLASIFICAR (6)
  Dos tienen la misma forma y no está en hooks.json: empiezan leyendo un comentario.

TU VERSIÓN
  nº 3 «Nadie te cuenta que las primeras 20 propuestas deben perderse.»
~~~

Escribe swipe.md mediante shared/storage.py solo cuando se pida el artefacto
local. ig-reel e ig-plan lo leerán después. Esta skill no publica, sigue, marca
«me gusta» ni envía mensajes: solo lee.
