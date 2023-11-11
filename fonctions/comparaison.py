import pandas as pd
from scipy.stats import pearsonr
import numpy as np

def Comparaison(symb1, symb2):    
    column1 = f"Close_{symb1}"
    file1 = f"data/actions/{symb1}.csv"
    df1 = pd.read_csv(file1, parse_dates=['Date'])

    column2 = f"Close_{symb2}"
    file2 = f"data/actions/{symb2}.csv"
    df2 = pd.read_csv(file2, parse_dates=['Date'])

    graph_comp = pd.merge(df1, df2, on='Date', how='inner')
    graph_comp = graph_comp.loc[:,["Date",column1,column2]]
    graph_comp.set_index("Date", inplace=True)

    X = graph_comp[column1].tolist()
    Y = graph_comp[column2].tolist()
    corr, _ = pearsonr(X, Y)
    
    return graph_comp, corr