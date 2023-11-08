import streamlit as st
import pickle as pkle  
import math
import pandas as pd
from prophet import Prophet
import yfinance as yf
import datetime
from datetime import date
import matplotlib as plt
from scipy.stats import pearsonr

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
    file = f"data/actions/{symb}.csv"
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
                predict_arima = pd.DataFrame(model_arima.resid())
                st.dataframe(predict_arima)
                
            except:
                st.error('pas de résultat pour ARIMA')

            predict_prophet = predict_prophet.rename(columns={"ds":"date","yhat":"prediction"})
            graph = ecart.loc[:,["y","yhat"]]
            graph = graph.rename(columns = {"y":'Reel',"yhat":"prediction"})
            st.line_chart(data=graph)
            st.write(round(sec,2))

       
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
    
    st.markdown('----')

    st.header("Comparer des actions ou indices")
    col_comp1, col_comp2, col_comp3 = st.columns(3)

    with col_comp1:
        action_comp1 = st.selectbox(' ', ('AAPL','META','AMZN','TSLA'))
        symb1 = action_comp1
        column1 = f"Close_{symb1}"
        file1 = f"data/actions/{symb1}.csv"
        df1 = pd.read_csv(file1)
        df1 = df1.loc[:,[column1, "Date"]]

    with col_comp2:
        action_comp2 = st.selectbox('', ('META','AMZN','TSLA','AAPL'))
        symb2 = action_comp2
        column2 = f"Close_{symb2}"
        file2 = f"data/actions/{symb2}.csv"
        df2 = pd.read_csv(file2)
        df2 = df2.loc[:,[column2, "Date"]]

    with col_comp3:
        st.write(' ')
        run = st.button('Comparer')

    if run:

        graph_comp = df1.set_index('Date').join(df2.set_index('Date'), how="left")
        st.line_chart(graph_comp)

        #coefficient de Pearson
        start_date1 = min(df1['Date'])
        start_date2 = min(df2["Date"])
        if start_date1 >= start_date2:
            start_date = start_date1
        else:
            start_date = start_date2
        start_date = pd.to_datetime(start_date)
        df1['Date'] = pd.to_datetime(df1['Date'])
        df2['Date'] = pd.to_datetime(df2['Date'])
        df1 = df1[df1.Date>=start_date]
        df2 = df2[df2.Date>=start_date]
        X = df1[column1].tolist()
        Y = df2[column2].tolist()
        corr, _ = pearsonr(X, Y)
        mess_corr = f'Corrélation linéraire à : {round(corr*100,2)}%'
        st.write(mess_corr)

    st.markdown('----')

with tab2 :
    st.header("Créer votre portefeuille")