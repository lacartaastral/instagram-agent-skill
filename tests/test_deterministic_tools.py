import copy
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


HOOKS = load_module("ig_hookscore", ROOT / "skills/ig-reel/hookscore.py")
BEATS = load_module("ig_beats", ROOT / "skills/ig-reel/beats.py")
CAPTION = load_module("ig_caption", ROOT / "skills/ig-caption/caption.py")
DETECT = load_module("ig_detect", ROOT / "skills/ig-human/detect.py")
HUMANIZE = load_module("ig_humanize", ROOT / "skills/ig-human/humanize.py")
sys.path.insert(0, str(ROOT / "skills/ig-reel"))
SWIPE = load_module("ig_swipe", ROOT / "skills/ig-viral/swipe.py")


class DeterministicToolTests(unittest.TestCase):
    def test_repeated_core_analysis_is_identical(self):
        hook = "I lost $18,000 because of one missing contract."
        self.assertEqual(HOOKS.run(hook), HOOKS.run(hook))
        script = "I lost $18,000.\nNow I use one clause.\nComment CONTRACT."
        self.assertEqual(BEATS.analyse(script, target=20), BEATS.analyse(script, target=20))
        text = "Stop scrolling. I built this in Madrid. Comment CONTRACT. #contracts"
        self.assertEqual(CAPTION.analyse(text, keywords=["Madrid", "pricing"]), CAPTION.analyse(text, keywords=["Madrid", "pricing"]))

    def test_humanizer_and_detector_use_local_resources(self):
        lexicon = HUMANIZE.load_lexicon()
        raw = "This is — robust.\u200b"
        clean_a, report_a = HUMANIZE.humanize(raw, lexicon)
        clean_b, report_b = HUMANIZE.humanize(raw, lexicon)
        self.assertEqual((clean_a, report_a), (clean_b, report_b))
        self.assertNotIn("—", clean_a)
        self.assertNotIn("\u200b", clean_a)
        self.assertEqual(DETECT.run(clean_a, lexicon), DETECT.run(clean_a, lexicon))

    def test_swipe_ranking_is_deterministic(self):
        rows = [
            {"account": "@a", "followers": 1000, "median": 100, "views": 500, "hook": "Nobody tells you this"},
            {"account": "@b", "followers": 1000, "median": 200, "views": 220, "hook": "A normal day"},
        ]
        formulas = SWIPE.load_formulas(ROOT / "skills/ig-reel/hooks.json")
        left = SWIPE.analyse(copy.deepcopy(rows), formulas)
        right = SWIPE.analyse(copy.deepcopy(rows), formulas)
        self.assertEqual(left, right)
        self.assertEqual(left["reels"][0]["account"], "@a")

    def test_swipe_accepts_spanish_headers(self):
        with tempfile.NamedTemporaryFile("w+", encoding="utf-8") as handle:
            handle.write("cuenta\tseguidores\tmediana\tvisitas\tgancho\n")
            handle.write("@ejemplo\t4000\t1000\t4000\tNadie te cuenta esto\n")
            handle.flush()
            rows = SWIPE.read_rows(handle.name)
        self.assertEqual(rows[0]["account"], "@ejemplo")
        self.assertEqual(rows[0]["views"], 4000)
        self.assertEqual(rows[0]["hook"], "Nadie te cuenta esto")

    def test_tools_run_from_outside_repo(self):
        commands = [
            (ROOT / "skills/ig-reel/hookscore.py", ["--json"], "Concrete $20 hook"),
            (ROOT / "skills/ig-reel/beats.py", ["--json"], "A $20 hook.\nThen one result."),
            (ROOT / "skills/ig-human/humanize.py", ["--json"], "This is robust."),
            (ROOT / "skills/ig-caption/caption.py", ["--json"], "Comment CONTRACT."),
        ]
        for script, args, stdin in commands:
            with self.subTest(script=script):
                result = subprocess.run([sys.executable, str(script), *args], input=stdin, text=True, capture_output=True, cwd="/tmp")
                self.assertIn(result.returncode, (0, 1))
                self.assertNotIn("Traceback", result.stderr)
                json.loads(result.stdout)


if __name__ == "__main__":
    unittest.main()
