import pandas as pd

def CDP(portefeuille: list): 
    for acts in portefeuille:
        close_columns = [col for col in acts.columns if 'Close' in col]
        acts = acts.set_index("Date")
        if close_columns:
            acts = acts.loc[:,close_columns]
            df_ptf = pd.merge(acts)
            pd.DataFrame(df_ptf, inplace=True)
    return df_ptf