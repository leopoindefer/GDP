from statsmodels.tsa.arima.model import ARIMA
import pandas as pd

#ARIMA
def model_arima(df_arima):
        arima_shifted = df_arima.shift(2)/df_arima
        # Définir les différentes valeurs de p, d et q à tester
        p_values = range(0, 5)
        d_values = range(0, 5)
        q_values = range(0, 5)

        # Stocker les résultats de l'AIC pour chaque combinaison de paramètres
        aic_results = []

        for p in p_values:
                for d in d_values:
                        for q in q_values:
                                try:
                                        model = ARIMA(arima_shifted, order=(p,d,q)).fit()
                                        # Stocker l'AIC pour ce modèle
                                        aic_results.append((p,d,q,model.aic))
                                except:
                                        continue
        best_model = list(sorted(aic_results, key=lambda x: x[3])[0])[0:3]
        model_arima = ARIMA(arima_shifted, order=best_model).fit()
        predict_arima = model_arima.predict()
        return predict_arima