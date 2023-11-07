from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_predict
import statsmodels.api as sm

def arima_model(df):
    df_shifted = df.shift(2)/df
    df_shifted = df_shifted.dropna()
    # Définir les différentes valeurs de p, d et q à tester

    # Stocker les résultats de l'AIC pour chaque combinaison de paramètres

    # Boucler sur toutes les combinaisons possibles de p, d et q
    model = sm.tsa.ARIMA(df_shifted, order=(5,1,0)).fit()
    # Stocker l'AIC pour ce modèle
    arima_pred = model.forecast()
    return arima_pred