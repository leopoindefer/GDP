import pandas as pd 

class Library:
    def __init__(self, indice:list, selected_assets:list) -> None:
        self._indice = indice
        self._selected_assets = selected_assets
        pass

    def get_assets(self):
        file_indice = f"data/indices/{self._indice}.csv"
        df_indice = pd.read_csv(file_indice, delimiter=";")
        assets_indice = df_indice['ticker'].tolist()
        return assets_indice

    def get_assets_all(self):
        symbol_txt = []
        symbol_nom = []
        dict_symb = {}
        for ind in self._indice:
            file_path = f"data/indices/{ind}.csv"
            indices_df = pd.read_csv(file_path, delimiter=";")
            symbols_list = indices_df["ticker"].tolist()
            symbols_name = indices_df["nom"].tolist()
            symbol_txt.extend(symbols_list)
            symbol_nom.extend(symbols_name)
            dict_symb[ind] = {"tickers": symbols_list, "noms": symbols_name}
            return symbol_txt

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