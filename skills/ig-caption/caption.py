#!/usr/bin/env python3
"""
caption.py - revisa un caption de Instagram y muestra exactamente qué se ve
antes de «... más».

Instagram enseña una ventana corta del caption y oculta el resto tras un toque.
Aquí suelen fallar los captions: el gancho aparece en la tercera frase, la
primera línea es un saludo o todo empieza con un hashtag. Esta herramienta
muestra la ventana visible y revisa ocho aspectos útiles.

El corte es una aproximación: cambia con el dispositivo, la fuente y los saltos
de línea. Usa --truncate para probar otra ventana.

Uso
  python3 caption.py caption.txt
  python3 caption.py caption.txt --keywords "software para propuestas,contrato de cliente"
  pbpaste | python3 caption.py -
  python3 caption.py caption.txt --json
"""

import argparse
import json
import re
import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
from shared.platform_rules import load_rules, rule_value, rule_verified

DEFAULT_RULES = load_rules()
LIMIT = int(rule_value(DEFAULT_RULES, "caption.max_characters", 2200))
TRUNCATE = int(rule_value(DEFAULT_RULES, "caption.feed_preview_characters", 125))
HASHTAG_LIMIT = int(rule_value(DEFAULT_RULES, "caption.hashtag_max_per_post", 5))

HASHTAG_RE = re.compile(r"(?:^|\s)(#[A-Za-z0-9_]+)")
MENTION_RE = re.compile(r"(?:^|\s)(@[A-Za-z0-9_.]+)")
LINK_RE = re.compile(r"https?://\S+|\bwww\.\S+|\b[a-z0-9-]+\.(?:com|co|io|net|org|ai|app)/\S*",
                     re.IGNORECASE)
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿←-⇿️]")
CONCRETE_RE = re.compile(r"\$\s?\d|\b\d[\d,.]*\b|(?<!^)\b[A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]{2,}\b", re.MULTILINE)

ASKS = [
    (re.compile(r"(?i)\b(?:comenta|escribe) (?:la palabra )?[A-Z0-9ÁÉÍÓÚÜÑ]{2,}\b"), "comentar una palabra"),
    (re.compile(r"(?i)\b(?:mándame|mandame|envíame|enviame|escríbeme|escribeme) (?:un )?(?:mensaje|DM)\b"), "enviar un DM"),
    (re.compile(r"(?i)\bguárd(?:alo|alo)|\bguarda esto\b"), "guardar esto"),
    (re.compile(r"(?i)\bcompárte(?:lo|la)|\bcomparte esto\b"), "compartir esto"),
    (re.compile(r"(?i)\bsigue(?:me)? para\b|\bsígueme\b"), "seguir"),
    (re.compile(r"(?i)\benlace en (?:mi )?bio\b"), "enlace en bio"),
    (re.compile(r"(?i)\bdesliza|\btoca (?:para|a la)\b"), "deslizar o tocar"),
    (re.compile(r"(?i)\bdime\b|\bcuál eliges\b|\bqué harías\b"), "responder una pregunta"),
    (re.compile(r"(?i)\bcomment (?:the word |\")?[A-Z0-9]{2,}\b"), "comentar una palabra"),
    (re.compile(r"(?i)\b(?:dm|message) me\b"), "enviarme un DM"),
    (re.compile(r"(?i)\bsave (?:this|it)\b"), "guardar esto"),
    (re.compile(r"(?i)\bshare (?:this|it)\b"), "compartir esto"),
    (re.compile(r"(?i)\bfollow (?:me|for)\b"), "seguir"),
    (re.compile(r"(?i)\blink in (?:my )?bio\b"), "enlace en bio"),
    (re.compile(r"(?i)\b(?:swipe|tap) (?:through|left|right|for|to)\b"), "deslizar o tocar"),
    (re.compile(r"(?i)\btell me\b|\bwhat would you\b|\bwhich one\b"), "responder una pregunta"),
]

FILLER_TAGS = {"#viral", "#fyp", "#explore", "#explorepage", "#foryou", "#foryoupage",
               "#trending", "#instagood", "#love", "#follow", "#like4like", "#reels",
               "#parati", "#tendencia", "#amorporinstagram", "#me gusta",
               "#reelsinstagram", "#viralreels", "#instadaily"}


def visible_window(text, cut):
    """Qué muestra el feed; Instagram puede cortar una palabra a mitad."""
    flat = text.strip()
    return flat if len(flat) <= cut else flat[:cut]


def render_box(window, truncated, out=sys.stdout, width=52):
    print("\n  LO QUE MUESTRA EL FEED", file=out)
    print("  +" + "-" * (width + 2) + "+", file=out)
    lines = []
    for raw in window.split("\n"):
        lines.extend(textwrap.wrap(raw, width) or [""])
    for line in lines[:8]:
        print(f"  | {line:<{width}} |", file=out)
    tail = "... más" if truncated else "(cabe todo el caption)"
    print("  +" + "-" * (width + 2 - len(tail) - 2) + f" {tail} " + "+", file=out)


def analyse(text, cut=None, keywords=None, rules=None):
    text = text.rstrip()
    rules = rules or DEFAULT_RULES
    limit = int(rule_value(rules, "caption.max_characters", LIMIT))
    truncate_at = int(cut if cut is not None else rule_value(rules, "caption.feed_preview_characters", TRUNCATE))
    hashtag_limit = rule_value(rules, "caption.hashtag_max_per_post", HASHTAG_LIMIT)
    hashtag_limit = int(hashtag_limit) if hashtag_limit is not None else None
    limit_verified = rule_verified(rules, "caption.max_characters")
    truncate_verified = rule_verified(rules, "caption.feed_preview_characters")
    hashtag_limit_verified = rule_verified(rules, "caption.hashtag_max_per_post")
    cut = truncate_at
    stripped = text.strip()
    chars = len(stripped)
    lines = [l for l in stripped.split("\n")]
    first_line = lines[0].strip() if lines else ""
    tags = HASHTAG_RE.findall(stripped)
    mentions = MENTION_RE.findall(stripped)
    links = LINK_RE.findall(stripped)
    emoji = EMOJI_RE.findall(stripped)
    window = visible_window(stripped, cut)
    truncated = chars > cut
    asks = [name for pattern, name in ASKS if pattern.search(stripped)]
    filler = [t for t in tags if t.lower() in FILLER_TAGS]
    keywords = [k.strip() for k in (keywords or []) if k.strip()]

    checks = []

    def add(name, status, detail):
        checks.append({"check": name, "status": status, "detail": detail})

    add("LENGTH", "FAIL" if chars > limit else "WARN" if not limit_verified else "PASS",
        f"{chars} / {limit} caracteres" + (f", {chars - limit} por encima del límite configurado"
                                           if chars > limit else ""))
    if not limit_verified:
        checks[-1]["detail"] += " (regla no verificada)"

    if not first_line:
        add("FIRST LINE", "FAIL", "el caption empieza con una línea vacía")
    elif first_line.startswith("#") or first_line.startswith("@"):
        add("FIRST LINE", "FAIL",
            "empieza con un hashtag o una mención, justo donde debería ir una frase")
    elif len(first_line) > cut:
        add("FIRST LINE", "WARN",
            f"{len(first_line)} caracteres, así que se corta en {cut} a mitad de una idea. "
            "Está bien si crea curiosidad; no si deja una subordinada colgando")
    else:
        add("FIRST LINE", "PASS", f"{len(first_line)} caracteres y cabe completa")

    add("HOOK IS CONCRETE", "PASS" if CONCRETE_RE.search(window) else "WARN",
        f"{len(CONCRETE_RE.findall(window))} cifra(s) o nombre(s) en la ventana visible"
        + ("" if CONCRETE_RE.search(window) else " - no hay nada comprobable antes del toque"))

    if hashtag_limit is None:
        add("HASHTAGS", "WARN", f"{len(tags)} etiquetas; el máximo no está configurado")
    elif len(tags) > hashtag_limit:
        status = "WARN" if not hashtag_limit_verified else "FAIL"
        add("HASHTAGS", status, f"{len(tags)} etiquetas, por encima del máximo configurado de {hashtag_limit}. "
                                "verifica la regla antes de tratarlo como un fallo duro")
    elif len(tags) == hashtag_limit and filler:
        add("HASHTAGS", "WARN", f"{len(tags)} etiquetas, en el máximo configurado, y "
                                f"{len(filler)} son genéricas. Usa las etiquetas disponibles para temas concretos")
    elif filler:
        add("HASHTAGS", "WARN", f"{len(tags)} etiqueta(s), {len(filler)} genérica" + (f": {' '.join(tags)}" if tags else ""))
    else:
        add("HASHTAGS", "WARN" if not hashtag_limit_verified else "PASS", f"{len(tags)} etiqueta(s)" + (f": {' '.join(tags)}" if tags else ""))
        if not hashtag_limit_verified:
            checks[-1]["detail"] += " (regla máxima no verificada)"

    if not tags:
        add("TAG PLACEMENT", "PASS", "no hay etiquetas que colocar")
    elif any(re.search(r"(?:^|\s)" + re.escape(t) + r"\b", window) for t in tags):
        add("TAG PLACEMENT", "WARN", "hay un hashtag dentro de la ventana visible y "
                                     "ocupa espacio del feed")
    else:
        add("TAG PLACEMENT", "PASS", "las etiquetas quedan debajo del corte")

    add("LINKS", "WARN" if links else "PASS",
        f"{len(links)} enlace(s) en el caption; los captions no son clicables. "
        f"Muévelo a la bio o al DM" if links else "no hay enlaces muertos en el cuerpo")

    if len(asks) == 1:
        add("ONE ASK", "PASS", f"una llamada a la acción: {asks[0]}")
    elif not asks:
        add("ONE ASK", "WARN", "no hay llamada a la acción. Decide para qué sirve esta publicación")
    else:
        add("ONE ASK", "WARN", f"{len(asks)} acciones ({', '.join(asks)}). "
                               "Dos acciones equivalen a ninguna")

    density = len(emoji) * 100 / max(chars, 1)
    add("EMOJI", "WARN" if density > 4 else "PASS",
        f"{len(emoji)} emoji, {density:.1f} por cada 100 caracteres"
        + (" - parece decoración" if density > 4 else ""))

    if keywords:
        low = stripped.lower()
        found = [k for k in keywords if k.lower() in low]
        missing = [k for k in keywords if k.lower() not in low]
        in_window = [k for k in found if k.lower() in window.lower()]
        status = "PASS" if not missing else ("WARN" if found else "FAIL")
        add("SEARCH TERMS", status,
            f"{len(found)}/{len(keywords)} presentes"
            + (f", {len(in_window)} en la ventana visible" if found else "")
            + (f". Faltan: {', '.join(missing)}" if missing else ""))

    fails = sum(1 for c in checks if c["status"] == "FAIL")
    warns = sum(1 for c in checks if c["status"] == "WARN")
    verdict = "FIX" if fails else ("REVIEW" if warns else "READY")

    return {
        "characters": chars, "limit": limit, "truncate_at": cut,
        "rules": {
            "max_characters_verified": limit_verified,
            "feed_preview_verified": truncate_verified,
            "hashtag_limit": hashtag_limit,
            "hashtag_limit_verified": hashtag_limit_verified,
        },
        "visible": window, "truncated": truncated,
        "first_line_chars": len(first_line),
        "hashtags": tags, "mentions": mentions, "links": links,
        "emoji": len(emoji), "asks": asks,
        "checks": checks, "verdict": verdict,
    }


def render(a, out=sys.stdout):
    head = (f"REVISIÓN DEL CAPTION  ·  {a['characters']} / {a['limit']} caracteres · "
            f"{len(a['hashtags'])} etiquetas · {len(a['asks'])} acción(es)")
    print("\n" + head, file=out)
    print("=" * max(len(head), 62), file=out)
    render_box(a["visible"], a["truncated"], out=out)
    print("", file=out)
    display_checks = {"LENGTH": "LONGITUD", "FIRST LINE": "PRIMERA LÍNEA", "HOOK IS CONCRETE": "GANCHO CONCRETO", "HASHTAGS": "HASHTAGS", "TAG PLACEMENT": "UBICACIÓN DE ETIQUETAS", "LINKS": "ENLACES", "ONE ASK": "UNA ACCIÓN", "EMOJI": "EMOJI", "SEARCH TERMS": "TÉRMINOS DE BÚSQUEDA"}
    display_status = {"PASS": "OK", "WARN": "AVISO", "FAIL": "FALLO"}
    for c in a["checks"]:
        status = display_status.get(c["status"], c["status"])
        check = display_checks.get(c["check"], c["check"])
        print(f"  {status:<5} {check:<21} {c['detail']}", file=out)
    print("-" * max(len(head), 62), file=out)
    verdict_names = {"FIX": "CORREGIR", "REVIEW": "REVISAR", "READY": "LISTO"}
    print(f"  RESULTADO  {verdict_names.get(a['verdict'], a['verdict'])}\n", file=out)


def main():
    ap = argparse.ArgumentParser(description="Revisar un caption de Instagram.")
    ap.add_argument("input", nargs="?", default="-", help="archivo de caption, o - para leer de stdin")
    ap.add_argument("--truncate", type=int, default=None,
                    help="caracteres visibles antes de '... más' (por defecto, según las reglas)")
    ap.add_argument("--rules", help="superposición de platform-rules.json del perfil")
    ap.add_argument("--keywords", default="", help="términos separados por comas por los que quieres aparecer")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    rules = load_rules(args.rules) if args.rules else DEFAULT_RULES
    a = analyse(raw, cut=args.truncate, keywords=args.keywords.split(","), rules=rules)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0 if a["verdict"] == "READY" else 1)


if __name__ == "__main__":
    main()
