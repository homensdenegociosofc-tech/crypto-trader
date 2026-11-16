from dataclasses import dataclass
from config import get_settings
from schemas import AIDecision, AccountSummary

@dataclass
class GateResult:
    approved: bool
    reason: str

class RiskGate:
    def __init__(self):
        self.settings = get_settings()

    def validate(self, decision: AIDecision, account: AccountSummary) -> GateResult:
        if decision.decision == "NO_TRADE":
            return GateResult(False, decision.reason)
        if self.settings.real_trading_enabled:
            return GateResult(False, "MODO_REAL_BLOQUEADO_NESTA_FASE")
        if decision.symbol is None or decision.stop_loss is None or decision.take_profit is None:
            return GateResult(False, "DECISAO_INCOMPLETA")
        if decision.risk_percentage is None or decision.risk_percentage > self.settings.max_risk_per_trade_percent:
            return GateResult(False, "RISCO_ACIMA_DO_LIMITE")
        max_position = account.balance * self.settings.max_position_percent / 100
        if decision.position_size_usdt is None or decision.position_size_usdt > max_position:
            return GateResult(False, "POSICAO_ACIMA_DO_LIMITE")
        if account.open_positions >= self.settings.max_open_positions:
            return GateResult(False, "MAXIMO_DE_POSICOES_ATINGIDO")
        if account.trades_today >= self.settings.max_trades_per_day:
            return GateResult(False, "MAXIMO_DE_OPERACOES_ATINGIDO")
        if (decision.expected_risk_reward or 0) < self.settings.min_risk_reward:
            return GateResult(False, "RISCO_RETORNO_INSUFICIENTE")
        return GateResult(True, "APROVADA")
