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
            gap_indiv_value = (end_value - start_value)
            invest_part = float(montant/start_value)
            div = div_indiv * invest_part
            gap_value = gap_indiv_value * invest_part
            tRend = (div/montant)*100
            tRent = (div+gap_value)/montant*100
            if tRent<0:
                nb_part = f'<span style="color: #008000;">{round(invest_part,2)}</span>'
                tx_rendement = f'<span style="color: #008000;">{round(tRend,2)}%</span>'
                rendement = f'<span style="color: #008000;">{round(div,2)}€</span>'
                tx_rentabilite = f'<span style="color: #008000;">{round(tRent,2)}%</span>' 
                rentabilite = f'<span style="color: #008000;">{round(div + gap_value,2)}€</span>'
            elif tRent>=0:
                nb_part = f'<span style="color: #008000;">{round(invest_part,2)}</span>'
                tx_rendement = f'<span style="color: #008000;">{round(tRend,2)}%</span>'
                rendement = f'<span style="color: #008000;">{round(div,2)}€</span>'
                tx_rentabilite = f'<span style="color: #008000;">{round(tRent,2)}%</span>' 
                rentabilite = f'<span style="color: #008000;">{round(div + gap_value,2)}€</span>'
        except:
            print('pas de résultat')

        return  nb_part, tx_rendement, rendement, tx_rentabilite, rentabilite