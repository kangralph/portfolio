import pandas as pd
import numpy as np
import datetime as dt

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from fixed_mlb import MultiLabelBinarizerFixedTransformer
from sklearn.linear_model import LogisticRegression

import joblib

df = pd.read_csv('sample.csv')

ohe = OneHotEncoder(sparse=False,handle_unknown='ignore')
multi = MultiLabelBinarizerFixedTransformer()

X = df.drop(labels=['target'],axis=1)
y = df['target']

mlb_col = ['col1','col2','col8']
normal_cols = X.drop(labels=mlb_col,axis=1).columns.tolist()

preprocessor = ColumnTransformer(transformers=[('onehot',ohe,normal_cols),('binerizer',multi,mlb_col)])
preprocessor.fit(X)
joblib.dump(preprocessor,'preprocessor.joblib')

X_pre = preprocessor.transform(X)

final_lr = LogisticRegression(C=0.0001,solver='sag')

final_lr.fit(X_pre,y)

joblib.dump(final_lr,'model.joblib')
