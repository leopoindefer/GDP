import streamlit as st

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

    assets = Library(indice,None).get_assets()
    dataframes = Library(None,assets).get_dataframes()
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
    assets_all = Library(liste_indice, None).get_assets_all()
    st.write(assets_all)

    with col_comp1:
        symb1 = st.selectbox('', assets)
    
    with col_comp2:
        asset2 = assets.copy()
        asset2.remove(symb1)
        symb2 = st.selectbox(' ', asset2)

    with col_comp3:
        st.write('')
        st.write("")
        run = st.button('Comparer')

    if run:
        comp1 = symb1
        comp2 = symb2
        assets_comp = [comp1, comp2]
        selected_dataframes = Library(None, assets_comp).get_dataframes()
        dataframes_resampled_comp = Transform(selected_dataframes).resample()
        compar_chart, corr = Comparaison(dataframes_resampled_comp).inner_combine()
        st.line_chart(compar_chart)

        mess_corr = f'Corrélation linéraire à : {round(corr*100,2)}%'
        st.write(mess_corr)


    st.markdown('----')
    