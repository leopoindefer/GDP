import pandas as pd
from prophet import Prophet
import yfinance as yf

def model(df):
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    end_value = forecast["yhat"].iloc[-1]
    return end_value