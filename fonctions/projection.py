import pandas as pd
import yfinance as yf

def Projection(montant, duree, symb, df_model, prediction):
    montant = float(montant)
    duree = pd.to_datetime(duree)
    try:
        ticker = yf.Ticker(symb)
        div_indiv = pd.DataFrame(ticker.dividends)
        div_indiv = div_indiv.iloc[-1].tolist()
        div_indiv = sum(div_indiv)*4
    except:
        div_indiv = 0
        print('dividende réinvesti')

    try: 
        start_value = df_model["y"].iloc[-1]
        end_date = prediction[prediction['date'] <= duree]
        end_value = end_date["prediction"].iloc[-1]
        gap_indiv_value = (end_value - start_value)
        invest_part = float(montant/start_value)
        div = div_indiv * invest_part
        gap_value = gap_indiv_value * invest_part
        tRend = (div/montant)*100
        tRent = (div+gap_value)/montant*100
        nb_part = f'<span style="color: #FF0000;">{round(invest_part,2)}</span>'
        tx_rendement = f'<span style="color: #FF0000;">{round(tRend,2)}%</span>'
        rendement = f'<span style="color: #FF0000;">{round(div,2)}€</span>'
        tx_rentabilite = f'<span style="color: #FF0000;">{round(tRent,2)}%</span>' 
        rentabilite = f'<span style="color: #FF0000;">{round(div + gap_value,2)}€</span>'
    except:
        print('pas de résultat')
    return  nb_part, tx_rendement, rendement, tx_rentabilite, rentabilite
