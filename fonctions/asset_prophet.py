import pandas as pd
import numpy as np
from prophet import Prophet
from prophet.diagnostics import performance_metrics
from .asset_transform import Transform

class Prediction(Transform):
    def __init__(self, selected_dataframes:dict) -> None:
        super().__init__(selected_dataframes)

    def forecast(self): 
        for symbol, df in self._selected_dataframes.items():
            column = f"Close_{symbol}"
            df["date_column"] = df.index
            df_prophet = df.rename(columns = {column:'y',"date_column":"ds"})
            df_prophet = df_prophet.loc[:,["ds","y"]]
            m = Prophet()
            m.fit(df_prophet)
            future = m.make_future_dataframe(periods=365)
            forecast = m.predict(future)

            forecast = forecast.loc[:,["ds","yhat", "yhat_lower", "yhat_upper"]]
            df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])
            forecast['ds'] = pd.to_datetime(forecast['ds'])
            loss_prophet = forecast.set_index('ds').join(df_prophet.set_index('ds'), how="left")
            loss_prophet = loss_prophet.loc[:,["y","yhat"]]
            loss_prophet['se'] = np.square(loss_prophet['y'] - loss_prophet['yhat'])
            mse_prophet = loss_prophet['se'].mean(axis=0)
            forecast = forecast.rename(columns={"ds":"date","yhat":"prediction"})
            graph_forecast = loss_prophet.loc[:,["y","yhat"]]
            graph_forecast = graph_forecast.rename(columns = {"y":'Reel',"yhat":"prediction"})

            return df_prophet,forecast, mse_prophet, graph_forecast
