from uuid import uuid4
from schemas import AIDecision
from .base import AIProvider

class OpenAIProvider(AIProvider):
    async def generate_decision(self, snapshot: dict) -> AIDecision:
        return AIDecision(decision_id=str(uuid4()), decision="NO_TRADE", reason="OPENAI_PROVIDER_PREPARADO_MAS_AINDA_NAO_ATIVADO")
