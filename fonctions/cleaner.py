import pandas as pd
import datetime
from datetime import date

def df_prophet(df):
    df_prophet = df.rename(columns = {column:'y',"Date":"ds"})
    df_prophet = df_prophet.loc[:,["ds","y"]]
    df_prophet['ds'] = pd.to_datetime(df_prophet['ds'])
    return df_prophet