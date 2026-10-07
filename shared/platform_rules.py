"""Load and merge mutable Instagram platform rules.

The skills keep mutable platform claims in JSON so a verification update does
not require editing thirteen prompts or a Python heuristic.  Values may be
present while still marked unverified; callers must surface that status.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RULES_PATH = REPO_ROOT / "config" / "platform-rules.json"


def _merge(base: dict[str, Any], overlay: dict[str, Any]) -> dict[str, Any]:
    result = copy.deepcopy(base)
    for key, value in overlay.items():
        if isinstance(value, dict) and isinstance(result.get(key), dict):
            result[key] = _merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def load_rules(path: str | Path | None = None) -> dict[str, Any]:
    """Load package defaults, optionally overlaid by a profile rules file."""
    with DEFAULT_RULES_PATH.open(encoding="utf-8") as handle:
        base = json.load(handle)
    if path is None:
        return base
    candidate = Path(path).expanduser().resolve()
    if candidate == DEFAULT_RULES_PATH.resolve():
        return base
    with candidate.open(encoding="utf-8") as handle:
        overlay = json.load(handle)
    return _merge(base, overlay)


def rule_entry(rules: dict[str, Any], dotted_key: str) -> dict[str, Any]:
    """Return a rule object by dotted key, or an empty object when absent."""
    node: Any = rules.get("rules", rules)
    for part in dotted_key.split("."):
        if not isinstance(node, dict):
            return {}
        node = node.get(part)
    return node if isinstance(node, dict) else {}


def rule_value(rules: dict[str, Any], dotted_key: str, default: Any = None) -> Any:
    entry = rule_entry(rules, dotted_key)
    return entry.get("value", default)


def rule_verified(rules: dict[str, Any], dotted_key: str) -> bool:
    return bool(rule_entry(rules, dotted_key).get("verified", False))


def unverified_rule_keys(rules: dict[str, Any]) -> list[str]:
    """Return dotted keys for present rules not independently verified."""
    found: list[str] = []

    def walk(node: Any, prefix: str = "") -> None:
        if not isinstance(node, dict):
            return
        if "value" in node and "verified" in node:
            if not node["verified"]:
                found.append(prefix)
            return
        for key, value in node.items():
            walk(value, f"{prefix}.{key}" if prefix else key)

    walk(rules.get("rules", rules))
    return found
