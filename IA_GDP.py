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
file = f"bdd/actions/{symb}.csv"
df = pd.read_csv(file)
df = df.rename(columns = {column:'y',"Date":"ds"})
df=df.loc[:,["ds","y"]]

model = model(df)
print(model)