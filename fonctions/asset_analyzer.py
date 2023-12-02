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
        asset_dataframe_resampled = {}
        liste_symb = []
        liste_df = []
        for symbol, asset_dataframe in self._selected_dataframes.items():
            liste_symb.append(symbol)
            liste_df.append(asset_dataframe)
            try:
                for df in liste_df:
                    close_columns = [col for col in df.columns if 'Close' in col]
                    if close_columns:
                        df_resampled = Transform(df).resample().values()
                        df_resampled = pd.DataFrame(df_resampled)
                        cours = round(df[close_columns].iloc[-1].values.sum(),2)
                        cours_prec = round(df_resampled[close_columns].iloc[-7].values.sum(),2)
                        var = round(((cours - cours_prec)/ cours_prec)*100,2)
                        sixmois_prec = datetime.now() - timedelta(days=183)
                        sixmois_prec = pd.to_datetime(sixmois_prec)
                        df.index = pd.to_datetime(df.index)
                        s_six_mois_prec = df[df.index>=sixmois_prec]
                        s_six_mois_prec_resampled = df_resampled[df_resampled.index>=sixmois_prec]
                        variation = s_six_mois_prec_resampled[close_columns].pct_change().dropna()
                        renta_moy = variation.values.mean()
                        renta_moy = round(renta_moy*100,2)
                        risque_moy = variation.values.std()
                        risque_moy = round(risque_moy*100,2)
                        line = [str(val) for val in s_six_mois_prec[close_columns].values.flatten()]
                liste_cours.append({"SYMBOLE": liste_symb, "ACTUEL": f'{cours}', "M-6": f'{cours_prec}', "VAR": f'{var}%', "RENTABILITÉ": f'{renta_moy}%', "VOLATILITÉ": f'{risque_moy}%', "VISION":line})
            except FileNotFoundError:
                continue
            except Exception:
                continue
        macro = pd.DataFrame(liste_cours)
        #macro.set_index('SYMBOLE', inplace=True)
        return risque_moy

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