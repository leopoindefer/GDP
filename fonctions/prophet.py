import pandas as pd
import numpy as np
from prophet import Prophet
import yfinance as yf

def prophet_model(df, symb):
    column = f"Close_{symb}"
    df = df.rename(columns = {column:'y',"Date":"ds"})
    df = df.loc[:,["ds","y"]]
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)

    #MSE
    df['ds'] = pd.to_datetime(forecast['ds'])
    forecast['ds'] = pd.to_datetime(forecast['ds'])
    ecart = df.set_index('ds').join(forecast.set_index('ds'), how="left")
    ecart['se'] = ecart['y'] - ecart['yhat']
    sec = ecart.sum(axis=0)
    sec = sec.iloc[-1].tolist()**2

    return forecast, sec