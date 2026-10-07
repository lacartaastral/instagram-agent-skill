# Instagram Agent OpenClaw

Fork mantenible y nativo para OpenClaw del proyecto
Jakeschincariol/instagram-agent-skill. Parte exactamente del baseline

d03c56bb598be770c60b201f94237e5d1a4268a6.

Conserva las 13 skills y sus heurísticas Python/JSON. Añade un boundary de
perfiles, voces, estado externo, reglas de plataforma verificables y routing
gobernado. El sistema prepara texto y análisis; no publica.

## 1. Origen y atribución

- Upstream: https://github.com/Jakeschincariol/instagram-agent-skill
- Baseline: d03c56bb598be770c60b201f94237e5d1a4268a6
- Fork: https://github.com/lacartaastral/instagram-agent-skill
- Licencia: MIT, conservada en LICENSE
- Autoría original: Jake Schincariol / opusjake.ai

Las métricas, límites y afirmaciones del upstream se consideran evidencia
histórica del baseline hasta que estén verificadas de nuevo. No se presentan
como resultados propios ni como garantía.

## 2. Diferencias respecto al upstream

- Se eliminan los manifiestos y rutas específicos del asistente original.
- SKILL.md sigue siendo el formato principal; los recursos de cada skill se
  resuelven mediante {baseDir}.
- Se añade shared/storage.py para localizar estado por workspace, perfil y voz,
  validar componentes y escribir de forma atómica.
- Se añade shared/model_routing.py y config/model-routing.json. Las skills no
  escogen modelos por su cuenta.
- Se añade ig-router, un orquestador pequeño que resuelve profile, speaker,
  intención, skill y tier sin redactar.
- Las reglas mutables viven en config/platform-rules.json y pueden ser
  sobreescritas por el platform-rules.json de cada perfil. Las reglas no
  verificadas generan warnings y no se convierten en hechos.
- La investigación viral usa el browser de OpenClaw solo para lectura humana
  de un conjunto pequeño. No hay crawler, login automatizado, Apify, Blotato ni
  servicios equivalentes.
- El approval gate queda explícito: NOTHING PUBLISHES UNTIL USER APPROVES.
  Incluso después de aprobar un borrador, la aprobación solo registra estado
  local; no habilita acciones sociales externas.

## 3. Instalación en OpenClaw

La instalación no requiere cambiar el modelo principal, credenciales,
proveedores ni políticas allow/deny. Desde un checkout escribible:

~~~bash
git clone https://github.com/lacartaastral/instagram-agent-skill.git /srv/openclaw/instagram-agent-openclaw
git -C /srv/openclaw/instagram-agent-openclaw remote add upstream https://github.com/Jakeschincariol/instagram-agent-skill.git
git -C /srv/openclaw/instagram-agent-openclaw fetch upstream
git -C /srv/openclaw/instagram-agent-openclaw switch openclaw/multiperfil-governed
~~~

Añade solo la raíz de skills como extensión, preservando la configuración
existente. Haz primero dry-run y comprueba el diff de configuración:

~~~bash
openclaw config set skills.load.extraDirs '["/srv/openclaw/instagram-agent-openclaw/skills"]' --strict-json --dry-run
openclaw config set skills.load.extraDirs '["/srv/openclaw/instagram-agent-openclaw/skills"]' --strict-json
openclaw skills list --eligible
~~~

La ruta anterior es la del host auditado; en otro host debe ser la ruta real
del checkout. No sustituyas openclaw.json completo. Si no se desea activar aún
la raíz, los tests locales siguen siendo ejecutables sin modificar OpenClaw.

## 4. Estructura

~~~text
instagram-agent-openclaw/
  README.md
  LICENSE
  UPSTREAM.md
  config/
    intent-routes.json
    model-routing.json
    platform-rules.json
    platform-rules.schema.json
  shared/
    model_routing.py
    platform_rules.py
    storage.py
  skills/
    ig-reel/
    ig-viral/
    ig-caption/
    ig-carousel/
    ig-story/
    ig-profile/
    ig-plan/
    ig-human/
    ig-comment/
    ig-reply/
    ig-dm/
    ig-repurpose/
    ig-audit/
    ig-router/
  templates/
    voice.md
  tests/
~~~

Las 13 skills originales se conservan. ig-router es la única skill nueva de
orquestación.

## 5. Perfiles y voces

El estado no vive dentro del checkout:

~~~text
<OPENCLAW_WORKSPACE>/state/instagram-agent/profiles/<profile>/
  brand.md
  facts.md
  offers.md
  swipe.md
  log.md
  plan.md
  platform-rules.json
  voices/
    <speaker>.md
~~~

Inicializa un perfil sin inventar contenido:

~~~bash
python3 shared/storage.py init --workspace <OPENCLAW_WORKSPACE> \
  --profile infancia-astral --voices miriam joaquin
~~~

Una cuenta y una voz son conceptos distintos. El mismo perfil puede tener
miriam.md y joaquin.md, y dos perfiles nunca comparten por accidente sus
archivos. El nombre de perfil y speaker se valida contra un conjunto seguro; no
se aceptan componentes con traversal.

infancia-astral es solo un perfil inicial de ejemplo. La lógica genérica no
contiene hechos astrológicos, posiciones, aspectos, interpretaciones ni claims
sobre esa marca. Si un contenido necesita datos astrológicos, debe recibirlos
de la fuente autorizada correspondiente.

Mantén separadas estas capas:

- brand voice: identidad y promesa de la cuenta;
- speaker voice: cómo habla una persona concreta;
- factual knowledge: hechos suministrados y trazables;
- offer: producto o servicio real;
- CTA: acción solicitada, sin inventar enlaces ni resultados.

## 6. Model routing

La política está en config/model-routing.json y fue contrastada con la
allowlist observada en la auditoría OpenClaw del 2026-10-07:

- Tier 0 DETERMINISTIC: scripts locales; no llama a un modelo.
- Tier 1 ROUTINE: default autorizado, actualmente openai/gpt-5.6-luna.
- Tier 2 QUALITY: solo delegación explícita, actualmente openai/gpt-5.6-sol.
- Tier 3 DEEP: solo delegación explícita, actualmente openai/gpt-6-astra.

Los IDs son una instantánea y deben compararse con la allowlist live antes de
usar Tier 2/3. Si no están autorizados, el routing falla cerrado. La skill no
modifica la allowlist, no convierte Sol en modelo global y no usa Astra por
defecto. La delegación se realiza mediante el mecanismo nativo de OpenClaw con
model y thinking explícitos.

## 7. Reglas de plataforma

config/platform-rules.json centraliza límites, dimensiones, safe zones,
duraciones y claims de comportamiento. Cada regla contiene value,
verified_at, source, notes y verified. Los valores heredados del baseline están
marcados no verificados; el linter los muestra como warnings. Un perfil puede
overlayar sus reglas sin editar las 13 skills.

## 8. Investigación viral

ig-viral trabaja con browser disponible en OpenClaw solo si está habilitado y
el usuario está presente. Lee una muestra pequeña, calcula el outlier multiple
frente a la mediana de la propia cuenta y copia estructuras, no contenido. No
pide contraseñas, no inicia sesión por el usuario, no hace crawling masivo y no
ejecuta automatizaciones de crecimiento.

## 9. Approval gate

Las skills pueden investigar, analizar, redactar, puntuar, planificar, preparar
assets y registrar un artefacto local aprobado. No pueden publicar, comentar,
seguir cuentas, enviar DMs ni ejecutar acciones sociales irreversibles. No se
implementa una extensión de publicación en este fork.

## 10. Tests y smoke tests

No hay dependencias Python externas para la suite determinista:

~~~bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q shared skills

printf '%s\n' 'A hook with a real number' | \
  python3 skills/ig-reel/hookscore.py --json
printf '%s\n' 'A true sentence. Another concrete sentence.' | \
  python3 skills/ig-human/humanize.py --json
printf '%s\n' 'Comment CONTRACT and save this.' | \
  python3 skills/ig-caption/caption.py --json
~~~

Para validar discovery después de activar la raíz:

~~~bash
openclaw skills list --eligible
openclaw skills list --json
~~~

La suite comprueba carga de las 13 skills y ig-router, ausencia de rutas
específicas del asistente original, resolución de recursos, aislamiento entre
perfiles/voces, routing sin Sol/Astra para Tier 0 y lectura de las reglas
centralizadas.

## 11. Sincronizar upstream

No edites el upstream directamente. Los remotes esperados son:

~~~bash
git remote -v
# origin   https://github.com/lacartaastral/instagram-agent-skill.git
# upstream https://github.com/Jakeschincariol/instagram-agent-skill.git
~~~

Flujo conservador:

~~~bash
git fetch --no-tags upstream
git switch openclaw/multiperfil-governed
git diff HEAD upstream/main -- skills templates README.md
# revisar manualmente, actualizar tests y platform-rules si procede
git merge --no-commit upstream/main
python3 -m unittest discover -s tests -v
git diff --check
git commit
~~~

No aceptes automáticamente cambios que reintroduzcan rutas del asistente
original, publicación, scraping masivo, datos inventados o mezcla de estado.
