import pandas as pd
import numpy as np
from prophet import Prophet
import yfinance as yf

def prophet_model(df):
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)
    return forecast