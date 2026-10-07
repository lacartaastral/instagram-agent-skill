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
    def test_all_skills_have_unique_openclaw_frontmatter(self):
        files = sorted(SKILLS.glob("*/SKILL.md"))
        self.assertEqual({path.parent.name for path in files}, EXPECTED)
        names = []
        for path in files:
            text = path.read_text(encoding="utf-8")
            match = re.search(r"(?m)^name:\s*([a-z0-9-]+)\s*$", text)
            self.assertIsNotNone(match, path)
            names.append(match.group(1))
            self.assertIn("## OpenClaw contract", text)
        self.assertEqual(len(names), len(set(names)))

    def test_no_upstream_assistant_paths_remain(self):
        forbidden = ("~/" + ".claude", "." + "claude-plugin", "." + "claude/skills")
        for path in ROOT.rglob("*"):
            if not path.is_file() or ".git" in path.parts:
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            for marker in forbidden:
                self.assertNotIn(marker, text, f"{marker} in {path}")

    def test_json_contracts_are_valid(self):
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
