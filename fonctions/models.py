import pandas as pd
import numpy as np
from prophet import Prophet
import yfinance as yf

from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_predict
import statsmodels.api as sm

def prophet_model(df):
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    return forecast

def arima_model(df):
    df_shifted = df.shift(2)/df
    df_shifted = df_shifted.dropna()
    adf_shifted = adfuller(df_shifted)

    # Définir les différentes valeurs de p, d et q à tester
    p_values = range(8, 13)
    d_values = range(0, 5)
    q_values = range(8, 13)

    # Stocker les résultats de l'AIC pour chaque combinaison de paramètres
    aic_results = []

    # Boucler sur toutes les combinaisons possibles de p, d et q
    for p in p_values:
        for d in d_values:
            for q in q_values:
                try:
                    model = sm.tsa.ARIMA(df_shifted, order=(p,d,q)).fit()
                    # Stocker l'AIC pour ce modèle
                    aic_results.append((p,d,q,model.aic))
                except:
                    continue

    print('BEST MODEL', sorted(aic_results, key=lambda x: x[3])[0])