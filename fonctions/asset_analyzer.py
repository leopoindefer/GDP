import pandas as pd
from typing import TypeVar, Generic
from datetime import datetime, timedelta
from .asset_transform import Transform

class Analyse(Transform):
    def __init__(self, selected_dataframes:dict):
        super().__init__(selected_dataframes)

    def KPI_1month(self):
        liste_cours = list()
        for symbol, asset_dataframe in self._selected_dataframes.items():
            try:
                asset_dataframe_resampled = Transform(asset_dataframe).resample()
                close_columns = [col for col in asset_dataframe_resampled.columns if 'Close' in col]
                if close_columns:
                    cours = round(asset_dataframe[close_columns].iloc[-1].values.sum(),2)
                    cours_prec = round(asset_dataframe_resampled[close_columns].iloc[-2].values.sum(),2)
                    var = round(((cours - cours_prec)/ cours_prec)*100,2)
                    mois_prec = datetime.now() - timedelta(days=31)
                    s_mois_prec = asset_dataframe[asset_dataframe.index>=mois_prec]
                    s_mois_prec_resampled = asset_dataframe_resampled[asset_dataframe_resampled.index>=mois_prec]
                    variation = s_mois_prec_resampled[close_columns].pct_change().dropna()
                    renta_moy = variation.values.mean()
                    renta_moy = round(renta_moy*100,2)
                    risque_moy = variation.values.std()
                    risque_moy = round(risque_moy*100,2)
                    line = [str(val) for val in s_mois_prec[close_columns].values.flatten()]
                    liste_cours.append({"SYMBOLE": symbol, "ACTUEL": f'{cours}', "M-1": f'{cours_prec}', "VAR": f'{var}%', "RENTABILITÉ": f'{renta_moy}%', "VOLATILITÉ": f'{risque_moy}%', "VISION":line})
            except FileNotFoundError:
                continue
            except Exception:
                continue
        macro = pd.DataFrame(liste_cours)
        macro.set_index('SYMBOLE', inplace=True)
        return macro

    def KPI_6month(self):
        liste_cours = []
        for symbol, asset_dataframe in self._selected_dataframes.items():
            s = pd.DataFrame(asset_dataframe)
            s.index = pd.to_datetime(s.index)
            s_resampled = s.resample("MS").first()
            close_columns = [col for col in s_resampled.columns if 'Close' in col]
            cours = round(s[close_columns].iloc[-1].values.sum(), 2)
            cours_prec = round(s_resampled[close_columns].iloc[-7].values.sum(),2)
            var = round(((cours - cours_prec)/ cours_prec)*100,2)
            sixmois_prec = datetime.now() - timedelta(days=183)
            
            liste_cours.append({
                "SYMBOL": symbol,
                "ACTUEL": cours,
                "M-6": cours_prec,
                "VAR" : f'{var}%',
                "SIXMOISPREC": sixmois_prec
            })

        macro = pd.DataFrame(liste_cours)
        macro.set_index('SYMBOL', inplace=True)
        return macro


    def KPI_1year(self):
        liste_cours = list()
        for symbol, asset_dataframe in self._selected_dataframes.items():
            try:
                asset_dataframe_resampled = Transform(asset_dataframe).resample()
                close_columns = [col for col in asset_dataframe_resampled.columns if 'Close' in col]
                if close_columns:
                    cours = round(asset_dataframe[close_columns].iloc[-1].values.sum(),2)
                    cours_prec = round(asset_dataframe_resampled[close_columns].iloc[-13].values.sum(),2)
                    var = round(((cours - cours_prec)/ cours_prec)*100,2)
                    annee_prec = datetime.now() - timedelta(days=365)
                    annee_prec = pd.to_datetime(annee_prec)
                    asset_dataframe.index = pd.to_datetime(asset_dataframe.index)
                    s_annee_prec = asset_dataframe[asset_dataframe.index >= annee_prec]
                    s_annee_prec_resampled = asset_dataframe_resampled[asset_dataframe_resampled.index>=annee_prec]
                    variation = s_annee_prec_resampled[close_columns].pct_change().dropna()
                    renta_moy = variation.values.mean()
                    renta_moy = round(renta_moy*100,2)
                    risque_moy = variation.values.std()
                    risque_moy = round(risque_moy*100,2)
                    line = [str(val) for val in s_annee_prec[close_columns].values.flatten()]
                    liste_cours.append({"SYMBOLE": symbol, "ACTUEL": f'{cours}', "N-1": f'{cours_prec}', "VAR": f'{var}%', "RENTABILITÉ": f'{renta_moy}%', "VOLATILITÉ": f'{risque_moy}%', "VISION":line})
            except FileNotFoundError:
                continue
            except Exception:
                continue
        macro = pd.DataFrame(liste_cours)
        macro.set_index('SYMBOLE', inplace=True)
        return macro
     
    def KPI_5year(self):
        liste_cours = list()
        for symbol, asset_dataframe in self._selected_dataframes.items():
            try:
                asset_dataframe_resampled = Transform(asset_dataframe).resample()
                close_columns = [col for col in asset_dataframe_resampled.columns if 'Close' in col]
                if close_columns:
                    cours = round(asset_dataframe[close_columns].iloc[-1].values.sum(),2)
                    start_date = datetime.now() - timedelta(days=365*5)
                    s_cinq_ans = asset_dataframe_resampled[asset_dataframe_resampled.index>=start_date]
                    cours_prec = round(s_cinq_ans[close_columns].iloc[0].values.sum(),2)
                    var = round(((cours - cours_prec)/ cours_prec)*100,2)
                    variation = s_cinq_ans[close_columns].pct_change().dropna()
                    renta_moy = variation.values.mean()
                    renta_moy = round(renta_moy*100,2)
                    risque_moy = variation.values.std()
                    risque_moy = round(risque_moy*100,2)
                    line = [str(val) for val in s_cinq_ans[close_columns].values.flatten()]
                    liste_cours.append({"SYMBOLE": symbol, "ACTUEL": f'{cours}', "N-5": f'{cours_prec}', "VAR": f'{var}%', "RENTABILITÉ": f'{renta_moy}%', "VOLATILITÉ": f'{risque_moy}%', "VISION":line})
            except FileNotFoundError:
                continue
            except Exception:
                continue
        macro = pd.DataFrame(liste_cours)
        macro.set_index('SYMBOLE', inplace=True)
        return macro