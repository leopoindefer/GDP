import pandas as pd
from scipy.stats import pearsonr
from .asset_transform import Transform

class Comparaison(Transform):
    def __init__(self, selected_dataframes: dict) -> None:
        super().__init__(selected_dataframes)

    def combine(self, how='inner'):
        symbols = list(self._selected_dataframes.keys())
        columns = [f"Close_{symbol}" for symbol in symbols]

        dfs = [self._selected_dataframes[symbol].assign(date_column=self._selected_dataframes[symbol].index) for symbol in symbols]

        joined_df = pd.merge(dfs[0], dfs[-1], on='date_column', how=how)
        joined_df.set_index('date_column', inplace=True)

        X, Y = joined_df[columns[0]].tolist(), joined_df[columns[-1]].tolist()
        corr, _ = pearsonr(X, Y)

        return joined_df, corr
