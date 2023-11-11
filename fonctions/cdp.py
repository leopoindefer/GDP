import pandas as pd

def CDP(dataframes):
    df_ptf = dataframes[0]
    for df in dataframes[1:]:
        close_columns = [col for col in df.columns if 'Close' in col]
        if close_columns:
            df = df.set_index("Date").loc[:, close_columns]
            df_ptf = pd.merge(df_ptf, df, how="inner", left_index=True, right_index=True)

    return df_ptf