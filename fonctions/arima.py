import pandas as pd
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_predict
import statsmodels.api as sm

#ARIMA
def ARIMA(df_arima):
        predict_arima = ARIMA(df_arima, order=(1,5,0)).fit()
        summary = pd.DataFrame(predict_arima.summary())
        return summary