import os
import pytest

from llm_security.client import OllamaClient
from llm_security.hardening import HARDENED_SYSTEM_PROMPT


def _system_prompt() -> str | None:
    """Return the hardened prompt when HARDENED=true is set."""
    if os.getenv("HARDENED", "false").lower() == "true":
        return HARDENED_SYSTEM_PROMPT
    return None


@pytest.fixture(scope="session")
def llm():
    return OllamaClient(system=_system_prompt())


def pytest_collection_modifyitems(config, items):
    if OllamaClient().is_available():
        return
    skip = pytest.mark.skip(reason="Ollama not reachable — skipping security tests")
    for item in items:
        item.add_marker(skip)