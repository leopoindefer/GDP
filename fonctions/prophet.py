import pandas as pd
import numpy as np
from prophet import Prophet

def prophet_model(df, symb):
    column = f"Close_{symb}"
    df = df.rename(columns = {column:'y',"Date":"ds"})
    df = df.loc[:,["ds","y"]]
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)

    return forecast