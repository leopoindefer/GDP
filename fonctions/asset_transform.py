import pandas as pd 
import numpy as np
from typing import TypeVar, Generic

class Transform():
    def __init__(self, selected_dataframes:dict) -> None:
        self._selected_dataframes = selected_dataframes
        pass

    def resample(self):
        dataframes_resampled = {}
        for symbol, df in self._selected_dataframes.items():
            df.index = pd.to_datetime(df.index)
            df = df.resample("MS").first()
            dataframes_resampled[symbol] = df 
        return dataframes_resampled