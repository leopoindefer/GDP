import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def Tableau(symbol_txt,symbol):
    liste_cours = list()
    for s, s_txt in zip(symbol, symbol_txt):
        s["Date"] = pd.to_datetime(s["Date"])
        s = s.set_index("Date")
        s_resampled = s.resample("M").first()
        close_columns = [col for col in s_resampled.columns if 'Close' in col]
        if close_columns:
            cours = round(s[close_columns].iloc[-1].values.sum(),2)
            cours_prec = round(s_resampled[close_columns].iloc[-2].values.sum(),2)
            var = round(((cours - cours_prec)/ cours_prec)*100,2)
            start_date = datetime.now() - timedelta(days=365*5)
            s_cinq_ans = s_resampled[s_resampled.index>=start_date]
            variation = s_cinq_ans[close_columns].pct_change().dropna()
            renta_moy = variation.values.mean()
            renta_moy = round(renta_moy*100,2)
            risque_moy = np.std(s_cinq_ans[close_columns]).values.mean()
            risque_moy = round(risque_moy,2)
            line = [str(val) for val in s_cinq_ans[close_columns].values.flatten()]
            liste_cours.append({"SYMBOLE": s_txt, "DERNIER": f'{cours}', "M-1": f'{cours_prec}', "VAR": f'{var}%', "RENTABILITE": f'{renta_moy}%', "VOLATILITE": f'{risque_moy}', "VISION":line})
    macro = pd.DataFrame(liste_cours)
    macro.set_index('SYMBOLE', inplace=True)
    return macro