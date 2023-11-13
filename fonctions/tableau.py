import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def Tableau(periode, symbol_txt, symbol):
    if periode == "1 mois":
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
                mois_prec = datetime.now() - timedelta(days=31)
                s_mois_prec = s_resampled[s_resampled.index>=mois_prec]
                variation = s_cinq_ans[close_columns].pct_change().dropna()
                renta_moy = variation.values.mean()
                renta_moy = round(renta_moy*100,2)
                risque_moy = np.std(s_cinq_ans[close_columns]).values.mean()
                risque_moy = round(risque_moy,2)
                line = [str(val) for val in s_mois_prec[close_columns].values.flatten()]
                liste_cours.append({"SYMBOLE": s_txt, "ACTUEL": f'{cours}', "M-1": f'{cours_prec}', "VAR": f'{var}%', "RENTABILITÉ": f'{renta_moy}%', "VOLATILITÉ": f'{risque_moy}', "VISION":line})
        macro = pd.DataFrame(liste_cours)
        macro.set_index('SYMBOLE', inplace=True)
        return macro
    
    elif periode == "6 mois":
        liste_cours = list()
        for s, s_txt in zip(symbol, symbol_txt):
            s["Date"] = pd.to_datetime(s["Date"])
            s = s.set_index("Date")
            s_resampled = s.resample("M").first()
            close_columns = [col for col in s_resampled.columns if 'Close' in col]
            if close_columns:
                cours = round(s[close_columns].iloc[-1].values.sum(),2)
                cours_prec = round(s_resampled[close_columns].iloc[-7].values.sum(),2)
                var = round(((cours - cours_prec)/ cours_prec)*100,2)
                start_date = datetime.now() - timedelta(days=365*5)
                s_cinq_ans = s_resampled[s_resampled.index>=start_date]
                sixmois_prec = datetime.now() - timedelta(days=183)
                s_six_mois_prec = s_resampled[s_resampled.index>=sixmois_prec]
                variation = s_cinq_ans[close_columns].pct_change().dropna()
                renta_moy = variation.values.mean()
                renta_moy = round(renta_moy*100,2)
                risque_moy = np.std(s_cinq_ans[close_columns]).values.mean()
                risque_moy = round(risque_moy,2)
                line = [str(val) for val in s_six_mois_prec[close_columns].values.flatten()]
                liste_cours.append({"SYMBOLE": s_txt, "ACTUEL": f'{cours}', "M-6": f'{cours_prec}', "VAR": f'{var}%', "RENTABILITÉ": f'{renta_moy}%', "VOLATILITÉ": f'{risque_moy}', "VISION":line})
        macro = pd.DataFrame(liste_cours)
        macro.set_index('SYMBOLE', inplace=True)
        return macro
    
    elif periode == "1 an":
        liste_cours = list()
        for s, s_txt in zip(symbol, symbol_txt):
            s["Date"] = pd.to_datetime(s["Date"])
            s = s.set_index("Date")
            s_resampled = s.resample("M").first()
            close_columns = [col for col in s_resampled.columns if 'Close' in col]
            if close_columns:
                cours = round(s[close_columns].iloc[-1].values.sum(),2)
                cours_prec = round(s_resampled[close_columns].iloc[-13].values.sum(),2)
                var = round(((cours - cours_prec)/ cours_prec)*100,2)
                start_date = datetime.now() - timedelta(days=365*5)
                s_cinq_ans = s_resampled[s_resampled.index>=start_date]
                annee_prec = datetime.now() - timedelta(days=365)
                s_annee_prec = s_resampled[s_resampled.index>=annee_prec]
                variation = s_cinq_ans[close_columns].pct_change().dropna()
                renta_moy = variation.values.mean()
                renta_moy = round(renta_moy*100,2)
                risque_moy = np.std(s_cinq_ans[close_columns]).values.mean()
                risque_moy = round(risque_moy,2)
                line = [str(val) for val in s_annee_prec[close_columns].values.flatten()]
                liste_cours.append({"SYMBOLE": s_txt, "ACTUEL": f'{cours}', "N-1": f'{cours_prec}', "VAR": f'{var}%', "RENTABILITÉ": f'{renta_moy}%', "VOLATILITÉ": f'{risque_moy}', "VISION":line})
        macro = pd.DataFrame(liste_cours)
        macro.set_index('SYMBOLE', inplace=True)
        return macro
    
    elif periode == "5 ans":
        liste_cours = list()
        for s, s_txt in zip(symbol, symbol_txt):
            s["Date"] = pd.to_datetime(s["Date"])
            s = s.set_index("Date")
            s_resampled = s.resample("M").first()
            close_columns = [col for col in s_resampled.columns if 'Close' in col]
            if close_columns:
                cours = round(s[close_columns].iloc[-1].values.sum(),2)
                start_date = datetime.now() - timedelta(days=365*5)
                s_cinq_ans = s_resampled[s_resampled.index>=start_date]
                cours_prec = round(s_cinq_ans[close_columns].iloc[0].values.sum(),2)
                var = round(((cours - cours_prec)/ cours_prec)*100,2)
                variation = s_cinq_ans[close_columns].pct_change().dropna()
                renta_moy = variation.values.mean()
                renta_moy = round(renta_moy*100,2)
                risque_moy = np.std(s_cinq_ans[close_columns]).values.mean()
                risque_moy = round(risque_moy,2)
                line = [str(val) for val in s_cinq_ans[close_columns].values.flatten()]
                liste_cours.append({"SYMBOLE": s_txt, "ACTUEL": f'{cours}', "N-5": f'{cours_prec}', "VAR": f'{var}%', "RENTABILITÉ": f'{renta_moy}%', "VOLATILITÉ": f'{risque_moy}', "VISION":line})
        macro = pd.DataFrame(liste_cours)
        macro.set_index('SYMBOLE', inplace=True)
        return macro