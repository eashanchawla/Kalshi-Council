import requests
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from backend.config import settings

class TokenUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int

class ChatResponse(BaseModel):
    content: str
    model: str
    usage: TokenUsage
    raw_response: Dict[str, Any]

class OpenRouterClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: Optional[str] = None,
        system: Optional[str] = None,
        max_tokens: Optional[int] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 1.0
    ) -> ChatResponse:
        """
        Calls OpenRouter's /api/v1/chat/completions endpoint.
        """
        target_model = model or settings.OPENROUTER_DEFAULT_MODEL

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/kalshi-council", # Site name for OpenRouter rankings
            "X-Title": "Kalshi Council"
        }

        # Prepare messages
        formatted_messages = []
        if system:
            formatted_messages.append({"role": "system", "content": system})
        formatted_messages.extend(messages)

        payload = {
            "model": target_model,
            "messages": formatted_messages,
            "temperature": temperature
        }

        if max_tokens:
            payload["max_tokens"] = max_tokens
        if tools:
            payload["tools"] = tools

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        data = response.json()

        # Extract content and usage
        choice = data["choices"][0]
        content = choice["message"].get("content", "")
        usage_data = data.get("usage", {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0})

        usage = TokenUsage(
            prompt_tokens=usage_data.get("prompt_tokens", 0),
            completion_tokens=usage_data.get("completion_tokens", 0),
            total_tokens=usage_data.get("total_tokens", 0)
        )

        return ChatResponse(
            content=content,
            model=data.get("model", target_model),
            usage=usage,
            raw_response=data
        )

openrouter_client = OpenRouterClient()
