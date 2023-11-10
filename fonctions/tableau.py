import pandas as pd

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
            line = [str(val) for val in s_resampled[close_columns].values.flatten()]
            liste_cours.append({"SYMBOLE": s_txt, "DERNIER": cours, "M-1": cours_prec, "VAR": f'{var}%', "VIEW":line})
    macro = pd.DataFrame(liste_cours)
    macro.set_index('SYMBOLE', inplace=True)
    return macro