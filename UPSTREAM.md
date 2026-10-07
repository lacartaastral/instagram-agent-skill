# Seguimiento del repositorio de origen

## Commit base

- Repositorio de origen: https://github.com/Jakeschincariol/instagram-agent-skill
- Fork: https://github.com/lacartaastral/instagram-agent-skill
- Commit base: d03c56bb598be770c60b201f94237e5d1a4268a6
- Fecha observada del commit base: 2026-10-07
- Rama local: openclaw/multiperfil-governed

El commit base se clonó y se dejó en su referencia correspondiente antes de aplicar
cualquier cambio propio del fork. La licencia MIT y la atribución original se
mantienen intactas.

## Límites intencionados del fork

- skills/*/SKILL.md: conserva los contratos editoriales, sustituye las rutas
  específicas del sistema original por la resolución de recursos OpenClaw con
  {baseDir} y añade el límite de perfil, voz (speaker) y aprobación.
- skills/*/*.py y recursos JSON: conserva el comportamiento determinista y solo
  añade los cambios mínimos necesarios para las reglas por perfil de OpenClaw.
- shared/: contratos nuevos y deterministas para almacenamiento, reglas y
  enrutamiento de modelos.
- config/: rutas de intención, instantánea de política de modelos y reglas
  mutables de plataforma.
- skills/ig-router/: orquestador fino de OpenClaw; no redacta ni actúa.
- El manifiesto específico del sistema de origen se elimina porque este fork se
  descubre como skills nativas de OpenClaw.

## Procedimiento seguro de actualización

1. Descarga el repositorio de origen sin cambiar el árbol de trabajo actual.
2. Inspecciona el diff contra este baseline, especialmente las rutas de skills,
   las cifras de plataforma y cualquier verbo que implique una acción.
3. Haz el merge con --no-commit en la rama gobernada.
4. Reaplica o actualiza los tests y los metadatos de reglas si el origen cambió
   el comportamiento.
5. Ejecuta la suite determinista completa, compileall, git diff --check y la
   validación de discovery de OpenClaw.
6. Confirma el merge como un cambio revisable. Nunca sobrescribas la
   configuración ni el estado del fork y nunca aceptes cambios que añadan
   publicación, scraping amplio o lecturas entre perfiles.
