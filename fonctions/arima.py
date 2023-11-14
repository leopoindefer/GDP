import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

#ARIMA
def model_arima(df_arima):
        model_arima = ARIMA(df_arima, order=(1,5,0)).fit()
        predict_arima = model_arima.predict()
        return predict_arima