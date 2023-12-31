import pandas as pd
from datetime import datetime, timedelta
from .asset_transform import Transform

class Analyse(Transform):
    def __init__(self, selected_dataframes:dict, dict_assets_names:dict, period:str):
        super().__init__(selected_dataframes)
        self._dict_assets_names = dict_assets_names
        self._period = period

    def KPI(self):
        if self._period == "1 mois":
            liste_cours = []
            for symbol, asset_dataframe in self._selected_dataframes.items():
                try:
                    s = pd.DataFrame(asset_dataframe)
                    s.index = pd.to_datetime(s.index)
                    close_columns = [col for col in s.columns if 'Close' in col]
                    cours = round(s[close_columns].iloc[-1].values.sum(),2)
                    max_date = pd.to_datetime(s.index[-1])
                    mois_prec = pd.to_datetime(max_date - timedelta(days=31))
                    s_mois_prec = s[s.index>=mois_prec]
                    cours_prec = round(s_mois_prec[close_columns].iloc[0],2)
                    cours_prec = float(cours_prec)
                    var = round(((cours - cours_prec)/ cours_prec)*100,2)
                    var = float(var)
                    variation = s_mois_prec[close_columns].pct_change().dropna()
                    renta_moy = var
                    risque_moy = variation.values.std()
                    risque_moy = round(risque_moy*100,2)
                    line = [str(val) for val in s_mois_prec[close_columns].values.flatten()]
                    name = [str(valeur) for cle, valeur in self._dict_assets_names.items() if cle == symbol][0]

                    liste_cours.append({
                        "SYMBOLE": symbol,
                        "NOM" : f'{name}',
                        "ACTUEL": f'{cours}',
                        "M-1": f'{cours_prec}',
                        "VAR" : f'{var}%',
                        "RENTABILITÉ": f'{renta_moy}%', 
                        "VOLATILITÉ": f'{risque_moy}%',
                        "VISION":line
                    })
                
                except FileNotFoundError:
                    continue
                except Exception:
                    continue

            macro = pd.DataFrame(liste_cours)
            macro.set_index('SYMBOLE', inplace=True)
            return macro
        else:   
            if self._period == "6 mois":
                time_delta = timedelta(days=183)
            elif self._period == "1 an":
                time_delta = timedelta(days=365)
            elif self._period == "5 ans":
                time_delta = timedelta(days=365*5)
            liste_cours = []
            for symbol, asset_dataframe in self._selected_dataframes.items():
                try: 
                    s = pd.DataFrame(asset_dataframe)
                    s.index = pd.to_datetime(s.index)
                    s_resampled = s.resample("MS").first()
                    close_columns = [col for col in s_resampled.columns if 'Close' in col]
                    cours = round(s[close_columns].iloc[-1].values.sum(),2)
                    cours_prec = round(s_resampled[close_columns].iloc[-7].values.sum(),2)
                    var = round(((cours - cours_prec)/ cours_prec)*100,2)
                    max_date = pd.to_datetime(s.index[-1])
                    sixmois_prec = pd.to_datetime(max_date - time_delta)
                    s_mois_prec = s[s.index>=sixmois_prec]
                    s_mois_prec_resampled = s_resampled[s_resampled.index>=sixmois_prec]
                    variation = s_mois_prec_resampled[close_columns].pct_change().dropna()
                    renta_moy = variation.values.mean()
                    renta_moy = round(renta_moy*100,2)
                    risque_moy = variation.values.std()
                    risque_moy = round(risque_moy*100,2)
                    line = [str(val) for val in s_mois_prec[close_columns].values.flatten()]
                    name = [str(valeur) for cle, valeur in self._dict_assets_names.items() if cle == symbol][0]

                    liste_cours.append({
                        "SYMBOLE": symbol,
                        "NOM" : f'{name}',
                        "ACTUEL": f'{cours}',
                        "M-6": f'{cours_prec}',
                        "VAR" : f'{var}%',
                        "RENTABILITÉ": f'{renta_moy}%', 
                        "VOLATILITÉ": f'{risque_moy}%',
                        "VISION":line
                    })

                except FileNotFoundError:
                    continue
                except Exception:
                    continue

            macro = pd.DataFrame(liste_cours)
            macro.set_index('SYMBOLE', inplace=True)
            return macro