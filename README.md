# Instagram Agent para OpenClaw

Fork mantenible y nativo para OpenClaw del proyecto
Jakeschincariol/instagram-agent-skill. Parte exactamente del commit base

d03c56bb598be770c60b201f94237e5d1a4268a6.

Conserva las 13 skills originales y sus heurísticas Python/JSON. Añade un límite
seguro entre perfiles, voces y estado externo, reglas de plataforma verificables
y un enrutamiento de modelos gobernado. El sistema prepara texto y análisis;
no publica.

## 1. Origen y atribución

- Repositorio de origen: https://github.com/Jakeschincariol/instagram-agent-skill
- Commit base: d03c56bb598be770c60b201f94237e5d1a4268a6
- Fork: https://github.com/lacartaastral/instagram-agent-skill
- Licencia: MIT, conservada en LICENSE
- Autoría original: Jake Schincariol / opusjake.ai

Las métricas, límites y afirmaciones del repositorio de origen se consideran
evidencia histórica del commit base hasta que se verifiquen de nuevo. No se
presentan como resultados propios ni como garantías.

## 2. Diferencias respecto al repositorio de origen

- Se eliminan sus manifiestos y rutas específicas del asistente original.
- SKILL.md sigue siendo el formato principal; los recursos de cada skill se
  resuelven mediante {baseDir}.
- shared/storage.py localiza el estado por workspace, perfil y voz, valida los
  componentes y escribe de forma atómica.
- shared/model_routing.py y config/model-routing.json centralizan la política.
  Las skills no eligen modelos por su cuenta.
- ig-router resuelve perfil, voz (speaker), intención, skill y tier sin redactar.
- Las reglas mutables viven en config/platform-rules.json y pueden ser
  sobreescritas por el platform-rules.json de cada perfil. Las reglas no
  verificadas generan avisos y no se convierten en hechos.
- La investigación viral usa el navegador de OpenClaw solo para lectura humana
  de un conjunto pequeño. No hay crawler, login automatizado ni servicios
  externos de crecimiento.
- El gate de aprobación queda explícito: NO SE PUBLICA NADA HASTA QUE EL
  USUARIO LO APRUEBA. Incluso después de aprobar un borrador, la aprobación
  solo registra estado local; no habilita acciones sociales externas.

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
existente. Haz primero un dry-run y comprueba el diff de configuración:

~~~bash
openclaw config set skills.load.extraDirs '["/srv/openclaw/instagram-agent-openclaw/skills"]' --strict-json --dry-run
openclaw config set skills.load.extraDirs '["/srv/openclaw/instagram-agent-openclaw/skills"]' --strict-json
openclaw skills list --eligible
~~~

La ruta anterior es la del host auditado; en otro host debe ser la ruta real del
checkout. No sustituyas openclaw.json completo. Si todavía no se desea activar
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

- voz de marca: identidad y promesa de la cuenta;
- voz seleccionada: cómo habla una persona concreta;
- conocimiento factual: hechos suministrados y trazables;
- oferta: producto o servicio real;
- CTA: acción solicitada, sin inventar enlaces ni resultados.

## 6. Enrutamiento de modelos

La política está en config/model-routing.json y fue contrastada con la allowlist
observada en la auditoría de OpenClaw del 2026-10-07:

- Tier 0 DETERMINISTIC: scripts locales; no llama a un modelo.
- Tier 1 ROUTINE: modelo autorizado por defecto, actualmente
  openai/gpt-5.6-luna.
- Tier 2 QUALITY: solo delegación explícita, actualmente
  openai/gpt-5.6-sol.
- Tier 3 DEEP: solo delegación explícita, actualmente openai/gpt-6-astra.

Los identificadores son una instantánea y deben compararse con la lista permitida (allowlist) viva
antes de usar Tier 2/3. Si no están autorizados, el enrutamiento falla cerrado.
La skill no modifica la lista permitida, no convierte Sol en modelo global y no usa
Astra por defecto. La delegación se realiza mediante el mecanismo nativo de
OpenClaw con model y thinking explícitos.

## 7. Reglas de plataforma

config/platform-rules.json centraliza límites, dimensiones, zonas seguras,
duraciones y afirmaciones de comportamiento. Cada regla contiene value,
verified_at, source, notes y verified. Los valores heredados del commit base están
marcados como no verificados; el linter los muestra como avisos. Un perfil
puede superponer sus reglas sin editar las 13 skills.

## 8. Investigación viral

ig-viral trabaja con el navegador disponible en OpenClaw solo si está habilitado
y el usuario está presente. Lee una muestra pequeña, calcula el múltiplo de
outlier frente a la mediana de la propia cuenta y copia estructuras, no
contenido. No pide contraseñas, no inicia sesión por el usuario, no hace
crawling masivo y no ejecuta automatizaciones de crecimiento.

## 9. Gate de aprobación

Las skills pueden investigar, analizar, redactar, puntuar, planificar, preparar
assets y registrar un artefacto local aprobado. No pueden publicar, comentar,
seguir cuentas, enviar DMs ni ejecutar acciones sociales irreversibles. Este fork
no implementa una extensión de publicación.

## 10. Tests y pruebas rápidas

No hay dependencias Python externas para la suite determinista:

~~~bash
python3 -m unittest discover -s tests -v
python3 -m compileall -q shared skills

printf '%s\n' 'Un gancho con una cifra real' | \
  python3 skills/ig-reel/hookscore.py --json
printf '%s\n' 'Una frase cierta. Otra frase concreta.' | \
  python3 skills/ig-human/humanize.py --json
printf '%s\n' 'Comenta CONTRATO y guárdalo.' | \
  python3 skills/ig-caption/caption.py --json
~~~

Para validar el discovery después de activar la raíz:

~~~bash
openclaw skills list --eligible
openclaw skills list --json
~~~

La suite comprueba la carga de las 13 skills y ig-router, la ausencia de rutas
específicas del sistema original, la resolución de recursos, el aislamiento
entre perfiles y voces, el enrutamiento sin Sol/Astra para Tier 0 y la lectura
de las reglas centralizadas.

## 11. Sincronizar el repositorio de origen

No edites el repositorio de origen directamente. Los remotes esperados son:

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

No aceptes automáticamente cambios que reintroduzcan rutas del sistema original,
publicación, scraping masivo, datos inventados o mezcla de estado.
