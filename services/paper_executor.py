from datetime import datetime, timezone
from uuid import uuid4
from config import get_settings
from schemas import AccountSummary, AIDecision

class PaperTradingEngine:
    def __init__(self):
        settings = get_settings()
        self.balance = settings.initial_paper_balance
        self.positions = []
        self.orders = []
        self.history = []

    def summary(self) -> AccountSummary:
        return AccountSummary(balance=self.balance, equity=self.balance, open_positions=len(self.positions), trades_today=len(self.history))

    def execute(self, decision: AIDecision) -> dict:
        order = {"id": str(uuid4()), "decision_id": decision.decision_id, "symbol": decision.symbol, "side": decision.side, "type": decision.entry_type, "amount_usdt": decision.position_size_usdt, "status": "FILLED_SIMULATION", "created_at": datetime.now(timezone.utc).isoformat()}
        self.orders.append(order)
        position = {**order, "entry_price": decision.entry_price, "stop_loss": decision.stop_loss, "take_profit": decision.take_profit, "strategy": decision.strategy}
        self.positions.append(position)
        self.history.append({"event": "OPEN_POSITION", **order})
        return order
