"""Groq API client for Phase 4."""

from __future__ import annotations

import json
from typing import Any

import httpx


class GroqClientError(RuntimeError):
    """Raised when Groq API request or response handling fails."""


def call_groq_chat_completion(
    *,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    temperature: float = 0.3,
    timeout_seconds: int = 30,
) -> str:
    """Call Groq chat completions API and return assistant content."""
    url = "https://api.groq.com/openai/v1/chat/completions"
    body = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
    }
    try:
        response = httpx.post(
            url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "User-Agent": "mile1-zomato-phase4/1.0",
            },
            json=body,
            timeout=timeout_seconds,
        )
    except httpx.RequestError as exc:
        raise GroqClientError(f"Groq network error: {exc}") from exc

    if response.status_code >= 400:
        raise GroqClientError(f"Groq HTTP {response.status_code}: {response.text}")

    try:
        payload = response.json()
    except json.JSONDecodeError as exc:
        raise GroqClientError("Groq response is not valid JSON.") from exc

    return _extract_content(payload)


def _extract_content(payload: dict[str, Any]) -> str:
    choices = payload.get("choices")
    if not isinstance(choices, list) or not choices:
        raise GroqClientError("Groq response missing choices.")
    first = choices[0]
    if not isinstance(first, dict):
        raise GroqClientError("Groq response choice is malformed.")
    message = first.get("message")
    if not isinstance(message, dict):
        raise GroqClientError("Groq response missing message.")
    content = message.get("content")
    if not isinstance(content, str) or not content.strip():
        raise GroqClientError("Groq response missing assistant content.")
    return content

