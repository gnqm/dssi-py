import argparse
import numpy as np
import pandas as pd

def load_data(data_path):
    df = pd.read_csv(data_path)
    return df

def save_data(data_path, df):
    df.to_csv(data_path.replace('.csv','_processed.csv'), index=False)
    return None

def log_txf(df, cols: list):
    for col in cols:
        df['log_'+col] = np.log(df[col]+1)
    return df

def remap_emp_length(x):
    if x in ['< 1 year','1 year','2 years']:
        return 'less_than_3yr'
    if x in ['3 years','4 years','5 years']:
        return '3_to_5yr'
    if x in ['6 years','7 years','8 years','9 years']:
        return '6_to_9yr'
    return 'more_than_9yr'

def preprocess(df):
    df = log_txf(df, ['annual_inc'])
    df['emp_len'] = df['emp_length'].map(remap_emp_length)
    return df

def run(data_path):
    df = load_data(data_path)
    df = preprocess(df)
    save_data(data_path, df)
    return df

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--data_path", type=str)
    args = argparser.parse_args()
    run(args.data_path)