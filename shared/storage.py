"""Safe, profile-scoped storage for the OpenClaw Instagram skill pack.

State is deliberately outside the package.  Every profile and voice component
is validated before a path is resolved, and writes are atomic.  The module does
not accept an arbitrary path as a substitute for the OpenClaw workspace:
callers provide the effective workspace explicitly or through the documented
environment variable.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

PROFILE_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
VOICE_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]{0,63}$")
PROFILE_FILES = {
    "brand": "brand.md",
    "facts": "facts.md",
    "offers": "offers.md",
    "swipe": "swipe.md",
    "log": "log.md",
    "plan": "plan.md",
    "platform-rules": "platform-rules.json",
}
DEFAULT_STATE_RELATIVE = Path("state") / "instagram-agent"


class StorageError(ValueError):
    """Raised when a profile/voice or resolved path is unsafe."""


def _component(value: str, pattern: re.Pattern[str], label: str) -> str:
    candidate = str(value).strip().lower()
    if not pattern.fullmatch(candidate):
        raise StorageError(f"invalid {label}: {value!r}")
    return candidate


def _inside(root: Path, candidate: Path) -> Path:
    root_resolved = root.resolve()
    candidate_resolved = candidate.resolve()
    try:
        candidate_resolved.relative_to(root_resolved)
    except ValueError as exc:
        raise StorageError(f"path escapes storage root: {candidate}") from exc
    return candidate_resolved


@dataclass(frozen=True)
class InstagramStorage:
    workspace: Path

    def __post_init__(self) -> None:
        workspace = Path(self.workspace).expanduser().resolve()
        object.__setattr__(self, "workspace", workspace)

    @property
    def state_root(self) -> Path:
        return _inside(self.workspace, self.workspace / DEFAULT_STATE_RELATIVE)

    @classmethod
    def from_environment(cls, workspace: str | Path | None = None) -> "InstagramStorage":
        value = workspace or os.environ.get("OPENCLAW_WORKSPACE") or os.environ.get("OPENCLAW_AGENT_WORKSPACE")
        if not value:
            raise StorageError("effective OpenClaw workspace is required")
        return cls(Path(value))

    def profile_dir(self, profile: str) -> Path:
        name = _component(profile, PROFILE_PATTERN, "profile")
        return _inside(self.state_root, self.state_root / "profiles" / name)

    def profile_file(self, profile: str, file_key: str) -> Path:
        try:
            filename = PROFILE_FILES[file_key]
        except KeyError as exc:
            raise StorageError(f"unsupported profile file: {file_key!r}") from exc
        return _inside(self.profile_dir(profile), self.profile_dir(profile) / filename)

    def voice_file(self, profile: str, speaker: str) -> Path:
        name = _component(speaker, VOICE_PATTERN, "speaker")
        profile_dir = self.profile_dir(profile)
        return _inside(profile_dir, profile_dir / "voices" / f"{name}.md")

    def ensure_profile(self, profile: str, voices: Iterable[str] = ()) -> list[Path]:
        directory = self.profile_dir(profile)
        directory.mkdir(parents=True, exist_ok=True)
        (directory / "voices").mkdir(parents=True, exist_ok=True)
        created: list[Path] = []
        for key, filename in PROFILE_FILES.items():
            path = self.profile_file(profile, key)
            if path.exists():
                continue
            if key == "platform-rules":
                source = Path(__file__).resolve().parents[1] / "config" / "platform-rules.json"
                shutil.copyfile(source, path)
            else:
                path.write_text(f"# {filename.rsplit('.', 1)[0]}\n\n", encoding="utf-8")
            created.append(path)
        for speaker in voices:
            path = self.voice_file(profile, speaker)
            if not path.exists():
                path.write_text("# Speaker voice\n\n", encoding="utf-8")
                created.append(path)
        return created

    def read_text(self, profile: str, file_key: str, speaker: str | None = None) -> str:
        path = self.voice_file(profile, speaker) if file_key == "voice" and speaker else self.profile_file(profile, file_key)
        return path.read_text(encoding="utf-8")

    def write_text(self, profile: str, file_key: str, text: str,
                   speaker: str | None = None) -> Path:
        path = self.voice_file(profile, speaker) if file_key == "voice" and speaker else self.profile_file(profile, file_key)
        self.profile_dir(profile).mkdir(parents=True, exist_ok=True)
        path.parent.mkdir(parents=True, exist_ok=True)
        _inside(self.state_root, path)
        fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=str(path.parent), text=True)
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                handle.write(text)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        return path


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Resolve or initialize Instagram profile state safely.")
    sub = parser.add_subparsers(dest="command", required=True)
    path = sub.add_parser("path")
    path.add_argument("--workspace")
    path.add_argument("--profile", required=True)
    path.add_argument("--file", choices=[*PROFILE_FILES, "voice"], required=True)
    path.add_argument("--speaker")
    init = sub.add_parser("init")
    init.add_argument("--workspace")
    init.add_argument("--profile", required=True)
    init.add_argument("--voices", nargs="*", default=[])
    return parser


def main() -> None:
    args = _parser().parse_args()
    storage = InstagramStorage.from_environment(args.workspace)
    if args.command == "path":
        if args.file == "voice" and not args.speaker:
            raise SystemExit("--speaker is required for --file voice")
        path = storage.voice_file(args.profile, args.speaker) if args.file == "voice" else storage.profile_file(args.profile, args.file)
        print(path)
        return
    created = storage.ensure_profile(args.profile, args.voices)
    print(json.dumps({"profile": args.profile, "state_root": str(storage.profile_dir(args.profile)),
                      "created": [str(path) for path in created]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
