import streamlit as st
import pandas as pd

from fonctions.asset_database import Library
from fonctions.asset_transform import Transform
from fonctions.asset_analyzer import Analyse
from fonctions.asset_comparaison import Comparaison
from fonctions.asset_prophet import Prediction
from fonctions.asset_projection import Projection
from fonctions.asset_optimizer import Optimize

st.set_page_config(
    page_title="GDP",
    page_icon="💯",
)

st.title("Gérer votre portefeuille avec l'IA")

tab1, tab2, tab3 = st.tabs(["Analyser le marché", "Prédiction de performance", "Création de portefeuille"])

with tab1 :
    hide_st_style = """
                <style>
                MainMenu {Visibility: hidden;}
                footer {visibility: hidden;}
                .bouton {visibility: hidden;}
                </style>
                """
    st.markdown(hide_st_style, unsafe_allow_html=True) 

    liste_indice = ["CAC40", "DOWJONES", "NASDAQ100", "S&P500", "SBF120"]

    col_vision1, col_vision2, col_vision3 = st.columns((2,3,5))
    with col_vision1:
        periode = st.selectbox("Période d'analyse", ["1 mois","6 mois","1 an","5 ans"])
    with col_vision2:
        indice = st.selectbox("Indice", liste_indice)
    with col_vision3:
        st.write("")

    assets = Library(None, indice,None).get_assets()
    dataframes = Library(None, None,assets).get_dataframes()
    if periode == "1 mois":
        tableau = Analyse(dataframes).KPI_1month()
    elif periode == "6 mois":
        tableau = Analyse(dataframes).KPI_6month()
    elif periode == "1 an":
        tableau = Analyse(dataframes).KPI_1year()
    elif periode == "5 ans":
        tableau = Analyse(dataframes).KPI_5year()
    st.dataframe(tableau.style.applymap(lambda x: 'color: red' if any('-' in words for words in x.split()) else 'color: green',subset = ['VAR']), column_config={"VISION": st.column_config.LineChartColumn(
        "VISION", y_min=0, y_max=200)})
    

    col1_info, col2_info = st.columns((1, 8))
    with col1_info:
        info_button = st.button("ℹ️")

    with col2_info:
        if info_button:
            st.info('Rentabilité et volatilité mensuelle')

    st.markdown('----')

    st.header("Comparer des actions")
    col_comp1, col_comp2, col_comp3 = st.columns(3)
    assets_all, dict_assets_names = Library(None, liste_indice, None).get_assets_name()
    with col_comp1:
        symb1 = st.selectbox('', assets_all)
    
    with col_comp2:
        asset2 = assets_all.copy()
        asset2.remove(symb1)
        symb2 = st.selectbox(' ', asset2)

    with col_comp3:
        st.write('')
        st.write("")
        run = st.button('Comparer')

    comp1 = [cle for cle, valeur in dict_assets_names.items() if valeur == symb1]
    comp2 = [cle for cle, valeur in dict_assets_names.items() if valeur == symb2]
    
    if run:
        assets_comp = [comp1, comp2]
        assets_comp = sum(assets_comp, [])
        selected_dataframes = Library(None, None, assets_comp).get_dataframes()
        dataframes_resampled_comp = Transform(selected_dataframes).resample()
        compar_chart, corr = Comparaison(dataframes_resampled_comp).inner_combine()
        st.line_chart(compar_chart)

        st.write(f'Corrélation linéraire à : {round(corr*100,2)}%')

    st.markdown('----')

with tab2:

    st.header("Action à visualiser")
    asset = st.selectbox('Choisir une action', assets_all)
    asset = [cle for cle, valeur in dict_assets_names.items() if valeur == asset]
    asset_dataframe = Library(None, None, asset).get_dataframes()
    df_prophet,forecast, mse_prophet, graph_forecast = Prediction(asset_dataframe).forecast()
    st.line_chart(data=graph_forecast)
    st.write("PROPHET MSE:")
    st.write(round(mse_prophet,2))
    
    col1, col2 = st.columns(2)
    with col1:
        montant = st.text_input('Montant à investir', 1000)
    with col2:
        duree = st.date_input("Jusqu'à quand ?", pd.to_datetime(forecast["date"].iloc[-1]), min_value=pd.to_datetime(df_prophet["ds"].iloc[0]), max_value=pd.to_datetime(forecast["date"].iloc[-1]))
    try :
        nb_part, tx_rendement, rendement, tx_rentabilite, rentabilite, tx_renta_lower, renta_lower, tx_renta_upper, renta_upper = Projection(montant, duree, asset, df_prophet, forecast).unit_projection()
        st.write(f'Nombre d action acheté : {nb_part}', unsafe_allow_html=True)
        st.write(f'Taux de rendement de : {tx_rendement}, Rendement de {rendement}', unsafe_allow_html=True)
        st.write(f'Taux de Rentabilité de : {tx_rentabilite}, Rentabilité de {rentabilite}', unsafe_allow_html=True)
        st.write(f'Intervalle de confiance de rentabilité : [{renta_lower} : {renta_upper}]', unsafe_allow_html=True)
    except:
        st.error("Pas de projection disponible")

with tab3 : 
    st.header("Composer votre portefeuille")
    portefeuille = st.multiselect("Choisissez vos actions", assets_all)
    nb_acts = len(portefeuille)
    list_assets = []
    for actions in portefeuille:
        [list_assets.append(cle) for cle, valeur in dict_assets_names.items() if valeur == actions]

    calcul = st.button('Calculer')
    if calcul:
         with st.spinner('Chargement du calcul'):
             
            #try:

                if nb_acts <= 4:
                    portfolio_dataframes = Library(None, None, list_assets).get_dataframes()
                    merged_df = Optimize(list_assets, nb_acts, portfolio_dataframes).process_data()
                    st.write(merged_df)
                    st.subheader('Frontière efficiente')
                    st.scatter_chart(merged_df, x='Volatilité', y='Rentabilité')
                    #st.dataframe(merged_df, hide_index=True)
                    st.subheader('Portefeuille efficient pour :')
                    RisqueFaible, RisqueMoyen, RisqueEleve, RisqueTresEleve = Optimize(list_assets, nb_acts, merged_df).get_optimum()
                    col_result1, col_result2, col_result3, col_result4 = st.columns(4)
                    with col_result1:
                        st.write("Risque faible")
                        try :
                            st.dataframe(RisqueFaible)
                        except:
                            st.error("Aucun")

                    with col_result2:
                        st.write("Risque moyen")
                        try:
                            st.dataframe(RisqueMoyen)
                        except:
                            st.error("Aucun")

                    with col_result3:
                        st.write("Risque élevé")
                        try:
                            st.dataframe(RisqueEleve)
                        except:
                            st.error("Aucun")

                    with col_result4:
                        st.write("Risque très élevé")
                        try:
                            st.dataframe(RisqueTresEleve)
                        except:
                            st.error("Aucun")

                else:
                    mess_gdp = f"Création de portefeuille pas encore disponible pour {nb_acts}"
                    st.write(mess_gdp)
            #except:
                #st.error("Pas de portefeuille possible")