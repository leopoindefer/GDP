import pandas as pd
from scipy.stats import pearsonr
from .asset_transform import Transform

class Comparaison(Transform):
    def __init__(self, selected_dataframes: dict) -> None:
        super().__init__(selected_dataframes)

    def inner_combine(self):
        symb = list()
        for symbol in self._selected_dataframes.keys():
            symb.append(symbol)
        symb1 = symb[0]
        column1 = f"Close_{symb1}"
        df1 = self._selected_dataframes[symb1]
        df1['date_column'] = df1.index
        
        symb2 = symb[-1]
        column2 = f"Close_{symb2}"
        df2 = self._selected_dataframes[symb2]
        df2['date_column'] = df2.index

        inner_join = pd.merge(df1, df2, on='date_column' ,how='inner')
        inner_join.set_index('date_column', inplace=True)

        X = inner_join[column1].tolist()
        Y = inner_join[column2].tolist()
        corr, _ = pearsonr(X, Y)

        return  inner_join, corr