import streamlit as st
import pickle as pkle  
import math
import pandas as pd
from prophet import Prophet
import yfinance as yf

from model import model

st.set_page_config(
    page_title="GDP",
    page_icon="💯",
)

tab1, tab2 = st.tabs(["Analyser le marché", "Création de portefeuille"])

with tab1 :

    st.title("Gérer votre portefeuille avec l'IA")

    hide_st_style = """
                <style>
                #MainMenu {Visibility: hidden;}
                footer {visibility: hidden;}
                .bouton {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True) 

    st.header("Action à visualier")
    action = st.selectbox('Choisir une action', ('AAPL','META','AMZN','TSLA'))

    symb = action
    column = f"Close_{symb}"
    file = f"data/{symb}.csv"
    df = pd.read_csv(file)
    df = df.rename(columns = {column:'y',"Date":"ds"})
    df=df.loc[:,["ds","y"]]

    if action:
        try:
            predict = model(df)
            predict = predict.loc[:,["ds","yhat"]]
            SEC = df.join(predict, on="ds", how="left")
            predict = predict.rename(columns={"ds":"date","yhat":"prediction"})

            st.dataframe(SEC)
            st.line_chart(data=predict, x="date", y="prediction")
            st.dataframe(predict)

            col1, col2 = st.columns(2)
            with col1:
                montant = st.text_input('Montant à investir', 1000)
                start_value = df["y"].iloc[-1]
                end_value = predict["yhat"].iloc[-1]
                gap_indiv_value = (end_value - start_value)
                invest_part = montant/start_value

                ticker = yf.Ticker(symb)
                div_indiv = pd.DataFrame(ticker.dividends)
                div_indiv = div_indiv.iloc[-1].tolist()
                div_indiv = sum(div_indiv)*4
                div_indiv
                
            with col2:
                div = div_indiv * invest_part
                gap_value = gap_indiv_value * invest_part
                tRend = (div/montant)*100
                tRent = (div+gap_value)/montant*100
                mess = f'Taux de rendement de : {round(tRend,2)}%, Rendement de {round(div,2)}€ par actions\nTaux de rentabilité de : {round(tRent,2)}%, Rentabilité de {round(div + gap_value,2)}€ par actions'
                st.write(mess)

        except:
            st.error('pas de résultat')

with tab2 :
    st.header("Action à visualier")