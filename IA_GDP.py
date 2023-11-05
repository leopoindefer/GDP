import streamlit as st
import pickle as pkle  
import math
import pandas as pd

from model import model

st.set_page_config(
    page_title="GDP",
    page_icon="💯",
)

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

col1, col2 = st.columns(2)

with col1:

    button = st.button('ESTIMER LE COURS DE L ACTION')
    if button:
        try:
            predict = model(df)
            st.dataframe(predict)
            st.sucess('des résultats')
        except:
            st.error('pas de résultat')

with col2:
    try:
        result = f'<span style="color: #7DCEA0;">{math.ceil(predict.iloc[-1]["yhat"])}€</span>'

        st.write(
            f'### Le cours de l action est estimé à {result}', unsafe_allow_html=True)
    except:
        pass
    
st.line_chart(data=predict, x="ds", y="yhat")