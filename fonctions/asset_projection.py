import pandas as pd
import yfinance as yf

class Projection():
    def __init__(self, montant, duree, asset, df, forecast):
        self._montant = montant
        self._duree = duree
        self._asset = asset
        self._df = df
        self._forecast = forecast

    def process_data(self):
        montant = float(self._montant)
        duree = pd.to_datetime(self._duree)
        confiance_pred = self._forecast[self._forecast["date"] == duree]
        confiance_pred = confiance_pred.loc[:,["yhat_lower","yhat_upper"]]
        return montant, duree, confiance_pred

    def get_dividends(self):
        try:
            ticker = yf.Ticker(self._asset)
            div_indiv = pd.DataFrame(ticker.dividends)
            div_indiv = div_indiv.iloc[-1].tolist()
            div_indiv = sum(div_indiv)*4
        except:
            div_indiv = 0
            print('dividende réinvesti')
        return div_indiv

    def get_values(self):
        montant, duree, confiance_pred = self.process_data()
        start_value = self._df["y"].iloc[-1]
        end_date = self._forecast[self._forecast['date'] <= duree]
        end_value = end_date["prediction"].iloc[-1]
        lower_endvalue = confiance_pred["yhat_lower"].iloc[-1]
        upper_endvalue = confiance_pred["yhat_upper"].iloc[-1]
        return start_value, end_value, lower_endvalue, upper_endvalue

    def get_gap_values(self):
        start_value, end_value, lower_endvalue, upper_endvalue = self.get_values()
        montant, duree, confiance_pred = self.process_data()
        div_indiv = self.get_dividends()
        invest_part = float(montant/start_value)
        div = div_indiv * invest_part
        gap_indiv_lower = (lower_endvalue - start_value)
        gap_indiv_upper = (upper_endvalue - start_value)
        gap_indiv_value = (end_value - start_value)
        gap_value_lower = gap_indiv_lower * invest_part
        gap_value_upper = gap_indiv_upper * invest_part
        gap_value = gap_indiv_value * invest_part
        return invest_part, div, gap_value, gap_value_lower, gap_value_upper

    def get_rentability(self):
        invest_part, div, gap_value, gap_value_lower, gap_value_upper = self.get_gap_values()
        montant, duree, confiance_pred = self.process_data()
        tRend = (div/montant)*100
        tRent = (div+gap_value)/montant*100
        tRent_lower = (div+gap_value_lower)/montant*100
        tRent_upper = (div+gap_value_upper)/montant*100
        return tRend, tRent, tRent_lower, tRent_upper

    def get_color(self, tRent):
        return 'red' if tRent < 0 else 'green'
    
    def unit_projection(self):
        tRend, tRent, tRent_lower, tRent_upper = self.get_rentability()
        invest_part, div, gap_value, gap_value_lower, gap_value_upper = self.get_gap_values()
        color_style = self.get_color(tRent)
        nb_part, tx_rendement, rendement, tx_rentabilite, rentabilite, tx_renta_lower, renta_lower, tx_renta_upper, renta_upper = (
            f':{color_style}[{round(invest_part, 2)}]',
            f':{color_style}[{round(tRend, 2)}%]',
            f':{color_style}[{round(div, 2)}€]',
            f':{color_style}[{round(tRent, 2)}%]',
            f':{color_style}[{round(div + gap_value, 2)}€]',
            f':{color_style}[{round(tRent_lower, 2)}%]',
            f':{color_style}[{round(div + gap_value_lower, 2)}€]',
            f':{color_style}[{round(tRent_upper, 2)}%]',
            f':{color_style}[{round(div + gap_value_upper, 2)}€]',
        )
        return nb_part, tx_rendement, rendement, tx_rentabilite, rentabilite, tx_renta_lower, renta_lower, tx_renta_upper, renta_upper