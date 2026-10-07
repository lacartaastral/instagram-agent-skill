import tempfile
import unittest
from pathlib import Path

import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from shared.model_routing import decide, decide_from_policy, load_policy  # noqa: E402
from shared.storage import InstagramStorage, StorageError  # noqa: E402


class StorageAndRoutingTests(unittest.TestCase):
    def test_profile_and_speaker_state_isolated(self):
        with tempfile.TemporaryDirectory() as tmp:
            storage = InstagramStorage(Path(tmp))
            storage.ensure_profile("alpha", ["miriam"])
            storage.ensure_profile("beta", ["joaquin"])
            storage.write_text("alpha", "facts", "ALPHA ONLY")
            storage.write_text("alpha", "voice", "MIRIAM ONLY", speaker="miriam")
            self.assertEqual(storage.read_text("alpha", "facts"), "ALPHA ONLY")
            self.assertEqual(storage.read_text("alpha", "voice", "miriam"), "MIRIAM ONLY")
            self.assertNotIn("ALPHA", storage.profile_file("beta", "facts").read_text(encoding="utf-8"))
            self.assertNotEqual(storage.voice_file("alpha", "miriam"), storage.voice_file("beta", "joaquin"))

    def test_path_traversal_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            storage = InstagramStorage(Path(tmp))
            for bad in ("../beta", "alpha/../../beta", "", "A B"):
                with self.subTest(bad=bad), self.assertRaises(StorageError):
                    storage.profile_dir(bad)
            with self.assertRaises(StorageError):
                storage.profile_file("alpha", "unknown")

    def test_routing_is_fail_closed_and_tier_zero_is_local(self):
        allowed = ["openai/gpt-5.6-luna", "openai/gpt-5.6-sol", "openai/gpt-6-astra"]
        deterministic = decide(0, allowed_models=allowed, default_model=allowed[0], quality_model=allowed[1], deep_model=allowed[2])
        self.assertEqual(deterministic.status, "ready")
        self.assertIsNone(deterministic.model)
        self.assertFalse(deterministic.requires_subagent)

        routine = decide(1, allowed_models=allowed, default_model=allowed[0], quality_model=allowed[1], deep_model=allowed[2])
        self.assertEqual(routine.model, "openai/gpt-5.6-luna")
        self.assertFalse(routine.requires_subagent)

        quality = decide("quality", allowed_models=allowed, default_model=allowed[0], quality_model=allowed[1], deep_model=allowed[2])
        self.assertEqual(quality.model, "openai/gpt-5.6-sol")
        self.assertTrue(quality.requires_subagent)

        blocked = decide(3, allowed_models=[allowed[0]], default_model=allowed[0], quality_model=allowed[1], deep_model=allowed[2])
        self.assertEqual(blocked.status, "blocked")

    def test_policy_snapshot_resolves(self):
        policy = load_policy(ROOT / "config/model-routing.json")
        decision = decide_from_policy(policy, 0)
        self.assertEqual(decision.label, "DETERMINISTIC")
        self.assertIsNone(decision.model)
        self.assertEqual(policy["runtime"]["default_model"], "openai/gpt-5.6-luna")


if __name__ == "__main__":
    unittest.main()
