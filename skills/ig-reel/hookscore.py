#!/usr/bin/env python3
"""
hookscore.py - puntúa la primera línea de un reel con cinco propiedades de los
buenos ganchos y ordena varias opciones.

Son heurísticas locales: miden una duración que se pueda decir en menos de tres
segundos, una señal concreta, algo en juego, el contenido importante al principio
y una persona a la que dirigirse.

No predice visitas. Detecta saludos, introducciones, ganchos sin nada
comprobable y ganchos demasiado largos. No puede decir cuál de dos buenos ganchos
viajará más: eso depende de la cara, el montaje, el audio y la audiencia.

Cada comprobación devuelve de 0 a 100; cuanto más alto, mejor.

Uso
  python3 hookscore.py hooks.txt              # un gancho por línea, ordenado
  python3 hookscore.py --hook "Perdí 18.000 € por una cláusula que faltaba."
  pbpaste | python3 hookscore.py -
  python3 hookscore.py hooks.txt --json
"""

import argparse
import json
import re
import statistics
import sys

WORD_RE = re.compile(r"[\w$%'’-]+", re.UNICODE)
NUMBER_RE = re.compile(
    r"\$\s?\d[\d,]*(?:\.\d+)?"                       # money, whole
    r"|\b\d[\d,]*(?:\.\d+)?\s?"                      # a figure, with or
    r"(?:%|k\b|x\b|hrs?\b|hours?\b|horas?\b|mins?\b|minutes?\b|minutos?\b"
    r"|secs?\b|seconds?\b|segundos?\b|days?\b|días?\b|weeks?\b|semanas?\b"
    r"|months?\b|meses?\b|years?\b|años?\b|€|euros?\b)?",
    re.IGNORECASE)
PROPER_RE = re.compile(r"(?<!^)\b[A-ZÁÉÍÓÚÜÑ][a-záéíóúüñ]{2,}\b")
HASHTAG_RE = re.compile(r"(?:^|\s)#\w+")
EMOJI_RE = re.compile(r"[\U0001F300-\U0001FAFF☀-➿]")

# Los ganchos hablados dicen las cifras en voz alta. «Cero euros» y «veinte mil»
# son tan concretos como «0 €» y «20.000 €»; contar solo dígitos los perdería.
# «one» y «first» se omiten deliberadamente: suelen ser relleno, no cantidades.
SPOKEN_NUMBERS = {
    "zero", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    "ten", "eleven", "twelve", "fifteen", "twenty", "thirty", "forty", "fifty",
    "sixty", "seventy", "eighty", "ninety", "hundred", "thousand", "million",
    "billion", "dozen", "half", "twice", "triple",
    "cero", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
    "diez", "once", "doce", "quince", "veinte", "treinta", "cuarenta", "cincuenta",
    "sesenta", "setenta", "ochenta", "noventa", "cien", "ciento", "mil", "millón",
    "millones", "media", "doble", "triple",
}
MONEY_WORDS = {
    "dollars", "dollar", "bucks", "grand", "percent", "cents",
    "millionaire", "billionaire", "revenue", "profit", "salary", "rent",
    "euro", "euros", "precio", "ingresos", "beneficio", "sueldo", "alquiler",
}

# Palabras que ponen algo en juego. Un gancho sin ninguna es una afirmación;
# uno que contiene una da un motivo para seguir mirando.
STAKES = {
    "stop", "never", "wrong", "mistake", "mistakes", "lost", "lose", "losing",
    "cost", "costs", "broke", "broken", "failed", "failure", "fail", "nobody",
    "no", "not", "don't", "dont", "doesn't", "didn't", "can't", "won't",
    "quit", "quitting", "fired", "deleted", "delete", "killed", "kills", "kill",
    "replaced", "replaces", "cut", "beat", "free", "paid", "charged", "hired",
    "saved", "first",
    "banned", "illegal", "worst", "hate", "hated", "wasted", "waste", "scam",
    "lie", "lied", "lying", "truth", "secret", "hidden", "stole", "stolen",
    "before", "until", "instead", "but", "except", "unless", "problem",
    "risk", "danger", "warning", "regret", "wish", "should", "shouldn't",
    "still", "already", "only", "without", "versus", "vs", "actually",
    "deja", "dejar", "nunca", "error", "errores", "perdí", "perder", "perdido",
    "cuesta", "costó", "coste", "roto", "falló", "fracaso", "fallar", "nadie",
    "tampoco", "odio", "odié", "desperdicié", "desperdicio", "secreto", "oculto",
    "robó", "robado", "antes", "hasta", "problema", "riesgo", "peligro", "aviso",
    "arrepiento", "deberías", "solo", "realmente",
}

# Aperturas que gastan el primer segundo sin decir nada.
WEAK_OPENERS = [
    "so", "ok", "okay", "hey", "hi", "hello", "guys", "yo", "alright",
    "welcome", "today", "basically", "honestly", "look", "listen", "um",
    "just", "let", "lets", "let's", "i wanted", "i want", "one of",
    "have you", "did you", "do you", "are you", "in this", "in today",
    "the thing", "a lot", "there is", "there are", "this is", "it is",
    "as a", "when it", "if you've", "you know", "hola", "buenas", "hoy",
    "básicamente", "la cosa", "hay", "esto es", "en este", "si quieres", "ya sabes",
]

# Imperativos que merecen ocupar la primera posición.
IMPERATIVES = {
    "stop", "steal", "copy", "delete", "try", "watch", "read", "save",
    "use", "build", "make", "write", "send", "take", "start", "quit",
    "never", "always", "don't", "dont", "do", "put", "run", "check",
    "deja", "copia", "borra", "prueba", "mira", "lee", "guarda", "usa", "construye",
    "escribe", "envía", "empieza", "para", "haz", "pon", "comprueba", "no",
}

BLOQUEOS = [
    (re.compile(r"(?i)^\s*(?:deja de deslizar|no sigas deslizando)"),
     "Apertura «deja de deslizar». El gancho debe ganarse la atención con una afirmación."),
    (re.compile(r"(?i)\b(?:en este|en el) (?:vídeo|reel)|te voy a enseñar|voy a mostrarte\b"),
     "Introducción de vídeo. Elimínala y empieza por el resultado."),
    (re.compile(r"(?i)^\s*(?:hola|buenas|qué tal)[,!]?\s"),
     "Saludo. Empieza por lo que la persona ha venido a descubrir."),
    (re.compile(r"(?i)^\s*(?:stop scrolling|don'?t scroll)"),
     "Empieza por «deja de deslizar». Pedir atención demuestra que aún no la has ganado."),
    (re.compile(r"(?i)\b(?:in (?:this|today'?s) (?:video|reel)|i'?m going to show you|i'?ll show you how)\b"),
     "Introducción de vídeo. Elimínala y empieza por el resultado."),
    (re.compile(r"(?i)^\s*(?:hey |hi |what'?s up |welcome )"),
     "Saludo. Nadie entra al feed para recibir un saludo."),
    (HASHTAG_RE,
     "Hashtag en el gancho. Si se usan, los hashtags van al final del caption."),
    (EMOJI_RE,
     "Emoji en el gancho. El texto grande tiene sitio para palabras o para un emoji, no para ambos."),
]


def clamp(n):
    return max(0.0, min(100.0, n))


def words(text):
    # «18.000 €» es una palabra cuando se pronuncia, así que aquí también cuenta como una.
    return WORD_RE.findall(re.sub(r"(?<=\d),(?=\d)", "", text))


def check_length(text):
    """El gancho debe llegar antes de que el pulgar se mueva: unos dos segundos."""
    w = words(text)
    n = len(w)
    secs = n / 2.75                      # ~165 palabras por minuto al hablar
    chars = len(text.strip())
    if 5 <= n <= 12:
        score = 100.0
    elif n < 5:
        score = clamp(100 - (5 - n) * 20)
    else:
        score = clamp(100 - (n - 12) * 11)
    if chars > 60:                       # two lines of big on-screen text
        score -= 12
    return clamp(score), f"{n} palabras, {chars} caracteres, ~{secs:.1f} s habladas (objetivo: 5-12 palabras)"


def check_specificity(text):
    """Una cosa concreta supera a tres abstractas."""
    nums = [n.strip() for n in NUMBER_RE.findall(text) if n.strip()]
    propers = set(PROPER_RE.findall(text))
    low = [w.lower().strip("'’") for w in words(text)]
    spoken = [w for w in low if w in SPOKEN_NUMBERS or w in MONEY_WORDS]
    hits = len(nums) + len(propers) + len(spoken)
    score = 15.0 if hits == 0 else clamp(45 + hits * 30)
    found = ", ".join(nums[:2] + sorted(propers)[:2] + spoken[:2])
    return score, (f"{hits} marcador(es) concreto(s)" + (f": {found}" if found else
                   " - sin cifra, nombre ni nada comprobable"))


def check_stakes(text):
    """Tensión, coste o negación: algo que la persona pueda perder."""
    w = [x.lower().strip("'’") for x in words(text)]
    hits = [x for x in w if x in STAKES]
    markers = sorted(set(hits))
    if re.search(r"\$\s?\d", text):
        markers.append("un precio")
    n = len(markers)
    score = {0: 20.0, 1: 70.0}.get(n, 100.0)
    detail = f"{n} marcador(es) de tensión" + (f": {', '.join(markers[:4])}" if markers else
                                         " - en esta línea no hay nada en juego")
    return clamp(score), detail


def check_frontload(text):
    """La palabra interesante no puede aparecer en la posición nueve."""
    w = words(text)
    if not w:
        return 0.0, "vacío"
    low = [x.lower().strip("'’") for x in w]
    opener = " ".join(low[:2])
    penalty = 0
    hit_opener = None
    for weak in WEAK_OPENERS:
        if opener.startswith(weak) or low[0] == weak:
            penalty, hit_opener = 30, weak
            break
    payload = None
    for i, token in enumerate(low):
        if (token in STAKES or token in SPOKEN_NUMBERS or token in MONEY_WORDS
                or NUMBER_RE.match(w[i]) or (i and PROPER_RE.match(w[i]))):
            payload = i
            break
    if payload is None:
        base = 30.0
        where = "no hay palabra de contenido en la línea"
    elif payload <= 3:
        base = 100.0
        where = f"contenido en la palabra {payload + 1}"
    elif payload <= 6:
        base = 70.0
        where = f"contenido en la palabra {payload + 1}; podría adelantarse"
    else:
        base = 40.0
        where = f"contenido en la palabra {payload + 1}; demasiado tarde"
    detail = where + (f"; apertura débil \"{hit_opener}\"" if hit_opener else "")
    return clamp(base - penalty), detail


def check_address(text):
    """Debe dirigirse a alguien concreto, no quedar flotando."""
    low = text.lower()
    w = [x.lower().strip("'’") for x in words(text)]
    if re.search(r"\b(you|your|you're|youre|yourself|tú|tu|te|ti|vosotros|vosotras)\b", low):
        return 100.0, "habla a quien mira"
    if w and w[0] in IMPERATIVES:
        return 90.0, f"apertura imperativa (\"{w[0]}\")"
    if re.search(r"\b(i|my|me|we|our|yo|mi|me|nos|nuestro|nuestra)\b", low):
        return 70.0, "primera persona, sin nombrar a quien mira"
    return 35.0, "tercera persona, sin nadie concreto en la escena"


CHECKS = ["LENGTH", "SPECIFICITY", "STAKES", "FRONTLOAD", "ADDRESS"]


def run(text):
    results = {
        "LENGTH": check_length(text),
        "SPECIFICITY": check_specificity(text),
        "STAKES": check_stakes(text),
        "FRONTLOAD": check_frontload(text),
        "ADDRESS": check_address(text),
    }
    flags = [msg for pattern, msg in BLOQUEOS if pattern.search(text)]
    scores = [results[c][0] for c in CHECKS]
    # La propiedad más débil limita el gancho, igual que en detect.py: basta una
    # propiedad mala para que el pulgar siga deslizando.
    overall = statistics.mean(scores) * 0.6 + min(scores) * 0.4 - len(flags) * 15
    overall = clamp(overall)
    verdict = "STRONG" if overall >= 70 and min(scores) >= 55 and not flags else (
        "OK" if overall >= 50 else "WEAK")
    return results, overall, verdict, flags


def bar(score, width=24):
    filled = round(score / 100 * width)
    return "#" * filled + "." * (width - filled)


def render_one(text, results, overall, verdict, flags, out=sys.stdout):
    display_names = {"LENGTH": "DURACIÓN", "SPECIFICITY": "CONCRECIÓN", "STAKES": "EN JUEGO", "FRONTLOAD": "AL PRINCIPIO", "ADDRESS": "DESTINATARIO"}
    display_verdicts = {"STRONG": "FUERTE", "OK": "ACEPTABLE", "WEAK": "DÉBIL"}
    print("\nPUNTUACIÓN DEL GANCHO", file=out)
    print("=" * 62, file=out)
    print(f"  \"{text.strip()}\"\n", file=out)
    for name in CHECKS:
        score, detail = results[name]
        print(f"  {display_names.get(name, name):<13} {bar(score)} {score:5.1f}", file=out)
        print(f"  {'':<13} {detail}", file=out)
    print("-" * 62, file=out)
    print(f"  {'PUNTUACIÓN DEL GANCHO':<13} {bar(overall)} {overall:5.1f}   {display_verdicts.get(verdict, verdict)}", file=out)
    for f in flags:
        print(f"\n  BLOQUEO  {f}", file=out)
    if verdict != "STRONG":
        weakest = min(CHECKS, key=lambda c: results[c][0])
        print(f"\n  Propiedad más débil: {display_names.get(weakest, weakest)}. Corrige esa y repite.", file=out)
    print("", file=out)


def render_table(rows, out=sys.stdout):
    display_verdicts = {"STRONG": "FUERTE", "OK": "ACEPTABLE", "WEAK": "DÉBIL"}
    display_names = {"LENGTH": "DURACIÓN", "SPECIFICITY": "CONCRECIÓN", "STAKES": "EN JUEGO", "FRONTLOAD": "AL PRINCIPIO", "ADDRESS": "DESTINATARIO"}
    print("\nCLASIFICACIÓN DE GANCHOS\n" + "=" * 78, file=out)
    for i, r in enumerate(rows, 1):
        mark = "->" if i == 1 else "  "
        hook = r["hook"] if len(r["hook"]) <= 62 else r["hook"][:59] + "..."
        verdict = display_verdicts.get(r["verdict"], r["verdict"])
        print(f"{mark} {r['score']:5.1f} {verdict:<9} {hook}", file=out)
        print(f"        propiedad más débil: {display_names.get(r['weakest'], r['weakest'])} ({r['checks'][r['weakest']]['score']:.0f})", file=out)
        for f in r["flags"]:
            print(f"        bloqueo: {f}", file=out)
    print("\nGraba la primera. Si queda por debajo de 50, ninguna es todavía el gancho.\n",
          file=out)


def main():
    ap = argparse.ArgumentParser(description="Puntuar un gancho de reel con cinco propiedades.")
    ap.add_argument("input", nargs="?", default="-", help="archivo con un gancho por línea, o -")
    ap.add_argument("--hook", help="puntuar un único gancho escrito en la línea de comandos")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    if args.hook:
        lines = [args.hook]
    else:
        raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
    if not lines:
        print("no hay nada que puntuar", file=sys.stderr)
        sys.exit(2)

    payload = []
    for line in lines:
        results, overall, verdict, flags = run(line)
        payload.append({
            "hook": line,
            "checks": {k: {"score": round(v[0], 1), "detail": v[1]} for k, v in results.items()},
            "weakest": min(CHECKS, key=lambda c: results[c][0]),
            "flags": flags,
            "score": round(overall, 1),
            "verdict": verdict,
        })

    if args.json:
        print(json.dumps(payload if len(payload) > 1 else payload[0], indent=2, ensure_ascii=False))
        return

    if len(payload) == 1:
        results, overall, verdict, flags = run(lines[0])
        render_one(lines[0], results, overall, verdict, flags)
    else:
        render_table(sorted(payload, key=lambda r: -r["score"]))

    sys.exit(0 if max(p["score"] for p in payload) >= 70 else 1)


if __name__ == "__main__":
    main()
