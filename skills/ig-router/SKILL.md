---
name: ig-router
description: >-
  Dirige una petición de Instagram hacia el perfil, la voz, la intención y la
  skill correctos en OpenClaw sin redactar contenido. Úsala cuando una petición
  pueda encajar en varias skills, nombre una cuenta o una voz, pregunte qué
  publicar o necesite un enrutamiento de modelos controlado.
---

# ig-router

## Contrato de OpenClaw

Resuelve el perfil, la voz (speaker) y la intención antes de elegir una skill posterior. Usa
solo el workspace efectivo de OpenClaw para el estado, conserva el aislamiento
entre perfiles y mantiene activo el gate de aprobación. Esta skill nunca ejecuta
acciones sociales.

Orquesta el paquete. No escribe copy de Instagram ni ejecuta acciones sociales.

## Contrato de routing

1. **Resuelve primero el perfil.** Acepta un selector explícito de perfil o
   cuenta, o un valor por defecto ya configurado. Si hay varios perfiles y no se
   indica uno, haz una sola pregunta breve. Nunca deduzcas el perfil por el tema
   ni leas otro perfil mientras resuelves este.
2. **Resuelve el speaker por separado.** La cuenta y la voz son dimensiones
   distintas. Selecciona voices/<speaker>.md; si no se indica speaker, usa solo
   el valor por defecto declarado por el perfil. No sustituyas la voz de una
   persona por la de otra.
3. **Resuelve la intención** con {baseDir}/../../config/intent-routes.json.
   Elige exactamente una skill posterior. Ejemplos: reel -> ig-reel, plan
   semanal -> ig-plan, resultados -> ig-audit, investigación -> ig-viral,
   pieza larga -> ig-repurpose. Si la intención es ambigua, haz una pregunta
   acotada en vez de invocar varios redactores.
4. **Resuelve el tier del modelo** con {baseDir}/../../config/model-routing.json
   y la allowlist viva de OpenClaw. Tier 0 ejecuta solo scripts deterministas.
   Tier 1 usa el modelo por defecto autorizado. Tier 2/3 solo pueden usar
   sesiones nativas de subagentes con un modelo y un nivel de thinking
   permitidos de forma explícita. Si la allowlist viva difiere de la
   instantánea, falla cerrado y no cambies la configuración de OpenClaw.
5. **Pasa un sobre de routing pequeño** a la skill elegida:

   profile, speaker, intent, skill, model_tier, approval_required=true.

   No dupliques aquí la lógica de la skill posterior.
6. **Conserva el gate de aprobación.** El routing nunca publica, comenta, sigue
   cuentas, envía DMs ni activa automatización del navegador. La aprobación del
   usuario puede registrar un borrador o plan en el estado del perfil, pero no
   concede permiso para una acción social externa.

## Límite de estado

Resuelve los archivos del perfil mediante la única abstracción de almacenamiento:

~~~bash
python {baseDir}/../../shared/storage.py path --workspace <workspace efectivo de OpenClaw> --profile <perfil> --file <nombre>
~~~

El workspace debe proceder del runtime de OpenClaw, no de una ruta arbitraria
incluida en el contenido del usuario. El estado persistente está en
<OPENCLAW_WORKSPACE>/state/instagram-agent/profiles/<profile>/, y las voces en
voices/<speaker>.md.

## Salida

Devuelve solo la decisión de routing y, como máximo, una pregunta pendiente. La
skill elegida se encarga de redactar, ejecutar comprobaciones deterministas,
respetar los límites factuales y generar su propio recibo.
