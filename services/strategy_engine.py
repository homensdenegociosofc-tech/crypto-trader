class StrategyEngine:
    """Classifica oportunidades; não executa ordens e não promete rentabilidade."""
    def evaluate(self,row:dict)->dict:
        price=row["close"]; ema9=row["ema_9"]; ema21=row["ema_21"]; ema50=row["ema_50"]; rsi=row["rsi_14"]; adx=row["adx_14"]
        vr=row["volume_ratio"]; atrp=row["atr_pct"]; upper=row["bb_upper"]; lower=row["bb_lower"]
        high20=row["high_20_prev"]; low20=row["low_20_prev"]
        trend="ALTA" if ema9>ema21>ema50 and price>ema21 else "BAIXA" if ema9<ema21<ema50 and price<ema21 else "LATERAL"
        volatility="ALTA" if atrp>=2.0 else "BAIXA" if atrp<=0.45 else "NORMAL"
        setups=[]
        # 1 Tendência: alinhamento + ADX + momentum não extremo
        if trend=="ALTA" and adx>=23 and 52<=rsi<=68: setups.append(self._s("TENDENCIA","BUY",3,["EMA 9>21>50","ADX forte","RSI favorável"]))
        if trend=="BAIXA" and adx>=23 and 32<=rsi<=48: setups.append(self._s("TENDENCIA","SELL",3,["EMA 9<21<50","ADX forte","RSI favorável"]))
        # 2 Rompimento: preço rompe faixa anterior com participação
        if price>high20 and vr>=1.35 and adx>=20: setups.append(self._s("ROMPIMENTO","BUY",3,["Rompimento máxima 20 candles","Volume acima da média","ADX confirma"]))
        if price<low20 and vr>=1.35 and adx>=20: setups.append(self._s("ROMPIMENTO","SELL",3,["Rompimento mínima 20 candles","Volume acima da média","ADX confirma"]))
        # 3 Retração: tendência existente e retorno à média rápida
        dist21=abs(price-ema21)/price*100
        if trend=="ALTA" and dist21<=0.45 and 42<=rsi<=58 and adx>=20: setups.append(self._s("RETRACAO","BUY",2,["Tendência de alta","Preço próximo EMA21","Momentum resetado"]))
        if trend=="BAIXA" and dist21<=0.45 and 42<=rsi<=58 and adx>=20: setups.append(self._s("RETRACAO","SELL",2,["Tendência de baixa","Preço próximo EMA21","Momentum resetado"]))
        # 4 Reversão: só em extensão, ADX baixo para evitar lutar contra tendência forte
        if price<lower and rsi<=28 and adx<23: setups.append(self._s("REVERSAO","BUY",2,["Abaixo da Banda inferior","RSI sobrevendido","ADX não confirma tendência forte"]))
        if price>upper and rsi>=72 and adx<23: setups.append(self._s("REVERSAO","SELL",2,["Acima da Banda superior","RSI sobrecomprado","ADX não confirma tendência forte"]))
        best=max(setups,key=lambda z:z["score"],default=None)
        return {"regime":trend,"volatility":volatility,"candidate":best,"all_candidates":setups,"trade_allowed":False,"note":"Somente análise. A execução automática permanece desativada."}
    @staticmethod
    def _s(name,side,score,reasons): return {"strategy":name,"side":side,"score":score,"reasons":reasons}
