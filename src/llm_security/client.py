"""Minimal client for the local Ollama HTTP API."""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

DEFAULT_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3.2:3b"


class OllamaClient:
    """Talks to a locally-running Ollama server.

    If `system` is set, it's prepended to every request — that's how we
    apply the hardened system prompt during blue-team testing.
    """

    def __init__(
        self,
        base_url: str | None = None,
        model: str | None = None,
        system: str | None = None,
    ):
        self.base_url = base_url or os.getenv("OLLAMA_URL", DEFAULT_URL)
        self.model = model or os.getenv("OLLAMA_MODEL", DEFAULT_MODEL)
        self.system = system

    def generate(
        self,
        prompt: str,
        timeout: int = 120,
        temperature: float | None = None,
    ) -> str:
        options = {}
        if temperature is not None:
            options["temperature"] = temperature

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": options,
        }
        if self.system:
            payload["system"] = self.system

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=timeout,
        )
        response.raise_for_status()
        return response.json()["response"]

    def is_available(self) -> bool:
        try:
            requests.get(f"{self.base_url}/api/tags", timeout=2)
            return True
        except Exception:
            return False