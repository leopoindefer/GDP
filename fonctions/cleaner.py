import pandas as pd
import datetime
from datetime import date

def df_prophet(df):
    df_prophet = df.rename(columns = {column:'y',"Date":"ds"})
    df_prophet = df_prophet.loc[:,["ds","y"]]
    return df_prophet