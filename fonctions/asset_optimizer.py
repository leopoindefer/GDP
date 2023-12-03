import pandas as pd
import numpy as np
from .asset_transform import Transform

class Optimize():
    def __init__(self, selected_assets:list, len_assets:int, selected_dataframes:dict):
        self._selected_assets = selected_assets
        self._len_assets = len_assets
        self._selected_dataframes = selected_dataframes

    def process_data(self):
        dataframes = self._selected_dataframes.values()
        ptf_df = pd.concat(dataframes, axis=1, join='inner')
        ptf_df.index = pd.to_datetime(ptf_df.index)
        ptf_df = Transform(ptf_df).resample()

        file_poids = f"data/poids/{self._len_assets}.csv"
        combi_poids = pd.read_csv(file_poids)   
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
    
    def get_optimum(self):
        df_RisqueFaible, df_RisqueMoyen, df_RisqueEleve, df_RisqueTresEleve = self.risk_category()
        RisqueFaible = df_RisqueFaible.iloc[0]
        RisqueMoyen = df_RisqueMoyen.iloc[0]
        RisqueEleve = df_RisqueEleve.iloc[0]
        RisqueTresEleve = df_RisqueTresEleve.iloc[0]
        return RisqueFaible, RisqueMoyen, RisqueEleve, RisqueTresEleve
