import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import date

from fonctions.tableau import Tableau
from fonctions.comparaison import Comparaison
from fonctions.projection import Projection
from fonctions.cdp import CDP
from fonctions.prophet import prophet_model
from fonctions.arima import ARIMA

st.set_page_config(
    page_title="GDP",
    page_icon="💯",
)

symbol_txt = ["AAPL", "TSLA", "AMZN", "META", "PLUG", "PLTR", "AMD", "RIVN", "NVDA", "SOFI", "NIO", "MARA", "F", "DNA", "LCID", "LIFW", "U", "RLX", "PFE", "BAC", "STNE", "UBER", "AAL", "GRAB", "INTC", "VLA.PA", "ALGRE.PA", "ALO.PA", "BNP.PA", "ALCYB.PA", "STLAP.PA", "AF.PA", "VIE.PA", "SAN.PA", "GLE.PA"]
symbol_dataframes = []  # Initialiser une liste pour stocker les DataFrames

for sym in symbol_txt:
    file_path = f"data/actions/{sym}.csv"
    df = pd.read_csv(file_path)
    symbol_dataframes.append(df)

symbol_dict = dict(zip(symbol_txt, symbol_dataframes))

st.title("Gérer votre portefeuille avec l'IA")

tab1, tab2, tab3 = st.tabs(["Analyser le marché", "Prédiction de performance", "Création de portefeuille"])

with tab1 :

    hide_st_style = """
                <style>
                #MainMenu {Visibility: hidden;}
                footer {visibility: hidden;}
                .bouton {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True) 
    
    col_vision1, col_vision2 = st.columns((2,7))
    with col_vision1:
        periode = st.selectbox("Période d'analyse", ["1 mois","6 mois","1 an","5 ans"])
    with col_vision2:
        st.write("")
    
    macro = Tableau(periode, symbol_txt, symbol_dataframes)
    
    st.dataframe(macro.style.applymap(lambda x: 'color: red' if any('-' in words for words in x.split()) else 'color: green',subset = ['VAR']), column_config={"VISION": st.column_config.LineChartColumn(
            "VISION", y_min=0, y_max=500)})
    
    info_button_state = False

    col1_info, col2_info = st.columns((1, 8))
    with col1_info:
        info_button = st.button("ℹ️")

    with col2_info:
        if info_button:
            st.info('Rentabilité et volatilité mensuelle')

    st.markdown('----')

    st.header("Comparer des actions ou indices")
    col_comp1, col_comp2, col_comp3 = st.columns(3)

    with col_comp1:
        comp1 = st.selectbox('', symbol_txt)

    with col_comp2:
        symbol_txt2 = symbol_txt.copy()
        symbol_txt2.remove(comp1)
        comp2 = st.selectbox(' ', symbol_txt2)

    with col_comp3:
        st.write('')
        st.write("")
        run = st.button('Comparer')

    if run:
        symb1 = comp1
        symb2 = comp2
        graph_comp, corr = Comparaison(symb1,symb2)
        st.line_chart(graph_comp)

        mess_corr = f'Corrélation linéraire à : {round(corr*100,2)}%'
        st.write(mess_corr)

    st.markdown('----')
    
with tab2:

    st.header("Action à visualiser")
    action = st.selectbox('Choisir une action', symbol_txt)
    symb = action
    column = f"Close_{symb}"
    file = f"data/actions/{symb}.csv"
    df = pd.read_csv(file)

    #Preprocessing pour modele PROPHET
    #Mensuel
    #df_prophet = df.copy()
    #df_prophet['Date'] = pd.to_datetime(df_prophet['Date'])
    #df_prophet.set_index('Date', inplace = True) 
    #df_prophet = pd.DataFrame(df_prophet)
    #df_prophet = df_prophet.resample("MS").first()
    #df_prophet['Date'] = df_prophet.index
    #df_prophet = df_prophet.rename(columns = {column:'y',"Date":"ds"})
    #df_prophet = df_prophet.loc[:,["ds","y"]]

    #Journalier
    df_prophet = df.copy()
    df_prophet = df_prophet.rename(columns = {column:'y',"Date":"ds"})
    df_prophet = df_prophet.loc[:,["ds","y"]]

    #Preprocessing pour modele ARIMA
    df_arima = df
    df_arima['Date'] = pd.to_datetime(df_arima['Date'])
    df_arima.set_index('Date', inplace = True)
    df_arima = df_arima.loc[:,column]
    df_arima = pd.DataFrame(df_arima)
    df_arima = df_arima.resample("MS").first()

    if action:
        with st.spinner('Chargement de la prédiction'):

            #PROPHET
            try:
                predict_prophet = prophet_model(df_prophet)
                predict_prophet = predict_prophet.loc[:,["ds","yhat"]]

                df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])
                predict_prophet['ds'] = pd.to_datetime(predict_prophet['ds'])
                ecart = predict_prophet.set_index('ds').join(df_prophet.set_index('ds'), how="left")
                ecart['se'] = ecart['y'] - ecart['yhat']
                sec = ecart.sum(axis=0)
                sec = sec.iloc[-1].tolist()**2
            except:
                st.error('pas de résultat pour PROPHET')

            #ARIMA
            try:
                predict_arima = ARIMA(df_arima)
                st.dataframe(predict_arima)
            except:
                st.write("pas de résultat pour ARIMA")

            predict_prophet = predict_prophet.rename(columns={"ds":"date","yhat":"prediction"})
            graph = ecart.loc[:,["y","yhat"]]
            graph = graph.rename(columns = {"y":'Reel',"yhat":"prediction"})
            st.line_chart(data=graph)
            st.write(round(sec,2))
       
        col1, col2 = st.columns(2)
        with col1:
            montant = st.text_input('Montant à investir', 1000)
        with col2:
            duree = st.date_input("Jusqu'à quand ?", datetime.date(2024, 1, 1), min_value=pd.to_datetime(date.today()), max_value=pd.to_datetime(predict_prophet["date"].iloc[-1]))
        nb_part, tx_rendement, rendement, tx_rentabilite, rentabilite = Projection(montant, duree, symb, df_prophet, predict_prophet)
        st.write(f'Nombre d action acheté : {nb_part}', unsafe_allow_html=True)
        st.write(f'Taux de rendement de : {tx_rendement}, Rendement de {rendement}', unsafe_allow_html=True)
        st.write(f'Taux de Rentabilité de : {tx_rentabilite}, Rentabilité de {rentabilite}', unsafe_allow_html=True)

with tab3 : 
    st.header("Composer votre portefeuille")

    symbol_df = {sym: pd.read_csv(f"data/actions/{sym}.csv") for sym in symbol_txt}

    portefeuille = st.multiselect("Choisissez vos actions", symbol_txt)
    nb_acts = len(portefeuille)
    # Utilisez le dictionnaire symbol_dataframes pour obtenir les DataFrames correspondants
    selected_dataframes = [symbol_df[sym].set_index("Date").filter(like='Close') for sym in portefeuille]

    calcul = st.button('Calculer')
    if calcul:
         with st.spinner('Chargement du calcul'):

            # Fusionnez les DataFrames en utilisant pd.concat
            ptf_df = pd.concat(selected_dataframes, axis=1, join='inner')
            ptf_df.index = pd.to_datetime(ptf_df.index)
            ptf_df = ptf_df.resample('MS').first()

            if nb_acts == 2:
                merged_df = CDP(nb_acts, ptf_df)
                st.write('Frontière efficiente')
                st.scatter_chart(merged_df, x='Volatilité', y='Rentabilité')
                st.write("Couple rentabilité/volatilité par combinaison de pondération")
                st.dataframe(merged_df, hide_index=True)

            elif nb_acts == 3:
                merged_df = CDP(nb_acts, ptf_df)
                st.write('Frontière efficiente')   
                st.scatter_chart(merged_df, x='Volatilité', y='Rentabilité')
                st.write("Couple rentabilité/volatilité par combinaison de pondération")
                st.dataframe(merged_df, hide_index=True)

            elif nb_acts == 4:
                merged_df = CDP(nb_acts, ptf_df)
                st.write('Frontière efficiente')   
                st.scatter_chart(merged_df, x='Volatilité', y='Rentabilité')
                st.write("Couple rentabilité/volatilité par combinaison de pondération")
                st.dataframe(merged_df, hide_index=True)

            else:
                mess_gdp = f"Création de portefeuille pas encore disponible pour {nb_acts}"
                st.write(mess_gdp)