import streamlit as st
import pickle as pkle  
import math
import pandas as pd
from prophet import Prophet
import yfinance as yf
import datetime
from datetime import date

from model import model

st.set_page_config(
    page_title="GDP",
    page_icon="💯",
)

st.title("Gérer votre portefeuille avec l'IA")

tab1, tab2 = st.tabs(["Analyser le marché", "Création de portefeuille"])

with tab1 :

    hide_st_style = """
                <style>
                #MainMenu {Visibility: hidden;}
                footer {visibility: hidden;}
                .bouton {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True) 

    st.header("Action à visualiser")
    action = st.selectbox('Choisir une action', ('AAPL','META','AMZN','TSLA'))

    symb = action
    column = f"Close_{symb}"
    file = f"data/{symb}.csv"
    df = pd.read_csv(file)
    df = df.rename(columns = {column:'y',"Date":"ds"})
    df=df.loc[:,["ds","y"]]

    if action:
        with st.spinner('Chargement de la prédiction'):

            try:
                predict = model(df)
                predict = predict.loc[:,["ds","yhat"]]

                df['ds'] = pd.to_datetime(df['ds'])
                predict['ds'] = pd.to_datetime(predict['ds'])
                ecart = df.set_index('ds').join(predict.set_index('ds'), how="left")
                ecart['se'] = ecart['y'] - ecart['yhat']
                sec = ecart.sum(axis=0)
                sec = sec.iloc[-1].tolist()**2

                predict = predict.rename(columns={"ds":"date","yhat":"prediction"})

                st.line_chart(data=predict, x="date", y="prediction")
                st.write(sec)

            except:
                st.error('pas de résultat')

        try:
            col1, col2 = st.columns(2)
            with col1:

                montant = st.text_input('Montant à investir', 1000)
                duree = st.date_input("Jusqu'à quand ?", datetime.date(2024, 1, 1), min_value=pd.to_datetime(date.today()), max_value=pd.to_datetime(predict["date"].iloc[-1]))
                duree = pd.to_datetime(duree)
                montant = float(montant)
                start_value = df["y"].iloc[-1]
                end_date = predict[predict['date'] <= duree]
                end_value = end_date["prediction"].iloc[-1]
                gap_indiv_value = (end_value - start_value)
                invest_part = float(montant/start_value)

                ticker = yf.Ticker(symb)
                div_indiv = pd.DataFrame(ticker.dividends)
                div_indiv = div_indiv.iloc[-1].tolist()
                div_indiv = sum(div_indiv)*4
        except:
            st.error('pas de résultat')

        try:      
            with col2:
                div = div_indiv * invest_part
                gap_value = gap_indiv_value * invest_part
                tRend = (div/montant)*100
                tRent = (div+gap_value)/montant*100
                mess = f'Nombre d action acheté : {round(invest_part,2)}'
                mess1 = f'Taux de rendement de : {round(tRend,2)}%, Rendement de {round(div,2)}€'
                mess2 = f'Taux de rentabilité de : {round(tRent,2)}%, Rentabilité de {round(div + gap_value,2)}€'
                st.write(mess)
                st.write(mess1)
                st.write(mess2)

        except:
            st.error('pas de résultat')

with tab2 :
    st.header("Créer votre portefeuille")