import streamlit as st
import pickle as pkle  
import math
import pandas as pd
from prophet import Prophet

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
            predict = predict.rename(columns={"ds":"date","yhat":"prediction"})

            col1, col2 = st.columns(2)

            with col1:

                st.line_chart(data=predict, x="date", y="prediction")

            with col2:
                st.dataframe(predict)

        except:
            st.error('pas de résultat')

with tab2 :
    st.header("Action à visualier")