import pandas as pd
import numpy as np
from prophet import Prophet
from prophet.diagnostics import performance_metrics

def prophet_model(df):
    m = Prophet()
    m.fit(df)
    future = m.make_future_dataframe(periods=365)
    forecast = m.predict(future)

    return forecast