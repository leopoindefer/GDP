import pandas as pd
import numpy as np
from .asset_database import Library
from .asset_transform import Transform

class Optimize(Transform):
    def __init__(self, selected_assets:list, len_assets:int, selected_dataframes:dict):
        super().__init__(selected_dataframes)
        self._selected_assets = selected_assets
        self._len_assets = len_assets

    def process_data(self):
        dataframes = self._selected_dataframes.values()
        ptf_df = pd.concat(dataframes, axis=1, join='inner')
        ptf_df.index = pd.to_datetime(ptf_df.index)
        ptf_df = ptf_df.resample('MS').first()

        combi_poids = Library(self._len_assets, None, None).get_weights()
        matrice_poids = combi_poids.values
        matrice_poids = matrice_poids[:,1:]
        combi_poids = pd.DataFrame(matrice_poids)

        #matrice de covariance
        variation = ptf_df.pct_change().dropna()
        cov_matrix = variation.cov()/self._len_assets
        cov_matrix['sum'] = cov_matrix.sum(axis=1)

        #Calcul de la rentabilité
        variation_list = variation.mean().tolist()
        combi_renta = combi_poids * np.array(variation_list)
        combi_renta['Rentabilité'] = combi_renta.sum(axis=1)*100

        # Multiplier chaque matrice de poids par la matrice de covariance
        matrices_resultats = [np.dot(matrice_poids[i], cov_matrix) for i in range(len(matrice_poids))]

        # Ajouter une colonne supplémentaire pour la somme de chaque ligne
        for i, matrice_resultat in enumerate(matrices_resultats):
            combi_poids.loc[i, 'Volatilité'] = matrice_resultat.sum()
        combi_risque = np.sqrt(combi_poids) * 100

        combi_poids = combi_poids.drop(columns=['Volatilité'])
        columns_mapping = {combi_poids.columns[i]: self._selected_assets[i] for i in range(len(self._selected_assets))}
        combi_poids.rename(columns=columns_mapping, inplace=True)

        # Fusionner combi_poids avec combi_renta
        merged_df = combi_poids.merge(combi_renta[['Rentabilité']], left_index=True, right_index=True)

        #Fusionner le résultat avec combi_risque
        merged_df = merged_df.merge(combi_risque[['Volatilité']], left_index=True, right_index=True)

        return merged_df

    def risk_category(self):
        #renta optimale pour risque donné
        merged_df = self.process_data()
        df_RisqueFaible = merged_df[merged_df['Volatilité'] < 3].sort_values(by='Rentabilité', ascending=False)
        df_RisqueMoyen = merged_df[(merged_df['Volatilité'] >= 3) & (merged_df['Volatilité'] <= 8)].sort_values(by='Rentabilité', ascending=False)
        df_RisqueEleve = merged_df[(merged_df['Volatilité'] > 8) & (merged_df['Volatilité'] <= 15)].sort_values(by='Rentabilité', ascending=False)
        df_RisqueTresEleve = merged_df[merged_df['Volatilité'] > 15].sort_values(by='Rentabilité', ascending=False)
        
        return df_RisqueFaible, df_RisqueMoyen, df_RisqueEleve, df_RisqueTresEleve
    
    def result_df(self, df):
        df = pd.DataFrame(df)
        for c in df.columns:
            c = c
        df = df.rename(columns={c:'Répartition'})
        mask = (df.index != 'Rentabilité') & (df.index != 'Volatilité')
        df.loc[mask, 'Répartition'] *= 100
        df.loc[:,'Répartition'] = df.loc[:,'Répartition'].round(2)
        df.loc[:,'Répartition'] = df.loc[:,'Répartition'].astype(str) + '%'
        return df

    def get_optimum(self):
        df_RisqueFaible, df_RisqueMoyen, df_RisqueEleve, df_RisqueTresEleve = self.risk_category()
        if df_RisqueFaible.empty == False:
            RisqueFaible = df_RisqueFaible.iloc[0]
            RisqueFaible = self.result_df(RisqueFaible)
        else: 
            RisqueFaible = "Aucun"
        if df_RisqueMoyen.empty == False:
            RisqueMoyen = df_RisqueMoyen.iloc[0]
            RisqueMoyen = self.result_df(RisqueMoyen)
        else:
            RisqueMoyen = "Aucun"
        if df_RisqueEleve.empty == False:
            RisqueEleve = df_RisqueEleve.iloc[0]
            RisqueEleve = self.result_df(RisqueEleve)
        else:
            RisqueEleve = "Aucun"
        if df_RisqueTresEleve.empty == False:
            RisqueTresEleve = df_RisqueTresEleve.iloc[0]
            RisqueTresEleve = self.result_df(RisqueTresEleve)
        else:
            RisqueTresEleve = "Aucun"
        return RisqueFaible, RisqueMoyen, RisqueEleve, RisqueTresEleve
