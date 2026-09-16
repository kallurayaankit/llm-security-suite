"""Loads attack definitions from YAML files."""
import os
from dataclasses import dataclass, field
from pathlib import Path
import yaml


ATTACKS_DIR = Path(os.getenv("ATTACKS_DIR", Path(__file__).parent.parent.parent / "attacks"))


@dataclass
class Attack:
    id: str
    name: str
    severity: str
    payload: str = ""
    turns: list[str] = field(default_factory=list)
    success_signals: list[str] = field(default_factory=list)
    refusal_signals: list[str] = field(default_factory=list)
    source_file: str = ""

    @property
    def is_multi_turn(self) -> bool:
        return bool(self.turns)

    @property
    def full_text(self) -> str:
        """Payload text for the judge — concatenates turns if multi-turn."""
        if self.turns:
            return "\n---\n".join(self.turns)
        return self.payload


def load_attacks(only_file: str | None = None) -> list[Attack]:
    attacks: list[Attack] = []

    if only_file:
        files = [ATTACKS_DIR / only_file]
    else:
        files = sorted(ATTACKS_DIR.glob("*.yaml"))

    for path in files:
        with open(path, "r", encoding="utf-8") as f:
            entries = yaml.safe_load(f) or []
        for entry in entries:
            turns_raw = entry.get("turns") or []
            attacks.append(
                Attack(
                    id=entry["id"],
                    name=entry["name"],
                    severity=entry.get("severity", "medium"),
                    payload=(entry.get("payload") or "").strip(),
                    turns=[t.strip() for t in turns_raw],
                    success_signals=[s.lower() for s in entry.get("success_signals", [])],
                    refusal_signals=[s.lower() for s in entry.get("refusal_signals", [])],
                    source_file=path.name,
                )
            )

    return attacks