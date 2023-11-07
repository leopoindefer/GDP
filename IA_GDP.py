import streamlit as st
import pickle as pkle  
import math
import pandas as pd
from prophet import Prophet
import yfinance as yf
import datetime
from datetime import date
import matplotlib as plt

from fonctions.prophet import prophet_model

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_predict
import statsmodels.api as sm

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

    #Preprocessing pour modele PROPHET
    df_prophet = df.rename(columns = {column:'y',"Date":"ds"})
    df_prophet = df_prophet.loc[:,["ds","y"]]

    #Preprocessing pour modele ARIMA
    df_arima = df
    df_arima['Date'] = pd.to_datetime(df_arima['Date'])
    df_arima.set_index('Date', inplace = True)
    df_arima = df_arima.loc[:,column]
    df_arima = pd.DataFrame(df_arima)
    df_arima.resample("MS").first()

    if action:
        with st.spinner('Chargement de la prédiction'):

            #PROPHET
            try:
                predict_prophet = prophet_model(df_prophet)
                predict_prophet = predict_prophet.loc[:,["ds","yhat"]]

                df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])
                predict_prophet['ds'] = pd.to_datetime(predict_prophet['ds'])
                ecart = df_prophet.set_index('ds').join(predict_prophet.set_index('ds'), how="left")
                ecart['se'] = ecart['y'] - ecart['yhat']
                sec = ecart.sum(axis=0)
                sec = sec.iloc[-1].tolist()**2
            except:
                st.error('pas de résultat pour PROPHET')

            #ARIMA
            try:
                model_arima = ARIMA(df_arima, order=(1,5,0)).fit()
                predict_arima = model_arima.predict()
                st.dataframe(predict_arima)
                
            except:
                st.error('pas de résultat pour ARIMA')

            predict_prophet = predict_prophet.rename(columns={"ds":"date","yhat":"prediction"})
            graph = ecart.loc[:,["y","yhat"]]
            graph = graph.rename(columns = {"y":'Reel',"yhat":"predicttion"})
            st.line_chart(data=graph)
            st.write(sec)

       
        col1, col2 = st.columns(2)
        with col1:
            montant = st.text_input('Montant à investir', 1000)
            duree = st.date_input("Jusqu'à quand ?", datetime.date(2024, 1, 1), min_value=pd.to_datetime(date.today()), max_value=pd.to_datetime(predict_prophet["date"].iloc[-1]))
            duree = pd.to_datetime(duree)
            montant = float(montant)
            start_value = df_prophet["y"].iloc[-1]
            end_date = predict_prophet[predict_prophet['date'] <= duree]
            end_value = end_date["prediction"].iloc[-1]
            gap_indiv_value = (end_value - start_value)
            invest_part = float(montant/start_value)
    
        with col2:

            try:
                ticker = yf.Ticker(symb)
                div_indiv = pd.DataFrame(ticker.dividends)
                div_indiv = div_indiv.iloc[-1].tolist()
                div_indiv = sum(div_indiv)*4
            except:
                st.error('dividende réinvesti')
                div_indiv = 0

            try:  
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