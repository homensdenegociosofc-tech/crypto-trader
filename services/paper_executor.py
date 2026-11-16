from config import get_settings
class PaperTradingEngine:
    def __init__(self): self.balance=get_settings().initial_paper_balance; self.positions=[]; self.orders=[]; self.history=[]
    def summary(self): return {"balance":self.balance,"open_pnl":0,"daily_pnl":0,"equity":self.balance,"open_positions":len(self.positions),"trades_today":len(self.history)}
