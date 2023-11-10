import pandas as pd
from scipy.stats import pearsonr
import numpy as np

def Comparaison(symb1, symb2):    
    column1 = f"Close_{symb1}"
    file1 = f"data/actions/{symb1}.csv"
    df1 = pd.read_csv(file1)
    df1 = df1.loc[:,[column1, "Date"]]
    column2 = f"Close_{symb2}"
    file2 = f"data/actions/{symb2}.csv"
    df2 = pd.read_csv(file2)
    df2 = df2.loc[:,[column2, "Date"]]
    graph_comp = df1.set_index('Date').join(df2.set_index('Date'), how="left")
    start_date1 = min(df1['Date'])
    start_date2 = min(df2["Date"])
    if start_date1 >= start_date2:
        start_date = start_date1
    else:
        start_date = start_date2
    start_date = pd.to_datetime(start_date)
    df1['Date'] = pd.to_datetime(df1['Date'])
    df2['Date'] = pd.to_datetime(df2['Date'])
    df1 = df1[df1.Date>=start_date]
    df2 = df2[df2.Date>=start_date]
    X = df1[column1].tolist()
    Y = df2[column2].tolist()
    corr, _ = pearsonr(X, Y)
    return graph_comp, corr