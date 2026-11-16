import numpy as np
import pandas as pd
class IndicatorEngine:
    @staticmethod
    def wilder(s:pd.Series,n:int): return s.ewm(alpha=1/n,adjust=False,min_periods=n).mean()
    def calculate(self,df:pd.DataFrame)->pd.DataFrame:
        x=df.copy(); c=x.close; h=x.high; l=x.low
        for n in (9,21,50,200): x[f"ema_{n}"]=c.ewm(span=n,adjust=False,min_periods=n).mean()
        delta=c.diff(); gain=delta.clip(lower=0); loss=(-delta).clip(lower=0)
        ag=self.wilder(gain,14); al=self.wilder(loss,14); rs=ag/al.replace(0,np.nan); x["rsi_14"]=100-(100/(1+rs))
        prev=c.shift(1); tr=pd.concat([(h-l),(h-prev).abs(),(l-prev).abs()],axis=1).max(axis=1); x["atr_14"]=self.wilder(tr,14); x["atr_pct"]=x.atr_14/c*100
        up=h.diff(); down=-l.diff(); plus_dm=up.where((up>down)&(up>0),0.0); minus_dm=down.where((down>up)&(down>0),0.0)
        atr=self.wilder(tr,14); plus_di=100*self.wilder(plus_dm,14)/atr; minus_di=100*self.wilder(minus_dm,14)/atr
        dx=100*(plus_di-minus_di).abs()/(plus_di+minus_di).replace(0,np.nan); x["adx_14"]=self.wilder(dx,14); x["plus_di"]=plus_di; x["minus_di"]=minus_di
        x["bb_mid"]=c.rolling(20).mean(); std=c.rolling(20).std(ddof=0); x["bb_upper"]=x.bb_mid+2*std; x["bb_lower"]=x.bb_mid-2*std; x["bb_width_pct"]=(x.bb_upper-x.bb_lower)/x.bb_mid*100
        x["volume_sma_20"]=x.volume.rolling(20).mean(); x["volume_ratio"]=x.volume/x.volume_sma_20
        x["high_20_prev"]=h.shift(1).rolling(20).max(); x["low_20_prev"]=l.shift(1).rolling(20).min()
        x["return_1"]=c.pct_change()*100; x["return_4"]=c.pct_change(4)*100
        return x
