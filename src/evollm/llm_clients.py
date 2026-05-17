"""LLM client abstraction layer for EvoLLM strategy generation.

Supports OpenAI, Anthropic, and Google (Gemini) providers.
API keys are loaded from a .env file at the project root (or from the
environment if already set).
"""

import logging
import os
import re
import time
from dataclasses import dataclass
from typing import Any

import anthropic
import openai
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Model registry
# ---------------------------------------------------------------------------

PROVIDER_OPENAI = "openai"
PROVIDER_ANTHROPIC = "anthropic"
PROVIDER_GOOGLE = "google"

# Maps registry key -> (provider, api_model_id)
# Verified against live APIs on 2026-04-08.
MODEL_REGISTRY: dict[str, tuple[str, str]] = {
    # ── Modelos originales del paper (para comparación) ──────────────────────
    "chatgpt-4o-latest": (PROVIDER_OPENAI,    "chatgpt-4o-latest"),
    "claude-3-5-sonnet": (PROVIDER_ANTHROPIC, "claude-3-5-sonnet-20240620"),
    # ── Modelos nuevos (abril 2026) ───────────────────────────────────────────
    "gpt-5.4-mini":             (PROVIDER_OPENAI,    "gpt-5.4-mini"),
    "claude-sonnet-4-6":        (PROVIDER_ANTHROPIC, "claude-sonnet-4-6"),
    "gemini-3.1-pro-preview":   (PROVIDER_GOOGLE,    "gemini-3.1-pro-preview"),
    "gemini-2.5-flash":         (PROVIDER_GOOGLE,    "gemini-2.5-flash"),
}

# Default model key per provider
PROVIDER_DEFAULTS: dict[str, str] = {
    PROVIDER_OPENAI:    "gpt-5.4-mini",
    PROVIDER_ANTHROPIC: "claude-sonnet-4-6",
    PROVIDER_GOOGLE:    "gemini-3.1-pro-preview",
}

# Phase 2 pre-registration (PHASE2_PREREG.md §2, Option A): a SINGLE fixed
# model performs the natural-language → Python conversion for ALL strategy
# generators, so provider identity is not confounded with coding ability.
# Strategy *generation* stays per-model; only *conversion* is held constant.
FIXED_CONVERTER_MODEL: str = "gpt-5.4-mini"

# Human-readable display names for the GUI
MODEL_DISPLAY_NAMES: dict[str, str] = {
    # Originales
    "chatgpt-4o-latest": "GPT-4o-latest (paper original)",
    "claude-3-5-sonnet": "Claude 3.5 Sonnet (paper original)",
    # Nuevos
    "gpt-5.4-mini":           "GPT-5.4 Mini (abril 2026)",
    "claude-sonnet-4-6":      "Claude Sonnet 4.6 (abril 2026)",
    "gemini-2.5-flash":       "Gemini 2.5 Flash",
    "gemini-3.1-pro-preview": "Gemini 3.1 Pro Preview (abril 2026)",
}

# o-series models that do not accept a temperature parameter
_NO_TEMPERATURE_MODELS: set[str] = set()

# ---------------------------------------------------------------------------
# Retry configuration
# ---------------------------------------------------------------------------

# Google: reintentos ante 503 (servidor saturado, transitorio)
_GOOGLE_MAX_RETRIES_503 = 6
_GOOGLE_BACKOFF_503_BASE = 5      # segundos — se duplica en cada intento
_GOOGLE_BACKOFF_503_MAX = 120     # cap máximo de espera por intento

# Google: reintentos ante 429 (cuota agotada, puede ser largo)
# El error devuelve retryDelay; usamos ese valor si está disponible,
# con un cap para no bloquear indefinidamente en un solo intento.
_GOOGLE_MAX_RETRIES_429 = 3
_GOOGLE_BACKOFF_429_DEFAULT = 60  # segundos si no viene retryDelay en el error
_GOOGLE_BACKOFF_429_CAP = 300     # cap: no esperar más de 5 min por intento

# OpenAI: reintentos ante errores de servidor (5xx) o rate limit (429)
_OPENAI_MAX_RETRIES = 5
_OPENAI_BACKOFF_BASE = 5
_OPENAI_BACKOFF_MAX = 60


# ---------------------------------------------------------------------------
# Client dataclass
# ---------------------------------------------------------------------------

@dataclass
class LLMClient:
  """Wraps a native API client together with model metadata."""
  client: Any
  model_key: str
  model_id: str
  provider: str


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------

def load_api_keys() -> None:
  """Load API keys from the nearest .env file.

  Uses override=True so that values in .env always win over any empty or
  stale variables that may already be set in the shell environment.
  Safe to call multiple times.
  """
  load_dotenv(override=True)


def resolve_model(provider: str, model_override: str | None) -> str:
  """Return the MODEL_REGISTRY key for a given provider and optional override.

  Args:
    provider: One of 'openai', 'anthropic', 'google'.
    model_override: Explicit registry key (e.g. 'o4-mini'), or None to use
      the provider default.

  Returns:
    A valid key in MODEL_REGISTRY.
  """
  if model_override is not None:
    if model_override not in MODEL_REGISTRY:
      raise ValueError(
          f"Unknown model '{model_override}'. Valid options: {list(MODEL_REGISTRY)}"
      )
    registry_provider, _ = MODEL_REGISTRY[model_override]
    if registry_provider != provider:
      raise ValueError(
          f"Model '{model_override}' belongs to provider '{registry_provider}',"
          f" not '{provider}'"
      )
    return model_override
  if provider not in PROVIDER_DEFAULTS:
    raise ValueError(
        f"Unknown provider '{provider}'. Valid options: {list(PROVIDER_DEFAULTS)}"
    )
  return PROVIDER_DEFAULTS[provider]


def make_client(model_key: str) -> LLMClient:
  """Construct the appropriate API client for the given model registry key."""
  if model_key not in MODEL_REGISTRY:
    raise ValueError(
        f"Unknown model key: '{model_key}'. Valid options: {list(MODEL_REGISTRY)}"
    )

  provider, model_id = MODEL_REGISTRY[model_key]

  if provider == PROVIDER_OPENAI:
    api_key = os.environ.get("OPENAI_API_KEY", "")
    native: Any = openai.OpenAI(api_key=api_key)

  elif provider == PROVIDER_ANTHROPIC:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    native = anthropic.Anthropic(api_key=api_key)

  elif provider == PROVIDER_GOOGLE:
    try:
      from google import genai as google_genai  # type: ignore[import-untyped]
    except ImportError as exc:
      raise ImportError(
          "The 'google-genai' package is required for Google models. "
          "Install it with: pip install google-genai"
      ) from exc
    api_key = os.environ.get("GOOGLE_API_KEY", "")
    native = google_genai.Client(api_key=api_key)

  else:
    raise ValueError(f"Unknown provider: '{provider}'")

  return LLMClient(client=native, model_key=model_key, model_id=model_id, provider=provider)


def get_response(llm: LLMClient, system: str, messages: list[dict[str, str]],
                 temp: float) -> str:
  """Dispatch to the appropriate provider and return the response text."""
  if llm.provider == PROVIDER_OPENAI:
    return _openai_message(llm.client, llm.model_id, system, messages, temp)
  if llm.provider == PROVIDER_ANTHROPIC:
    return _anthropic_message(llm.client, llm.model_id, system, messages, temp)
  if llm.provider == PROVIDER_GOOGLE:
    return _google_message(llm.client, llm.model_id, system, messages, temp)
  raise ValueError(f"Unknown provider: '{llm.provider}'")


# ---------------------------------------------------------------------------
# Internal utilities
# ---------------------------------------------------------------------------

def _parse_google_retry_delay(error: Exception) -> int | None:
  """Extrae retryDelay en segundos del mensaje de error de Google si está disponible.

  El error 429 suele incluir algo como: 'Please retry in 2h57m18.980328741s'
  o bien un campo retryDelay en los detalles JSON del error.
  Retorna segundos como entero, o None si no se puede parsear.
  """
  msg = str(error)

  # Intentar parsear formato "XhYmZs"
  pattern = r"retry in\s+(?:(\d+)h)?(?:(\d+)m)?(?:([\d.]+)s)?"
  match = re.search(pattern, msg, re.IGNORECASE)
  if match:
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(float(match.group(3) or 0))
    return hours * 3600 + minutes * 60 + seconds + 30  # +30s de margen

  # Intentar parsear retryDelay numérico en segundos (e.g. 'retryDelay': '10638s')
  delay_match = re.search(r"retryDelay['\"\s:]+(\d+)s", msg)
  if delay_match:
    return int(delay_match.group(1)) + 30

  return None


# ---------------------------------------------------------------------------
# Provider-specific implementations
# ---------------------------------------------------------------------------

def _openai_message(client: openai.OpenAI, model_id: str, system: str,
                    messages: list[dict[str, str]], temp: float) -> str:
  """Llama a la API de OpenAI con retry ante errores de servidor y rate limit."""
  full_messages = [{"role": "system", "content": system}] + messages
  kwargs: dict[str, Any] = {"model": model_id, "messages": full_messages}

  if model_id not in _NO_TEMPERATURE_MODELS:
    kwargs["temperature"] = temp

  last_exc: Exception | None = None
  for attempt in range(_OPENAI_MAX_RETRIES):
    try:
      response = client.chat.completions.create(**kwargs)
      return response.choices[0].message.content
    except openai.RateLimitError as exc:
      wait = min(_OPENAI_BACKOFF_BASE * (2 ** attempt), _OPENAI_BACKOFF_MAX)
      logger.warning(
          "[OpenAI] RateLimitError en intento %d/%d. Esperando %ds...",
          attempt + 1, _OPENAI_MAX_RETRIES, wait,
      )
      last_exc = exc
      time.sleep(wait)
    except openai.InternalServerError as exc:
      wait = min(_OPENAI_BACKOFF_BASE * (2 ** attempt), _OPENAI_BACKOFF_MAX)
      logger.warning(
          "[OpenAI] InternalServerError en intento %d/%d. Esperando %ds...",
          attempt + 1, _OPENAI_MAX_RETRIES, wait,
      )
      last_exc = exc
      time.sleep(wait)

  raise RuntimeError(
      f"[OpenAI] Falló tras {_OPENAI_MAX_RETRIES} intentos para el modelo '{model_id}'. "
      f"Último error: {last_exc}"
  )


def _anthropic_message(client: anthropic.Anthropic, model_id: str, system: str,
                       messages: list[dict[str, str]], temp: float) -> str:
  """Llama a la API de Anthropic con retry ante errores de servidor."""
  response = None
  for attempt in range(5):
    try:
      response = client.messages.create(
          model=model_id,
          max_tokens=4096,
          temperature=temp,
          system=system,
          messages=messages,
      )
      break
    except anthropic.InternalServerError:
      wait = min(5 * (2 ** attempt), 60)
      logger.warning(
          "[Anthropic] InternalServerError en intento %d/5. Esperando %ds...",
          attempt + 1, wait,
      )
      time.sleep(wait)

  if response is None:
    raise RuntimeError(
        f"[Anthropic] API retornó InternalServerError 5 veces para el modelo '{model_id}'"
    )
  return response.content[0].text


def _google_message(client: Any, model_id: str, system: str,
                    messages: list[dict[str, str]], temp: float) -> str:
  """Llama a la API de Google Gemini con manejo diferenciado de errores.

  - 503 UNAVAILABLE (servidor saturado): backoff exponencial, hasta
    _GOOGLE_MAX_RETRIES_503 reintentos. Es un error transitorio.
  - 429 RESOURCE_EXHAUSTED (cuota agotada): espera el retryDelay que
    devuelve Google (o un valor por defecto), hasta _GOOGLE_MAX_RETRIES_429
    reintentos. Si la espera supera el cap, lanza excepción inmediatamente
    para evitar bloquear el proceso horas enteras.

  Usa google.genai.Client (reemplaza el paquete google-generativeai obsoleto).
  Convierte el formato de mensajes OpenAI-style al formato Content de Gemini.
  """
  from google.genai import types  # type: ignore[import-untyped]
  from google.genai import errors as google_errors  # type: ignore[import-untyped]

  def _build_and_call() -> str:
    """Construye la request y ejecuta la llamada. Sin lógica de retry aquí."""
    history: list[Any] = []
    for msg in messages[:-1]:
      role = "user" if msg["role"] == "user" else "model"
      history.append(types.Content(role=role, parts=[types.Part(text=msg["content"])]))

    config = types.GenerateContentConfig(
        system_instruction=system,
        temperature=temp,
        max_output_tokens=4096,
    )

    if history:
      chat = client.chats.create(model=model_id, config=config, history=history)
      response = chat.send_message(messages[-1]["content"])
    else:
      response = client.models.generate_content(
          model=model_id,
          contents=messages[-1]["content"],
          config=config,
      )
    return response.text

  # ── Retry loop ─────────────────────────────────────────────────────────────
  retries_503 = 0
  retries_429 = 0

  while True:
    try:
      return _build_and_call()

    except google_errors.ServerError as exc:
      # 503 UNAVAILABLE — error transitorio de capacidad
      if retries_503 >= _GOOGLE_MAX_RETRIES_503:
        raise RuntimeError(
            f"[Google] 503 UNAVAILABLE persistente tras {_GOOGLE_MAX_RETRIES_503} "
            f"reintentos para el modelo '{model_id}'. Último error: {exc}"
        ) from exc

      wait = min(_GOOGLE_BACKOFF_503_BASE * (2 ** retries_503), _GOOGLE_BACKOFF_503_MAX)
      logger.warning(
          "[Google] 503 UNAVAILABLE en intento %d/%d para '%s'. Esperando %ds...",
          retries_503 + 1, _GOOGLE_MAX_RETRIES_503, model_id, wait,
      )
      retries_503 += 1
      time.sleep(wait)

    except google_errors.ClientError as exc:
      # 429 RESOURCE_EXHAUSTED — cuota agotada
      if "429" not in str(exc) and "RESOURCE_EXHAUSTED" not in str(exc):
        # Otro ClientError (ej. 400 BAD_REQUEST): no reintentar
        raise

      if retries_429 >= _GOOGLE_MAX_RETRIES_429:
        raise RuntimeError(
            f"[Google] 429 RESOURCE_EXHAUSTED persistente tras {_GOOGLE_MAX_RETRIES_429} "
            f"reintentos para el modelo '{model_id}'. "
            f"Verifique su cuota en https://ai.dev/rate-limit. "
            f"Último error: {exc}"
        ) from exc

      # Intentar extraer el retryDelay del mensaje de error
      suggested_wait = _parse_google_retry_delay(exc)

      if suggested_wait is not None and suggested_wait > _GOOGLE_BACKOFF_429_CAP:
        # El delay sugerido supera el cap: no tiene sentido esperar aquí,
        # mejor fallar rápido y dejar que el usuario reintente manualmente.
        raise RuntimeError(
            f"[Google] 429 RESOURCE_EXHAUSTED para '{model_id}'. "
            f"Google sugiere esperar {suggested_wait}s (~{suggested_wait//3600}h "
            f"{(suggested_wait%3600)//60}m). "
            f"Reintente manualmente más tarde o cambie de modelo."
        ) from exc

      wait = suggested_wait if suggested_wait is not None else _GOOGLE_BACKOFF_429_DEFAULT
      logger.warning(
          "[Google] 429 RESOURCE_EXHAUSTED en intento %d/%d para '%s'. "
          "Esperando %ds antes de reintentar...",
          retries_429 + 1, _GOOGLE_MAX_RETRIES_429, model_id, wait,
      )
      retries_429 += 1
      time.sleep(wait)
