#!/usr/bin/env python3
"""
beats.py - convierte un guion de reel en una escaleta temporal antes de grabarlo.

Estima cuánto tarda cada línea, las coloca en códigos de tiempo y marca cuatro
problemas habituales: gancho después de tres segundos, beat demasiado largo,
varias líneas sin nada concreto y duración distinta de la prevista.

Es una estimación basada en palabras por minuto, útil para planificar el montaje
pero no sustituta de grabar. Ajusta --wpm después de cronometrarte leyendo en
voz alta; el valor por defecto es 165.

Uso
  python3 beats.py guion.txt
  python3 beats.py guion.txt --objetivo 30
  python3 beats.py guion.txt --wpm 185 --target 45
  pbpaste | python3 beats.py -
  python3 beats.py guion.txt --json
"""

import argparse
import json
import re
import sys

WORD_RE = re.compile(r"[\w0-9$%'’-]+", re.UNICODE)
SENT_RE = re.compile(r"[^.!?]+[.!?]*")
CONCRETE_RE = re.compile(r"\$\s?\d|\b\d[\d,.]*\b|(?<!^)\b[A-Z][a-z]{2,}\b", re.MULTILINE)
STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "if", "of", "to", "in", "on", "for",
    "with", "that", "this", "it", "is", "are", "was", "were", "be", "been",
    "you", "your", "i", "my", "me", "we", "our", "they", "them", "he", "she",
    "so", "just", "not", "no", "do", "did", "does", "have", "has", "had",
    "will", "can", "at", "as", "by", "from", "out", "up", "off", "one", "all",
    "el", "la", "los", "las", "un", "una", "y", "o", "pero", "si", "de", "a", "en",
    "para", "con", "que", "esto", "eso", "es", "son", "era", "eran", "ser", "ha",
    "has", "han", "yo", "mi", "me", "nos", "tú", "tu", "te", "ellos", "ellas",
}

HOOK_WINDOW = 3.0        # segundos. Después, el pulgar ya ha decidido.
MAX_BEAT = 4.0           # segundos sobre una idea sin cambio en pantalla.
ABSTRACT_RUN = 3         # beats seguidos sin nada comprobable.


def words(text):
    # «18.000 €» es una palabra cuando se pronuncia, así que aquí también cuenta como una.
    return WORD_RE.findall(re.sub(r"(?<=\d),(?=\d)", "", text))


def pretty(token):
    """Devuelve el separador de miles para mostrarlo."""
    return re.sub(r"(\d)(?=(\d{3})+$)", r"\1,", token)


def tc(seconds):
    m, s = divmod(seconds, 60)
    return f"{int(m)}:{s:04.1f}"


def split_beats(raw, wps):
    """Cada línea es un beat, salvo que sea demasiado larga."""
    beats = []
    for line in [l.strip() for l in raw.splitlines()]:
        if not line:
            continue
        if len(words(line)) / wps <= MAX_BEAT * 1.5:
            beats.append(line)
            continue
        # Párrafo largo: divídelo cuando termine una frase para que los tiempos
        # tengan sentido y el informe pueda indicar que se ha dividido.
        parts = [p.strip() for p in SENT_RE.findall(line) if p.strip()]
        buf = ""
        for part in parts:
            candidate = (buf + " " + part).strip()
            if buf and len(words(candidate)) / wps > MAX_BEAT:
                beats.append(buf)
                buf = part
            else:
                buf = candidate
        if buf:
            beats.append(buf)
    return beats


def analyse(raw, wpm=165, target=None):
    wps = wpm / 60.0
    beats = split_beats(raw, wps)
    if not beats:
        return None

    rows, clock = [], 0.0
    for i, text in enumerate(beats):
        n = len(words(text))
        dur = n / wps
        rows.append({
            "n": i + 1,
            "start": round(clock, 2),
            "dur": round(dur, 2),
            "words": n,
            "text": text,
            "concrete": len(CONCRETE_RE.findall(text)),
            "label": "",
            "flags": [],
        })
        clock += dur
    total = clock

    # Etiqueta las posiciones estructurales sobre las que se construye un reel.
    for r in rows:
        if r["n"] == 1 or r["start"] + r["dur"] <= HOOK_WINDOW:
            r["label"] = "HOOK"
    rows[-1]["label"] = "CTA" if rows[-1]["label"] != "HOOK" else "HOOK/CTA"
    half = total / 2
    for r in rows:
        if not r["label"] and r["start"] <= half < r["start"] + r["dur"]:
            r["label"] = "MID"

    notes = []
    if rows[0]["dur"] > HOOK_WINDOW:
        rows[0]["flags"].append(f"el gancho dura {rows[0]['dur']:.1f} s; supera la marca de {HOOK_WINDOW:.0f} s")
        notes.append(f"El beat 1 tarda {rows[0]['dur']:.1f}s en decirse. Redúcelo a "
                     f"{int(HOOK_WINDOW * wps)} palabras o menos; si no, el gancho llega después de que "
                     "se haya tomado la decisión.")
    if rows[0]["concrete"] == 0:
        notes.append("El beat 1 no contiene cifra ni nombre. Los ganchos sin algo "
                     "comprobable son los que se pasan de largo.")

    for r in rows:
        if r["dur"] > MAX_BEAT:
            r["flags"].append(f"{r['dur']:.1f} s en un beat")
    long_beats = [r["n"] for r in rows if r["dur"] > MAX_BEAT]
    if long_beats:
        notes.append(f"Los beats {', '.join(map(str, long_beats))} superan {MAX_BEAT:.0f}s. "
                     "Divide la línea o cambia lo que aparece en pantalla. "
                     "La gente se va cuando el plano permanece estático.")

    run, start = 0, None
    for r in rows:
        if r["concrete"] == 0:
            run += 1
            start = start if start is not None else r["n"]
            if run == ABSTRACT_RUN:
                notes.append(f"Los beats {start}-{r['n']} no contienen nada concreto. "
                             "Añade una cifra, un nombre o un precio en uno.")
        else:
            run, start = 0, None

    # ¿La última línea devuelve a la primera?
    first = {w.lower() for w in words(rows[0]["text"]) if w.lower() not in STOPWORDS}
    last = {w.lower() for w in words(rows[-1]["text"]) if w.lower() not in STOPWORDS}
    loop = sorted(pretty(w) for w in first & last)
    if loop:
        notes.append(f"Bucle: el último beat repite \"{', '.join(loop[:3])}\" del gancho. "
                     "Las repeticiones aportan alcance sin coste.")
    else:
        notes.append("No hay bucle. El último beat no comparte ninguna palabra con el gancho y el vídeo "
                     "termina plano. Repetir una palabra del beat 1 es la forma más barata de provocar una repetición.")

    if target:
        delta = total - target
        if abs(delta) <= target * 0.1:
            notes.append(f"La duración está en objetivo ({total:.1f} s frente a {target} s).")
        elif delta > 0:
            notes.append(f"{delta:.1f} s por encima del objetivo. Corta unas {int(delta * wps)} palabras.")
        else:
            notes.append(f"{-delta:.1f} s por debajo del objetivo. Añade unas {int(-delta * wps)} palabras "
                         "o grábalo corto. Lo corto suele ser lo adecuado.")

    return {
        "wpm": wpm, "target": target,
        "total_seconds": round(total, 2),
        "total_words": sum(r["words"] for r in rows),
        "beats": rows,
        "notes": notes,
    }


def render(a, out=sys.stdout):
    head = (f"ESCALETA DEL REEL  ·  {a['total_words']} palabras  ·  ~{a['total_seconds']:.1f} s "
            f"a {a['wpm']} palabras/min" + (f"  ·  objetivo {a['target']} s" if a["target"] else ""))
    print("\n" + head, file=out)
    print("=" * max(len(head), 72), file=out)
    display_labels = {"HOOK": "GANCHO", "MID": "CENTRO", "CTA": "CTA", "HOOK/CTA": "GANCHO/CTA"}
    for r in a["beats"]:
        label_name = display_labels.get(r["label"], r["label"])
        label = f"{label_name:<8}" if label_name else " " * 8
        print(f"  {tc(r['start'])}  {r['dur']:4.1f}s  {label}{r['text']}", file=out)
        for f in r["flags"]:
            print(f"  {'':>6}  {'':>5}  {'':<8}^ {f}", file=out)
    print("-" * max(len(head), 72), file=out)
    for n in a["notes"]:
        print(f"  - {n}", file=out)
    print("", file=out)


def main():
    ap = argparse.ArgumentParser(description="Convertir un guion de reel en una escaleta temporal.")
    ap.add_argument("input", nargs="?", default="-", help="archivo de guion, o - para leer de stdin")
    ap.add_argument("--wpm", type=float, default=165, help="velocidad al hablar (por defecto, 165)")
    ap.add_argument("--target", type=float, help="duración objetivo en segundos")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    raw = sys.stdin.read() if args.input == "-" else open(args.input, encoding="utf-8").read()
    a = analyse(raw, wpm=args.wpm, target=args.target)
    if not a:
        print("guion vacío", file=sys.stderr)
        sys.exit(2)
    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    sys.exit(0)


if __name__ == "__main__":
    main()
