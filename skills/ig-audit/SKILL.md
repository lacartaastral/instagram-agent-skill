---
name: ig-audit
description: >-
  Analiza lo que la persona ya ha publicado: qué reels funcionaron, por qué y
  qué conviene dejar de hacer. Úsala cuando comparta estadísticas, publicaciones
  anteriores o pregunte qué funciona, por qué algo fracasó o qué debe repetir.
---

# ig-audit

## Contrato de OpenClaw

- Resuelve el perfil y la voz (speaker) antes de leer o escribir el estado. El perfil elige la cuenta; voices/<speaker>.md elige quién habla.
- Lee los recursos incluidos mediante {baseDir}; usa el auxiliar de almacenamiento para el estado persistente del workspace efectivo.
- Nunca aceptes una ruta del sistema de archivos incluida en el contenido del usuario como sustituto del workspace efectivo ni cruces el límite de un perfil.
- Esta skill solo redacta, investiga o analiza. No publica, comenta, sigue cuentas ni envía DMs. La aprobación puede registrar un borrador, plan o entrada de registro, pero no ejecutar una acción social externa.

La única fuente honesta de lo que funciona para una cuenta es esa cuenta. Todas
las reglas de las guías de Instagram, incluidas las de este paquete, son una
hipótesis previa. Las últimas 30 publicaciones de la persona son la evidencia.

## Entrada

Pide lo que tenga disponible:

- Estadísticas por publicación: visitas, alcance, interacciones, tiempo de
  reproducción, guardados, compartidos, seguidores ganados y porcentaje de
  alcance de personas que no seguían la cuenta.
- O el gráfico de retención del mejor y el peor reel reciente.
- O las publicaciones con sus visitas, suficiente para una primera lectura.

Resuelve el log.md del perfil con shared/storage.py y léelo solo si existe. Solo
registra qué fórmula de gancho usó cada publicación; nunca leas otro perfil.

## Qué medir

Las visitas brutas son el número menos útil. Calcula esto y enseña la cuenta:

| métrica | cálculo | qué indica |
| --- | --- | --- |
| **Múltiplo de outlier** | visitas / mediana propia de la cuenta | si fue un éxito real o un día normal |
| **Alcance no seguidor** | porcentaje de alcance de no seguidores | si el contenido viajó fuera de la audiencia |
| **Retención a 3 s** | personas a los 3 s / personas que empezaron | si funcionó el gancho |
| **Tiempo medio** | el dato de estadísticas | si funcionó la parte central |
| **Envíos por alcance** | compartidos / alcance | la señal más fuerte de recomendación |
| **Seguimientos por alcance** | seguidores ganados / alcance | si el perfil convirtió la atención |

Ordena por múltiplo de outlier y envíos por alcance, no por visitas. Un reel con
4.000 visitas y 90 envíos puede superar a uno con 60.000 visitas y 11 envíos.

## Busca el patrón

Compara los cinco primeros y los cinco últimos. Revisa:

- retención a 3 segundos;
- fórmula del gancho, usando ids de ig-reel/hooks.json;
- formato: reel, carrusel o imagen;
- duración: menos de 15 s, 15-30 s, 30-60 s o más de 60 s;
- tema;
- si se respondieron comentarios durante la primera hora;
- día y hora, solo al final y solo si todo lo demás no explica nada.

Expón cada hallazgo como afirmación con evidencia y nivel de confianza. Con 30
publicaciones se puede ver un patrón; con seis no, y es mejor decirlo que
inventarlo.

## La distinción importante

**Un reel con visitas y sin seguidores no es necesariamente un reel fallido: es
un problema de perfil.** Un reel sin visitas suele ser un problema de gancho.
Separa ambas cosas antes de recomendar. Si el alcance no seguidor es alto y los
seguimientos por alcance son bajos, deja de reescribir ganchos y pasa a
ig-profile.

## Salida

~~~text
AUDITORÍA · 31 publicaciones · 12 jun - 5 sep · mediana 4.100 visitas

TOP 5 POR MÚLTIPLO DE OUTLIER
  18,2x  nº 3  Nadie te cuenta esto  74.600 visitas  62 % no seguidores  128 envíos

QUÉ DICEN LOS DATOS
1. La retención a 3 segundos explica casi todo.
2. Las publicaciones donde la persona queda expuesta superan a las demás.
3. Las listas de herramientas tienen visitas, pero pocos envíos y seguimientos.
4. El día de la semana no muestra una diferencia útil.
~~~

Entrega las conclusiones a ig-plan para construir la semana con evidencia propia
y a ig-viral para filtrar el archivo de referencias hacia las fórmulas que
funcionan en esa cuenta.
