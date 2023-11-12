import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import date
from itertools import product

from fonctions.tableau import Tableau
from fonctions.comparaison import Comparaison
from fonctions.projection import Projection
from fonctions.cdp import CDP
from fonctions.prophet import prophet_model

st.set_page_config(
    page_title="GDP",
    page_icon="💯",
)

symbol_txt = ["AAPL", "TSLA", "AMZN", "META", "VLA.PA", "ALGRE.PA", "ALO.PA", "BNP.PA", "ALCYB.PA", "STLAP.PA", "AF.PA", "VIE.PA", "SAN.PA", "GLE.PA"]
symbol_dataframes = []  # Initialiser une liste pour stocker les DataFrames

for sym in symbol_txt:
    file_path = f"data/actions/{sym}.csv"
    df = pd.read_csv(file_path)
    symbol_dataframes.append(df)

symbol_dict = dict(zip(symbol_txt, symbol_dataframes))

st.title("Gérer votre portefeuille avec l'IA")

tab1, tab2, tab3 = st.tabs(["Analyser le marché", "Prédire", "Création de portefeuille"])

with tab1 :

    hide_st_style = """
                <style>
                #MainMenu {Visibility: hidden;}
                footer {visibility: hidden;}
                .bouton {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True) 
    
    macro = Tableau(symbol_txt, symbol_dataframes)
    st.dataframe(macro.style.applymap(lambda x: 'color: red' if any('-' in words for words in x.split()) else 'color: green',subset = ['VAR']), column_config={"VISION": st.column_config.LineChartColumn(
            "VISION", y_min=0, y_max=500)})

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
        st.write(f'Taux de rentabilité de : {tx_rentabilite}, Rentabilité de {rentabilite}', unsafe_allow_html=True)

with tab3 : 
    st.header("Composer votre portefeuille")

    symbol_df = {sym: pd.read_csv(f"data/actions/{sym}.csv") for sym in symbol_txt}

    portefeuille = st.multiselect("Choisissez vos actions", symbol_txt)
    nb_acts = len(portefeuille)
    # Utilisez le dictionnaire symbol_dataframes pour obtenir les DataFrames correspondants
    selected_dataframes = [symbol_df[sym].set_index("Date").filter(like='Close') for sym in portefeuille]

    # Fusionnez les DataFrames en utilisant pd.concat
    ptf_df = pd.concat(selected_dataframes, axis=1, join='inner')
    ptf_df.index = pd.to_datetime(ptf_df.index)
    ptf_df = ptf_df.resample('MS').first()

    #matrice de covariance
    variation = ptf_df.pct_change().dropna()
    cov_matrix = variation.cov()/4
    cov_matrix['sum'] = cov_matrix.sum(axis=1)

    calcul = st.button('Calculer')
    if calcul:
         with st.spinner('Chargement du calcul'):
            if nb_acts == 2:
                df_poids = f"data/poids/{nb_acts}.csv"
                matrice_poids = pd.read_csv(df_poids)

                # Multiplier chaque matrice de poids par la matrice de covariance
                matrices_resultats = [np.dot(matrice_poids.iloc[i], cov_matrix) for i in range(len(matrice_poids))]

                # Ajouter une colonne supplémentaire pour la somme de chaque ligne
                for i, matrice_resultat in enumerate(matrices_resultats):
                    df_poids.loc[i, 'portfolios_volatility'] = matrice_resultat.sum()
                combi_risque = np.sqrt(df_poids) * 100

                # Affichez le DataFrame fusionné
                st.write("DataFrame fusionné:")
                st.dataframe(combi_risque)

            else:
                st.write("Pas encore dispo")