#!/usr/bin/env python3
"""
swipe.py - ordena reels recopilados por cuánto superan a su propia cuenta,
nombra la fórmula de gancho y escribe el archivo de referencias.

La corrección central es sencilla: las visitas brutas no son evidencia. Una
cuenta con dos millones de seguidores y 400.000 visitas puede haber tenido un
día normal; una cuenta con 4.000 y 400.000 ha encontrado algo. Se ordena por
múltiplo respecto a la referencia de la propia cuenta.

La entrada es un archivo separado por tabuladores con una fila de cabecera:

    cuenta    seguidores  mediana  visitas  gancho
    @alguien  48000       11000    412000   nadie te cuenta que tus primeros 30 fallan

mediana es la mediana habitual reciente y la mejor referencia. gancho es la primera
línea hablada o en pantalla, con las palabras de la cuenta.

Uso
  python3 swipe.py captured.tsv
  python3 swipe.py captured.tsv --out <swipe.md del perfil>
  python3 swipe.py captured.tsv --json
"""

import argparse
import json
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HOOKS = os.path.join(HERE, "..", "ig-reel", "hooks.json")
WORD_RE = re.compile(r"[\w0-9$%'’-]+", re.UNICODE)

try:                                              # opcional: puntuar también los ganchos
    sys.path.insert(0, os.path.join(HERE, "..", "ig-reel"))
    from hookscore import run as score_hook       # noqa: E402
except Exception:                                 # ig-viral puede copiarse de forma independiente
    score_hook = None


def load_formulas(path):
    try:
        with open(path, encoding="utf-8") as handle:
            d = json.load(handle)
    except Exception:
        return None
    by_id = {h["id"]: h for h in d["hooks"]}
    order = d.get("classify_order") or sorted(by_id)
    return [(by_id[i]["id"], by_id[i]["name"],
             re.compile(by_id[i]["match"], re.IGNORECASE)) for i in order if i in by_id]


def classify(hook, formulas):
    if not formulas:
        return None, "unclassified"
    for fid, name, pattern in formulas:
        if pattern.search(hook):
            return fid, name
    return None, "unclassified"


def read_rows(path):
    if path == "-":
        raw = sys.stdin.read()
    else:
        with open(path, encoding="utf-8") as handle:
            raw = handle.read()
    lines = [l for l in raw.splitlines() if l.strip() and not l.lstrip().startswith("#")]
    if not lines:
        return []
    aliases = {"cuenta": "account", "seguidores": "followers", "mediana": "median", "visitas": "views", "gancho": "hook"}
    head = [aliases.get(c.strip().lower(), c.strip().lower()) for c in lines[0].split("\t")]
    if "views" in head and "hook" in head:
        cols, body = head, lines[1:]
    else:
        cols, body = ["account", "followers", "views", "hook"], lines
    rows = []
    for line in body:
        cells = line.split("\t")
        if len(cells) < len(cols):
            cells += [""] * (len(cols) - len(cells))
        r = dict(zip(cols, [c.strip() for c in cells]))
        try:
            r["views"] = int(re.sub(r"[^\d]", "", r.get("views", "")) or 0)
        except ValueError:
            continue
        for k in ("followers", "median"):
            digits = re.sub(r"[^\d]", "", r.get(k, "") or "")
            r[k] = int(digits) if digits else None
        if r["views"] and r.get("hook"):
            rows.append(r)
    return rows


def analyse(rows, formulas):
    used_median = any(r.get("median") for r in rows)
    for r in rows:
        base = r.get("median") or r.get("followers") or 0
        r["baseline"] = base
        r["outlier"] = round(r["views"] / base, 2) if base else None
        r["formula_id"], r["formula"] = classify(r["hook"], formulas)
        r["words"] = len(WORD_RE.findall(r["hook"]))
        if score_hook:
            _, overall, verdict, _ = score_hook(r["hook"])
            r["hook_score"], r["hook_verdict"] = round(overall, 1), verdict
        else:
            r["hook_score"], r["hook_verdict"] = None, None
    ranked = sorted(rows, key=lambda r: -(r["outlier"] or 0))
    third = max(1, len(ranked) // 3)
    top, bottom = ranked[:third], ranked[-third:]

    def med(items, key):
        vals = [i[key] for i in items if i.get(key) is not None]
        return round(statistics.median(vals), 1) if vals else None

    counts = {}
    for r in top:
        counts[r["formula"]] = counts.get(r["formula"], 0) + 1
    return {
        "baseline": "account median" if used_median else "follower count",
        "n": len(ranked),
        "accounts": len({r.get("account", "") for r in ranked}),
        "reels": ranked,
        "top_formulas": sorted(counts.items(), key=lambda kv: -kv[1]),
        "top_hook_score": med(top, "hook_score"),
        "bottom_hook_score": med(bottom, "hook_score"),
        "top_words": med(top, "words"),
        "bottom_words": med(bottom, "words"),
        "unclassified": sum(1 for r in ranked if r["formula"] == "unclassified"),
    }


def render(a, out=sys.stdout):
    baseline_label = "mediana de la cuenta" if a["baseline"] == "account median" else "número de seguidores"
    head = (f"ARCHIVO DE REFERENCIAS  ·  {a['n']} reels  ·  {a['accounts']} cuentas  ·  "
            f"referencia: {baseline_label}")
    print("\n" + head, file=out)
    print("=" * max(len(head), 78), file=out)
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "   ?"
        score = f"{r['hook_score']:.0f}" if r["hook_score"] is not None else " -"
        fid = f"#{r['formula_id']:<2}" if r["formula_id"] else "-  "
        formula = "sin clasificar" if r["formula"] == "unclassified" else r["formula"]
        print(f"  {mult:>7}  gancho {score:>3}  {fid} {formula[:22]:<22} "
              f"{r.get('account', '')[:16]:<16} {r['views']:>9,}", file=out)
        print(f"           \"{r['hook'][:96]}\"", file=out)
    print("-" * max(len(head), 78), file=out)
    print("QUÉ FUNCIONA EN ESTE LOTE", file=out)
    if a["top_formulas"]:
        print("  tercio superior por outlier:  "
              + ", ".join(f"{n} x{c}" for n, c in a["top_formulas"][:4]), file=out)
    if a["top_hook_score"] is not None:
        print(f"  mediana del gancho:      arriba {a['top_hook_score']:.0f}  "
              f"frente a abajo {a['bottom_hook_score']:.0f}", file=out)
    print(f"  longitud mediana:        arriba {a['top_words']} palabras  "
          f"frente a abajo {a['bottom_words']} palabras", file=out)
    print(f"  sin clasificar:           {a['unclassified']} de {a['n']}. Léelas a mano: "
          "ahí puede estar escondida una fórmula que aún no tienes.", file=out)
    print("\n  Un lote recogido a mano es evidencia, no una prueba. Doce reels no muestran "
          "nada;\n  cuarenta en seis cuentas sí muestran algo. Recoge más antes de "
          "darla por cierta.\n", file=out)


def to_markdown(a):
    baseline_label = "la mediana de la cuenta" if a["baseline"] == "account median" else "el número de seguidores"
    lines = ["# Archivo de referencias", "",
             f"{a['n']} reels de {a['accounts']} cuentas. "
             f"Ordenado por múltiplo sobre {baseline_label}.", ""]
    for r in a["reels"]:
        mult = f"{r['outlier']:.1f}x" if r["outlier"] else "?"
        formula = "sin clasificar" if r["formula"] == "unclassified" else r["formula"]
        lines += [f"## {mult}  {formula}  ({r.get('account', '')})",
                  f"- visitas: {r['views']:,}  referencia: {r['baseline']:,}",
                  f"- puntuación del gancho: {r['hook_score']}  palabras: {r['words']}",
                  f"- gancho: \"{r['hook']}\"", ""]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Ordenar reels recopilados por múltiplo de outlier.")
    ap.add_argument("input", nargs="?", default="-", help="archivo TSV, o - para leer de stdin")
    ap.add_argument("--hooks", default=HOOKS, help="ruta a ig-reel/hooks.json")
    ap.add_argument("--out", help="escribir también aquí el archivo de referencias en Markdown")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    rows = read_rows(args.input)
    if not rows:
        print("no hay filas utilizables. Hace falta un TSV con al menos visitas y gancho.",
              file=sys.stderr)
        sys.exit(2)
    formulas = load_formulas(args.hooks)
    a = analyse(rows, formulas)
    if not formulas:
        print("aviso: no se encontró hooks.json; las fórmulas no tendrán nombre. Usa --hooks.", file=sys.stderr)
    if score_hook is None:
        print("aviso: no se puede importar hookscore.py; se omiten las puntuaciones.", file=sys.stderr)

    if args.json:
        print(json.dumps(a, indent=2, ensure_ascii=False))
    else:
        render(a)
    if args.out:
        path = os.path.expanduser(args.out)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as handle:
            handle.write(to_markdown(a))
        print(f"escrito en {path}", file=sys.stderr)


if __name__ == "__main__":
    main()
