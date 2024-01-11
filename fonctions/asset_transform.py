import pandas as pd

class Transform():
    def __init__(self, selected_dataframes: dict) -> None:
        self._selected_dataframes = selected_dataframes

    def resample(self):
        dataframes_resampled = {symbol: df.set_index(pd.to_datetime(df.index)).resample("MS").first() for symbol, df in self._selected_dataframes.items()}
        return dataframes_resampled
    
    def __str__(self) -> str:
        return f"{self._selected_dataframes.keys()} est rééchantilloné à la fréquence mensuelle"