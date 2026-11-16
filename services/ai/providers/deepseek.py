import json
from uuid import uuid4
import httpx
from config import get_settings
from schemas import AIDecision
from .base import AIProvider

class DeepSeekProvider(AIProvider):
    URL = "https://api.deepseek.com/chat/completions"
    def __init__(self):
        self.settings = get_settings()

    async def generate_decision(self, snapshot: dict) -> AIDecision:
        if not self.settings.deepseek_api_key:
            return AIDecision(decision_id=str(uuid4()), decision="NO_TRADE", reason="DEEPSEEK_API_KEY_NAO_CONFIGURADA")
        system = "Você controla decisões de paper trading. Responda somente JSON compatível com AIDecision. Nunca omita stop, alvo, risco e tamanho quando abrir posição."
        payload = {"model": self.settings.ai_model, "response_format": {"type": "json_object"}, "messages": [{"role": "system", "content": system}, {"role": "user", "content": json.dumps(snapshot)}], "temperature": 0.1}
        try:
            async with httpx.AsyncClient(timeout=self.settings.ai_timeout_seconds) as client:
                response = await client.post(self.URL, headers={"Authorization": f"Bearer {self.settings.deepseek_api_key}"}, json=payload)
                response.raise_for_status()
                content = response.json()["choices"][0]["message"]["content"]
                return AIDecision.model_validate_json(content)
        except Exception as exc:
            return AIDecision(decision_id=str(uuid4()), decision="NO_TRADE", reason=f"AI_UNAVAILABLE:{type(exc).__name__}")
