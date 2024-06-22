from joblib import dump, load
import pandas as pd
import numpy as np
from .data_processor import preprocess
from .model_registry import retrieve

def get_prediction(**kwargs):
    clf, features = retrieve('loan_approval')
    pred_df = pd.DataFrame(kwargs, index=[0])
    pred_df = preprocess(pred_df)
    pred = clf.predict(pred_df[features])
    return pred[0]
