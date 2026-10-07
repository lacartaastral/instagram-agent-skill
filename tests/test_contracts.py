import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
EXPECTED = {
    "ig-reel", "ig-viral", "ig-caption", "ig-carousel", "ig-story",
    "ig-profile", "ig-plan", "ig-human", "ig-comment", "ig-reply",
    "ig-dm", "ig-repurpose", "ig-audit", "ig-router",
}


class ContractTests(unittest.TestCase):
    def test_todas_las_skills_tienen_frontmatter_openclaw_unico(self):
        files = sorted(SKILLS.glob("*/SKILL.md"))
        self.assertEqual({path.parent.name for path in files}, EXPECTED)
        names = []
        for path in files:
            text = path.read_text(encoding="utf-8")
            match = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", text)
            self.assertIsNotNone(match, path)
            names.append(match.group(1))
            self.assertIn("## Contrato de OpenClaw", text)
        self.assertEqual(len(names), len(set(names)))

    def test_no_quedan_rutas_del_sistema_de_origen(self):
        # Se construyen los marcadores para que el propio test no reintroduzca
        # literalmente las rutas que está comprobando.
        legacy_vendor = "".join(("cl", "aude"))
        legacy_api_vendor = "".join(("anth", "ropic"))
        forbidden = (
            f"~/.{legacy_vendor}",
            f".{legacy_vendor}-plugin",
            f".{legacy_vendor}/skills",
            legacy_api_vendor,
        )
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for marker in forbidden:
                self.assertNotIn(marker, text, f"{marker} en {path}")

    def test_los_contratos_json_son_validos(self):
        for path in (ROOT / "config").glob("*.json"):
            with self.subTest(path=path):
                json.loads(path.read_text(encoding="utf-8"))
        rules = json.loads((ROOT / "config/platform-rules.json").read_text(encoding="utf-8"))
        self.assertEqual(rules["schema_version"], 1)
        for category, entries in rules["rules"].items():
            for key, entry in entries.items():
                with self.subTest(rule=f"{category}.{key}"):
                    self.assertIn("value", entry)
                    self.assertIn("verified", entry)
                    self.assertIn("verified_at", entry)
                    self.assertIn("source", entry)
                    self.assertIn("notes", entry)


if __name__ == "__main__":
    unittest.main()
