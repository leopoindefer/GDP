import pandas as pd 

class Library:
    def __init__(self, len_asset:int, indice:list, selected_assets:list) -> None:
        self._indice = indice
        self._selected_assets = selected_assets
        self._len_asset = len_asset
        pass
    
    def get_assets(self):
        file_indice = f"data/indices/{self._indice}.csv"
        df_indice = pd.read_csv(file_indice, delimiter=";")
        assets_indice = df_indice['ticker'].tolist()
        return assets_indice
    
    def get_weights(self):
        file_poids = f"data/poids/{self._len_asset}.csv"
        combi_poids = pd.read_csv(file_poids)
        return combi_poids
    
    def get_assets_name(self):
        list_df = []
        for ind in self._indice:
            file_path = f"data/indices/{ind}.csv"
            df = pd.read_csv(file_path, delimiter=";")
            list_df.append(df)

        stacked_df = pd.concat(list_df, axis=0, ignore_index=True)
        dict_assets_names = {}
        for index, row in stacked_df.iterrows():
            cle = row[1]
            valeur = row[0]
            dict_assets_names[cle] = valeur

        stacked_df_concat = stacked_df.copy()
        stacked_df_concat["noms"] = stacked_df["ticker"] + " : " +stacked_df["nom"]
        stacked_df_concat.drop(columns={"nom"},inplace=True)
        dict_assets_names_concat = {}
        for index, row in stacked_df_concat.iterrows():
            cle = row[0]
            valeur = row[1]
            dict_assets_names_concat[cle] = valeur

        return list(dict_assets_names_concat.values()), dict_assets_names, dict_assets_names_concat
    
    def get_symbol(self):
        all_assets, dict_assets_names, dict_assets_names_concat = self.get_assets_name()
        list_symbols = []
        for actions in self._selected_assets:
            [list_symbols.append(cle) for cle, valeur in dict_assets_names_concat.items() if valeur == actions]
        return list_symbols
    
    def get_assets_all(self):
        dict_assets_names = self.get_assets_name()
        list_assets = [cle for cle, valeur in dict_assets_names.items() if valeur == self._selected_assets]
        return list_assets
    
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