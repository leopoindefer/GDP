import pandas as pd
import yfinance as yf

class Projection():
    def __init__(self, montant, duree, asset, df, forecast):
        self._montant = montant
        self._duree = duree
        self._asset = asset
        self._df = df
        self._forecast = forecast

    def unit_projection(self):
        montant = float(self._montant)
        duree = pd.to_datetime(self._duree)
        confiance_pred = self._forecast[self._forecast["date"] == duree]
        confiance_pred = confiance_pred.loc[:,["yhat_lower","yhat_upper"]]
        try:
            ticker = yf.Ticker(self._asset)
            div_indiv = pd.DataFrame(ticker.dividends)
            div_indiv = div_indiv.iloc[-1].tolist()
            div_indiv = sum(div_indiv)*4
        except:
            div_indiv = 0
            print('dividende réinvesti')

        try: 
            start_value = self._df["y"].iloc[-1]
            end_date = self._forecast[self._forecast['date'] <= duree]
            end_value = end_date["forecast"].iloc[-1]
            lower_endvalue = confiance_pred["yhat_lower"].iloc[-1]
            upper_endvalue = confiance_pred["yhat_upper"].iloc[-1]
            gap_indiv_lower = (lower_endvalue - start_value)
            gap_indiv_upper = (upper_endvalue - start_value)
            gap_indiv_value = (end_value - start_value)
            invest_part = float(montant/start_value)
            div = div_indiv * invest_part
            gap_value_lower = gap_indiv_lower * invest_part
            gap_value_upper = gap_indiv_upper * invest_part
            gap_value = gap_indiv_value * invest_part
            tRend = (div/montant)*100
            tRent = (div+gap_value)/montant*100
            tRent_lower = (div+gap_value_lower)/montant*100
            tRent_upper = (div+gap_value_upper)/montant*100
            if tRent<0:
                nb_part = f'<span style="color: #FF0000;">{round(invest_part,2)}</span>'
                tx_rendement = f'<span style="color: #008000;">{round(tRend,2)}%</span>'
                rendement = f'<span style="color: #FF0000;">{round(div,2)}€</span>'
                tx_rentabilite = f'<span style="color: #FF0000;">{round(tRent,2)}%</span>' 
                rentabilite = f'<span style="color: #FF0000;">{round(div + gap_value,2)}€</span>'
                tx_renta_lower = f'<span style="color: #FF0000;">{round(tRent_lower,2)}%</span>' 
                renta_lower = f'<span style="color: #FF0000;">{round(div + gap_value_lower,2)}€</span>'
                tx_renta_upper = f'<span style="color: #FF0000;">{round(tRent_upper,2)}%</span>' 
                renta_upper = f'<span style="color: #FF0000;">{round(div + gap_value_upper,2)}€</span>'
            elif tRent>=0:
                nb_part = f'<span style="color: #008000;">{round(invest_part,2)}</span>'
                tx_rendement = f'<span style="color: #008000;">{round(tRend,2)}%</span>'
                rendement = f'<span style="color: #008000;">{round(div,2)}€</span>'
                tx_rentabilite = f'<span style="color: #008000;">{round(tRent,2)}%</span>' 
                rentabilite = f'<span style="color: #008000;">{round(div + gap_value,2)}€</span>'
                tx_renta_lower = f'<span style="color: #008000;">{round(tRent_lower,2)}%</span>' 
                renta_lower = f'<span style="color: #008000;">{round(div + gap_value_lower,2)}€</span>'
                tx_renta_upper = f'<span style="color: #008000;">{round(tRent_upper,2)}%</span>' 
                renta_upper = f'<span style="color: #008000;">{round(div + gap_value_upper,2)}€</span>'
        except:
            print('pas de résultat')

        return invest_part