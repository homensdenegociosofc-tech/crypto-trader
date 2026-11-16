from config import get_settings
from .providers.base import AIProvider
from .providers.deepseek import DeepSeekProvider
from .providers.openai import OpenAIProvider

class AIProviderFactory:
    @staticmethod
    def create() -> AIProvider:
        provider = get_settings().ai_provider.lower()
        if provider == "deepseek":
            return DeepSeekProvider()
        if provider in {"openai", "chatgpt"}:
            return OpenAIProvider()
        raise ValueError(f"AI_PROVIDER não suportado: {provider}")

class DecisionOrchestrator:
    def __init__(self):
        self.provider = AIProviderFactory.create()
    async def decide(self, snapshot: dict):
        return await self.provider.generate_decision(snapshot)
