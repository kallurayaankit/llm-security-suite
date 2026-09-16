"""Loads attack definitions from YAML files."""

from dataclasses import dataclass, field
from pathlib import Path
import yaml


ATTACKS_DIR = Path(__file__).parent.parent.parent / "attacks"


@dataclass
class Attack:
    id: str
    name: str
    severity: str
    payload: str
    success_signals: list[str] = field(default_factory=list)
    refusal_signals: list[str] = field(default_factory=list)
    source_file: str = ""


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
            attacks.append(
                Attack(
                    id=entry["id"],
                    name=entry["name"],
                    severity=entry.get("severity", "medium"),
                    payload=entry["payload"].strip(),
                    success_signals=[s.lower() for s in entry.get("success_signals", [])],
                    refusal_signals=[s.lower() for s in entry.get("refusal_signals", [])],
                    source_file=path.name,
                )
            )

    return attacks