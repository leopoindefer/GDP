import pandas as pd 
from typing import TypeVar, Generic

class Library:
    def __init__(self, indice, selected_assets:list) -> None:
        self._indice = indice
        self._selected_assets = selected_assets
        pass

    def get_assets(self):
        file_indice = f"data/indices/{self._indice}.csv"
        df_indice = pd.read_csv(file_indice, delimiter=";")
        assets_indices = df_indice['ticker'].tolist()
        return assets_indices

    def get_dataframes(self):
        def load_data(symbol):
            try:
                data = pd.read_csv(f"data/actions/{symbol}.csv")
                data = data.set_index("Date").filter(like='Close')
                return data
            except Exception as e:
                print(f"Error loading data for {symbol}: {e}")
                return None

        dataframes = {symbol: load_data(symbol) for symbol in self._selected_assets}
        selected_dataframes = {symbol: df for symbol, df in dataframes.items() if df is not None}
        return selected_dataframes