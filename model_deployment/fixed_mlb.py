from sklearn.base import BaseEstimator,TransformerMixin
from sklearn.preprocessing import MultiLabelBinarizer
import numpy as np


class MultiLabelBinarizerFixedTransformer(BaseEstimator, TransformerMixin):
    """       
        Wraps `MultiLabelBinarizer` in a form that can work with `ColumnTransformer`
        Taken from: 
            https://stackoverflow.com/questions/59254662/sklearn-columntransformer-with-multilabelbinarizer
         
    """
    def __init__(
            self 
        ):
        self.feature_name = ["mlb"]
        self.mlb = MultiLabelBinarizer(sparse_output=False)

    def fit(self, X, y=None):
        self.mlb.fit(X.values.tolist())
        return self

    def transform(self, X):
        return self.mlb.transform(X.values.tolist())

    def get_feature_names(self, input_features=None):
        cats = self.mlb.classes_
        if input_features is None:
            input_features = ['x%d' % i for i in range(len(cats))]
            print(input_features)
        elif len(input_features) != len(self.categories_):
            raise ValueError(
                "input_features should have length equal to number of "
                "features ({}), got {}".format(len(self.categories_),
                                               len(input_features)))

        feature_names = [f"{input_features[i]}_{cats[i]}" for i in range(len(cats))]
        return np.array(feature_names, dtype=object)