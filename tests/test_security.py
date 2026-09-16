"""Prompt-injection and jailbreak tests.

These tests FAIL when the model falls for an attack.
"""

import pytest

from llm_security.loader import load_attacks
from llm_security.scorer import score


ALL_ATTACKS = load_attacks()


@pytest.mark.parametrize("attack", ALL_ATTACKS, ids=lambda a: f"{a.id}-{a.name}")
def test_attack_is_resisted(llm, attack):
    response = llm.generate(attack.payload, timeout=120)
    result = score(attack, response)

    print(f"\n[{result.severity.upper()}] {attack.id} ({attack.name}) → {result.verdict}")
    print(f"   reason: {result.reason}")
    print(f"   response: {result.response[:200]}...")

    if result.verdict == "COMPLIED":
        pytest.fail(
            f"Model complied with attack {attack.id} ({attack.name}). "
            f"Reason: {result.reason}"
        )

    if result.verdict == "AMBIGUOUS":
        pytest.skip(f"Ambiguous response for {attack.id} — review manually")