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
liste_indice = ["CAC40", "DOWJONES", "NASDAQ100", "S&P500", "SBF120"]
assets_all, dict_assets_names, dict_assets_names_concat = Library(None, liste_indice, None).get_assets_name()

with tab1 :
    hide_st_style = """
                <style>
                MainMenu {Visibility: hidden;}
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
    with col_vision3:
        st.write("")

    assets = Library(None, indice,None).get_assets()
    dataframes = Library(None, None,assets).get_dataframes()
    tableau = Analyse(dataframes, dict_assets_names, periode).KPI()
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
    with col_comp1:
        symb1 = st.selectbox('', assets_all,index=None,placeholder="Action 1")
    
    with col_comp2:
        symb2 = st.selectbox(' ', assets_all,index=None,placeholder="Action 2")

    with col_comp3:
        st.write('')
        st.write("")
        run = st.button('Comparer')

    try:
        if run:
            list_asset_comp = [symb1,symb2]
            assets_comp = Library(None,liste_indice,list_asset_comp).get_symbol()
            selected_dataframes = Library(None, None, assets_comp).get_dataframes()
            dataframes_resampled_comp = Transform(selected_dataframes).resample()
            compar_chart, corr = Comparaison(dataframes_resampled_comp).inner_combine()
            st.line_chart(compar_chart)

            st.write(f'Corrélation linéraire à : {round(corr*100,2)}%')
    except:
        st.error("Comparaison impossible")

    st.markdown('----')

with tab2:
    
    assets_viz = []
    st.header("Action à visualiser")
    col1_viz,col2_viz = st.columns((8,1))
    with col1_viz:
        asset = st.selectbox('Choisir une action', assets_all, index=None,placeholder="Action")
    with col2_viz:
        st.write("   ")
        st.write("     ")
        search_button = st.button("🔎")
    if search_button:
        assets_viz.append(asset)
        list_symbol = Library(None,liste_indice,assets_viz).get_symbol()
        asset_dataframe = Library(None, None, assets_viz).get_dataframes()
        st.write(assets_viz)
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

    calcul = st.button('Optimiser mon portefeuille')
    if calcul:
         with st.spinner('Chargement du calcul'):
            nb_acts = len(portefeuille)
             
            try:

                if nb_acts <= 4:
                    list_assets = Library(None,liste_indice,portefeuille).get_symbol()
                    portfolio_dataframes = Library(None, None, list_assets).get_dataframes()
                    merged_df = Optimize(list_assets, nb_acts, portfolio_dataframes).process_data()
                    st.subheader('Frontière efficiente')
                    st.scatter_chart(merged_df, x='Volatilité', y='Rentabilité')
                    st.subheader('Portefeuille efficient pour :')
                    RisqueFaible, RisqueMoyen, RisqueEleve, RisqueTresEleve = Optimize(list_assets, nb_acts, portfolio_dataframes).get_optimum()
                    col_result1, col_result2, col_result3, col_result4 = st.columns(4)
                    with col_result1:
                        st.write("Risque faible")
                        try :
                            st.dataframe(RisqueFaible)
                        except:
                            st.write("Aucun")

                    with col_result2:
                        st.write("Risque moyen")
                        try:
                            st.write(RisqueMoyen)
                        except:
                            st.write("Aucun")

                    with col_result3:
                        st.write("Risque élevé")
                        try:
                            st.write(RisqueEleve)
                        except:
                            st.write("Aucun")

                    with col_result4:
                        st.write("Risque très élevé")
                        try:
                            st.write(RisqueTresEleve)
                        except:
                            st.write("Aucun")

                else:
                    mess_gdp = f"Création de portefeuille pas encore disponible pour {nb_acts}"
                    st.write(mess_gdp)
            except:
                st.error("Pas de portefeuille possible")