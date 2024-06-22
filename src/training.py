import argparse
import pandas as pd
import numpy as np
import datetime
import logging

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import classification_report, f1_score
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.ensemble import RandomForestClassifier
from joblib import dump, load

import data_processor
import model_registry

logging.basicConfig(level=logging.INFO)

features = ['emp_len','int_rate','log_annual_inc','fico_range_high','loan_amnt']
numeric_features = ['int_rate','log_annual_inc','fico_range_high','loan_amnt']
categorical_features = ['emp_len']
label = 'fully_paid'

def run(data_path, model_path, f1_criteria):
    logging.info('Process Data...')
    df = data_processor.run(data_path)
    
    numeric_transformer = MinMaxScaler()
    categorical_transformer = OneHotEncoder(handle_unknown="ignore")
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_transformer, numeric_features),
            ("cat", categorical_transformer, categorical_features),
        ]
    )
    
    #Train-Test Split
    logging.info('Start Train-Test Split...')
    X_train, X_test, y_train, y_test = train_test_split(df[features], \
                                                        df[label], \
                                                        test_size=0.2, \
                                                        random_state=0)
    
    #Train Classifier
    logging.info('Start Training...')
    random_forest = RandomForestClassifier(n_estimators=100,
                                           max_depth=4, 
                                           class_weight = "balanced",
                                           n_jobs=2)
    
    clf = Pipeline(steps=[("preprocessor", preprocessor),\
                          ("binary_classifier", random_forest)
                         ])
    clf.fit(X_train, y_train)
    
    #Evaluate and Deploy
    logging.info('Evaluate...')
    score = f1_score(y_test, clf.predict(X_test), average='weighted')
    if score >= f1_criteria:
        logging.info('Deploy...')
        mdl_meta = { 'name': 'loan_approval', 'metrics': f"f1:{score}" }
        model_registry.register(clf, features, mdl_meta)
        #dump(clf, model_path+'mdl.joblib')
        #dump(features, model_path+'raw_features.joblib')
    
    logging.info('Training completed.')
    return None

if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--data_path", type=str)
    argparser.add_argument("--model_path", type=str)
    argparser.add_argument("--f1_criteria", type=float)
    args = argparser.parse_args()
    run(args.data_path, args.model_path, args.f1_criteria)