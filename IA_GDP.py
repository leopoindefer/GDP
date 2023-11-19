import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import date
import statistics

from fonctions.tableau import Tableau
from fonctions.comparaison import Comparaison
from fonctions.projection import Projection
from fonctions.cdp import CDP
from fonctions.prophet import prophet_model

st.set_page_config(
    page_title="GDP",
    page_icon="💯",
)

symbol_txt = []
symbol_nom = []
dict_symb = {}
liste_indice = ["CAC40", "DOWJONES", "NASDAQ100", "S&P500", "SBF120"]

#liste de toutes les actions
for ind in liste_indice:
    file_path = f"data/indices/{ind}.csv"
    indices_df = pd.read_csv(file_path, delimiter=";")
    symbols_list = indices_df["ticker"].tolist()
    symbols_name = indices_df["nom"].tolist()
    symbol_txt.extend(symbols_list)
    symbol_nom.extend(symbols_name)
    dict_symb[ind] = {"tickers": symbols_list, "noms": symbols_name}

st.title("Gérer votre portefeuille avec l'IA")

tab1, tab2, tab3, tab4 = st.tabs(["Analyser le marché", "Prédiction de performance", "Création de portefeuille","MEDAF"])

with tab1 :
    hide_st_style = """
                <style>
                #MainMenu {Visibility: hidden;}
                footer {visibility: hidden;}
                .bouton {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True) 
    
    col_vision1, col_vision2, col_vision3 = st.columns((2,3,5))
    with col_vision1:
        periode = st.selectbox("Période d'analyse", ["1 mois","6 mois","1 an","5 ans"])
    with col_vision2:
        indice = st.selectbox("Indice", liste_indice)
        file_indice = f"data/indices/{indice}.csv"
        df_indice = pd.read_csv(file_indice, delimiter=";")
        actions = df_indice['ticker'].tolist()
    with col_vision3:
        st.write("")
    try:
        macro = Tableau(periode, actions, dict_symb)
        st.dataframe(macro.style.applymap(lambda x: 'color: red' if any('-' in words for words in x.split()) else 'color: green',subset = ['VAR']), column_config={"VISION": st.column_config.LineChartColumn(
            "VISION", y_min=0, y_max=200)})
    except:
        st.write("pas de donnée")
    
    info_button_state = False

    col1_info, col2_info = st.columns((1, 8))
    with col1_info:
        info_button = st.button("ℹ️")

    with col2_info:
        if info_button:
            st.info('Rentabilité et volatilité mensuelle')

    st.markdown('----')

    st.header("Comparer des actions")
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
        try:
            graph_comp, corr = Comparaison(symb1,symb2)
            st.line_chart(graph_comp)

            mess_corr = f'Corrélation linéraire à : {round(corr*100,2)}%'
            st.write(mess_corr)
        except:
            st.write('Comparaison impossible')

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
    df_arima.index = pd.to_datetime(df_arima.index)
    df_arima = df_arima.resample("MS").first()

    if action:
        with st.spinner('Chargement de la prédiction'):

            result_prophet = prophet_model(df_prophet)
            predict_prophet = result_prophet.loc[:,["ds","yhat", "yhat_lower", "yhat_upper"]]

            df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])
            predict_prophet['ds'] = pd.to_datetime(predict_prophet['ds'])
            loss_prophet = predict_prophet.set_index('ds').join(df_prophet.set_index('ds'), how="left")
            loss_prophet = loss_prophet.loc[:,["y","yhat"]]
            loss_prophet['se'] = np.square(loss_prophet['y'] - loss_prophet['yhat'])
            mse_prophet = pd.DataFrame(loss_prophet['se'].mean(axis=0))
            mse_prophet = mse_prophet.iloc[-1].tolist()

            #ARIMA

            try:
                st.write("")
                #predict_arima = model_arima(df_arima)
                #predict_arima = pd.DataFrame(predict_arima)
                #loss_arima = predict_arima.join(df_arima, how="left")
                #loss_arima = loss_arima.rename(columns = {column:'y',"predicted_mean":"yhat"})
                #loss_arima['se'] = (loss_arima['y'] - loss_arima['yhat'])**2
                #mse_arima = loss_arima.mean(axis=0)
                #mse_arima = mse_arima.iloc[-1].tolist()
            except:
                st.error('pas de résultat pour ARIMA')

            predict_prophet = predict_prophet.rename(columns={"ds":"date","yhat":"prediction"})
            graph = loss_prophet.loc[:,["y","yhat"]]
            graph = graph.rename(columns = {"y":'Reel',"yhat":"prediction"})
            st.line_chart(data=graph)
            st.write("PROPHET MSE:")
            st.write(round(mse_prophet,2))
            st.dataframe(result_prophet)

        try:     
            col1, col2 = st.columns(2)
            with col1:
                montant = st.text_input('Montant à investir', 1000)
            with col2:
                duree = st.date_input("Jusqu'à quand ?", datetime.date(2024, 1, 1), min_value=pd.to_datetime(df_prophet["ds"].iloc[0]), max_value=pd.to_datetime(predict_prophet["date"].iloc[-1]))
            
            nb_part, tx_rendement, rendement, tx_rentabilite, rentabilite = Projection(montant, duree, symb, df_prophet, predict_prophet)
            st.write(f'Nombre d action acheté : {nb_part}', unsafe_allow_html=True)
            st.write(f'Taux de rendement de : {tx_rendement}, Rendement de {rendement}', unsafe_allow_html=True)
            st.write(f'Taux de Rentabilité de : {tx_rentabilite}, Rentabilité de {rentabilite}', unsafe_allow_html=True)
        except:
            st.write('Aucune estimation possible')

    duree = pd.to_datetime(duree)
    confiance_pred = result_prophet[result_prophet["Date"] == duree]
    st.dataframe(confiance_pred)


with tab3 : 
    st.header("Composer votre portefeuille")
    portefeuille = st.multiselect("Choisissez vos actions", symbol_txt)
    symbol_df = {}
    for symb in portefeuille:
        try:
            symbol_df[symb] = pd.read_csv(f"data/actions/{symb}.csv")
        except Exception as e:
            continue
    nb_acts = len(portefeuille)

    calcul = st.button('Calculer')
    if calcul:
         with st.spinner('Chargement du calcul'):

            selected_dataframes = [symbol_df[sym].set_index("Date").filter(like='Close') for sym in portefeuille]

            # Fusionnez les DataFrames en utilisant pd.concat
            ptf_df = pd.concat(selected_dataframes, axis=1, join='inner')
            ptf_df.index = pd.to_datetime(ptf_df.index)
            ptf_df = ptf_df.resample('MS').first()

            if nb_acts == 2:
                merged_df = CDP(portefeuille, nb_acts, ptf_df)
                st.write('Frontière efficiente')
                st.scatter_chart(merged_df, x='Volatilité', y='Rentabilité')
                st.write("Couple rentabilité/volatilité par combinaison de pondération")
                st.dataframe(merged_df, hide_index=True)
                df_RisqueFaible = merged_df[merged_df['Volatilité'] < 3].sort_values(by='Rentabilité', ascending=False)
                df_RisqueMoyen = merged_df[(merged_df['Volatilité'] >= 3) & (merged_df['Volatilité'] <= 8)].sort_values(by='Rentabilité', ascending=False)
                df_RisqueEleve = merged_df[(merged_df['Volatilité'] > 8) & (merged_df['Volatilité'] <= 15)].sort_values(by='Rentabilité', ascending=False)
                df_RisqueTresEleve = merged_df[merged_df['Volatilité'] > 15].sort_values(by='Rentabilité', ascending=False)

                try :
                    RisqueFaible = df_RisqueFaible.iloc[0]
                    st.write("Portefeuille efficient pour un risque faible :")
                    st.dataframe(RisqueFaible)
                except:
                    st.write("pas de risque faible")

                try:
                    RisqueMoyen = df_RisqueMoyen.iloc[0]
                    st.write("Portefeuille efficient pour un risque moyen :")
                    st.dataframe(RisqueMoyen)
                except:
                    st.write("pas de risque moyen")

                try:
                    RisqueEleve = df_RisqueEleve.iloc[0]
                    st.write("Portefeuille efficient pour un risque élevé :")
                    st.dataframe(RisqueEleve)
                except:
                    st.write("pas de risque élevé")

                try:
                    RisqueTresEleve = df_RisqueTresEleve.iloc[0]
                    st.write("Portefeuille efficient pour un risque très élevé :")
                    st.dataframe(RisqueTresEleve)
                except:
                    st.write("pas de risque très élevé")

            elif nb_acts == 3:
                merged_df = CDP(portefeuille, nb_acts, ptf_df)
                st.write('Frontière efficiente')   
                st.scatter_chart(merged_df, x='Volatilité', y='Rentabilité')
                st.write("Couple rentabilité/volatilité par combinaison de pondération")
                st.dataframe(merged_df, hide_index=True)
                df_RisqueFaible = merged_df[merged_df['Volatilité'] < 3].sort_values(by='Rentabilité', ascending=False)
                df_RisqueMoyen = merged_df[(merged_df['Volatilité'] >= 3) & (merged_df['Volatilité'] <= 8)].sort_values(by='Rentabilité', ascending=False)
                df_RisqueEleve = merged_df[(merged_df['Volatilité'] > 8) & (merged_df['Volatilité'] <= 15)].sort_values(by='Rentabilité', ascending=False)
                df_RisqueTresEleve = merged_df[merged_df['Volatilité'] > 15].sort_values(by='Rentabilité', ascending=False)

                try :
                    RisqueFaible = df_RisqueFaible.iloc[0]
                    st.write("Portefeuille efficient pour un risque faible :")
                    st.dataframe(RisqueFaible)
                except:
                    st.write("pas de risque faible")

                try:
                    RisqueMoyen = df_RisqueMoyen.iloc[0]
                    st.write("Portefeuille efficient pour un risque moyen :")
                    st.dataframe(RisqueMoyen)
                except:
                    st.write("pas de risque moyen")

                try:
                    RisqueEleve = df_RisqueEleve.iloc[0]
                    st.write("Portefeuille efficient pour un risque élevé :")
                    st.dataframe(RisqueEleve)
                except:
                    st.write("pas de risque élevé")

                try:
                    RisqueTresEleve = df_RisqueTresEleve.iloc[0]
                    st.write("Portefeuille efficient pour un risque très élevé :")
                    st.dataframe(RisqueTresEleve)
                except:
                    st.write("pas de risque très élevé")

            elif nb_acts == 4:
                merged_df = CDP(portefeuille, nb_acts, ptf_df)
                st.write('Frontière efficiente')   
                st.scatter_chart(merged_df, x='Volatilité', y='Rentabilité')
                st.write("Couple rentabilité/volatilité par combinaison de pondération")
                st.dataframe(merged_df, hide_index=True)
                df_RisqueFaible = merged_df[merged_df['Volatilité'] < 3].sort_values(by='Rentabilité', ascending=False)
                df_RisqueMoyen = merged_df[(merged_df['Volatilité'] >= 3) & (merged_df['Volatilité'] <= 8)].sort_values(by='Rentabilité', ascending=False)
                df_RisqueEleve = merged_df[(merged_df['Volatilité'] > 8) & (merged_df['Volatilité'] <= 15)].sort_values(by='Rentabilité', ascending=False)
                df_RisqueTresEleve = merged_df[merged_df['Volatilité'] > 15].sort_values(by='Rentabilité', ascending=False)

                try :
                    RisqueFaible = df_RisqueFaible.iloc[0]
                    st.write("Portefeuille efficient pour un risque faible :")
                    st.dataframe(RisqueFaible)
                except:
                    st.write("pas de risque faible")

                try:
                    RisqueMoyen = df_RisqueMoyen.iloc[0]
                    st.write("Portefeuille efficient pour un risque moyen :")
                    st.dataframe(RisqueMoyen)
                except:
                    st.write("pas de risque moyen")

                try:
                    RisqueEleve = df_RisqueEleve.iloc[0]
                    st.write("Portefeuille efficient pour un risque élevé :")
                    st.dataframe(RisqueEleve)
                except:
                    st.write("pas de risque élevé")

                try:
                    RisqueTresEleve = df_RisqueTresEleve.iloc[0]
                    st.write("Portefeuille efficient pour un risque très élevé :")
                    st.dataframe(RisqueTresEleve)
                except:
                    st.write("pas de risque très élevé")

            else:
                mess_gdp = f"Création de portefeuille pas encore disponible pour {nb_acts}"
                st.write(mess_gdp)

with tab4:
    st.write("Calcul MEDAF")
    col_medaf1, col_medaf2 = st.columns(2)
    with col_medaf1:
        indice = st.selectbox("marche", liste_indice)
        column_marche = f"Close_^FCHI"
        file_indice = f"data/indices/{indice}.csv"
        df_indice = pd.read_csv(file_indice, delimiter=";")
        actions = df_indice['ticker'].tolist()
        marche = pd.read_csv("data/indices/^FCHI.csv")
        marche["Date"] = pd.to_datetime(marche["Date"])
        marche = marche.set_index("Date")
        marche_resampled = marche.resample("M").first()
        close_columns = [col for col in marche_resampled.columns if 'Close' in col]
        variation_marche = marche_resampled[close_columns].pct_change().dropna()
        variation_marche["Datec"] = variation_marche.index
        
    with col_medaf2:
        actifs = st.selectbox("Action", actions)
        column_actif = f"Close_{actifs}"
        file_path = f"data/actions/{actifs}.csv"
        s = pd.read_csv(file_path)
        s["Date"] = pd.to_datetime(s["Date"])
        s = s.set_index("Date")
        s_resampled = s.resample("M").first()
        close_columns = [col for col in s_resampled.columns if 'Close' in col]
        variation = s_resampled[close_columns].pct_change().dropna()
        variation["Datec"] = variation.index

    actionsvsmarche = pd.merge(variation, variation_marche, on='Datec', how='inner')
    actionsvsmarche = actionsvsmarche.set_index("Datec")
    Beta = np.cov(actionsvsmarche[column_actif], actionsvsmarche[column_marche])[0][1] / np.var(actionsvsmarche[column_marche])
    st.write(Beta)