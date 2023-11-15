import pandas as pd
import numpy as np

def CDP(portefeuille, nb_acts, ptf_df):
    file_poids = f"data/poids/{nb_acts}.csv"
    combi_poids = pd.read_csv(file_poids)   
    matrice_poids = combi_poids.values
    matrice_poids = matrice_poids[:,1:]
    combi_poids = pd.DataFrame(matrice_poids)

    #matrice de covariance
    variation = ptf_df.pct_change().dropna()
    cov_matrix = variation.cov()/nb_acts
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
    combi_poids.rename(columns={portefeuille})

    # Fusionner combi_poids avec combi_renta
    merged_df = combi_poids.merge(combi_renta[['Rentabilité']], left_index=True, right_index=True)

    #Fusionner le résultat avec combi_risque
    merged_df = merged_df.merge(combi_risque[['Volatilité']], left_index=True, right_index=True)
    
    return merged_df