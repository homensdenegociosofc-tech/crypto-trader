from abc import ABC, abstractmethod
from schemas import AIDecision

class AIProvider(ABC):
    @abstractmethod
    async def generate_decision(self, snapshot: dict) -> AIDecision:
        raise NotImplementedError
