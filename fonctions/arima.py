import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

#ARIMA
def model_arima(df_arima):
        arima_shifted = df_arima.shift(2)/df_arima
        model_arima = ARIMA(arima_shifted, order=(1,5,0)).fit()
        predict_arima = model_arima.predict()
        return predict_arima