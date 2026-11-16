from config import get_settings


class PaperTradingEngine:
    """Estado básico do Paper Trading.

    Nesta fase o motor apenas fornece saldo e coleções vazias.
    O motor de análise não abre operações automaticamente.
    """

    def __init__(self):
        settings = get_settings()
        self.balance = float(settings.initial_paper_balance)
        self.positions = []
        self.orders = []
        self.history = []

    def summary(self) -> dict:
        return {
            "balance": self.balance,
            "open_pnl": 0.0,
            "daily_pnl": 0.0,
            "equity": self.balance,
            "open_positions": len(self.positions),
            "trades_today": len(self.history),
        }
