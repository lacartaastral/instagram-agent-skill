"""Política determinista de enrutamiento de modelos para Instagram.

Este módulo nunca cambia la configuración de OpenClaw ni llama a un modelo. El
caller proporciona la allowlist observada en tiempo de ejecución. Las rutas de
calidad y profundas fallan cerrado cuando el modelo configurado explícitamente
no está disponible.
"""
from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Iterable

TIER_NAMES = {0: "DETERMINISTIC", 1: "ROUTINE", 2: "QUALITY", 3: "DEEP"}
NAME_TO_TIER = {name.lower(): number for number, name in TIER_NAMES.items()}


@dataclass(frozen=True)
class RouteDecision:
    tier: int
    label: str
    deterministic: bool
    model: str | None
    requires_subagent: bool
    status: str
    reason: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def _allowed(values: Iterable[str]) -> set[str]:
    return {str(value).strip() for value in values if str(value).strip()}


def normalize_tier(tier: int | str) -> int:
    if isinstance(tier, str):
        value = tier.strip().lower()
        if value in NAME_TO_TIER:
            return NAME_TO_TIER[value]
        tier = int(value)
    tier = int(tier)
    if tier not in TIER_NAMES:
        raise ValueError(f"tier de modelo no admitido: {tier}")
    return tier


def decide(
    tier: int | str,
    *,
    allowed_models: Iterable[str],
    default_model: str | None,
    quality_model: str | None = None,
    deep_model: str | None = None,
) -> RouteDecision:
    """Resuelve una ruta contra la allowlist proporcionada por el runtime."""
    number = normalize_tier(tier)
    label = TIER_NAMES[number]
    allowed = _allowed(allowed_models)
    if number == 0:
        return RouteDecision(number, label, True, None, False, "ready",
                             "trabajo local determinista; no se llama a ningún modelo")

    candidate = {1: default_model, 2: quality_model, 3: deep_model}[number]
    if not candidate:
        return RouteDecision(number, label, False, None, True, "blocked",
                             f"no hay un modelo explícito configurado para {label.lower()}")
    if candidate not in allowed:
        return RouteDecision(number, label, False, candidate, True, "blocked",
                             f"el modelo {candidate!r} no está en la allowlist del runtime")
    if number == 1:
        return RouteDecision(number, label, False, candidate, False, "ready",
                             "usar el modelo autorizado por defecto para trabajo editorial rutinario")
    return RouteDecision(number, label, False, candidate, True, "ready",
                         "delegar explícitamente mediante el routing nativo de subagentes de OpenClaw")


def load_policy(path: str | Path) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def decide_from_policy(policy: dict[str, Any], tier: int | str,
                        runtime_allowlist: Iterable[str] | None = None) -> RouteDecision:
    runtime = policy.get("runtime", {})
    allowed = runtime_allowlist if runtime_allowlist is not None else runtime.get("allowlist", [])
    return decide(
        tier,
        allowed_models=allowed,
        default_model=runtime.get("default_model"),
        quality_model=runtime.get("quality_model"),
        deep_model=runtime.get("deep_model"),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolver una ruta de modelo de Instagram sin llamar a ningún modelo.")
    parser.add_argument("tier", help="0-3 o deterministic/routine/quality/deep")
    parser.add_argument("--policy", required=True, help="ruta al JSON de política")
    parser.add_argument("--allowed", nargs="*", default=None,
                        help="allowlist del runtime; por defecto usa la instantánea de la política")
    args = parser.parse_args()
    policy = load_policy(args.policy)
    decision = decide_from_policy(policy, args.tier,
                                  runtime_allowlist=args.allowed if args.allowed else None)
    print(json.dumps(decision.as_dict(), indent=2, ensure_ascii=False))
    raise SystemExit(0 if decision.status == "ready" else 2)


if __name__ == "__main__":
    main()
