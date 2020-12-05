import os

import pandas as pd
import numpy as np
import joblib


class YourPredictor(object):
    """
    Custom Predictor for your model. Runs all the necessary code you 
    need prior to predicting. 
    """

    def __init__(self, model, preprocessor):
        """Stores artifacts for prediction. Only initialized via `from_path`.
        """
        self._model = model
        self._preprocessor = preprocessor

    def predict(self, instances, **kwargs):
        """Performs custom prediction.

        Preprocesses inputs, then performs prediction using the trained
        scikit-learn model.

        Args:
            instances: A list of prediction input instances.
            **kwargs: A dictionary of keyword args provided as additional
                fields on the predict request body.

        Returns:
            A list of Predictions and Class Probabilities for each instance.
        """
        cols = ["col1","col2","col3","col4","col5",
                "col6","col7","col8","col9"]
        try:
            items = np.array(instances).reshape(-1,len(instances))
            inputs = pd.DataFrame(items,columns=cols)
            preprocessed_inputs = self._preprocessor.transform(inputs)
            outputs = self._model.predict(preprocessed_inputs)
            probs = self._model.predict_proba(preprocessed_inputs)
            
            return {
                'prediction':outputs.tolist(),
                'class_proba':probs.tolist(),
                }
        except Exception as e:
            raise e

    @classmethod
    def from_path(cls, model_dir):
        """Creates an instance of YourPredictor using the given path.

        This loads artifacts that have been copied from your model directory in
        Cloud Storage. YourPredictor uses them during prediction.

        Args:
            model_dir: The local directory that contains the trained
                scikit-learn model and the pickled preprocessor instance. These
                are copied from the Cloud Storage model directory you provide
                when you deploy a version resource.

        Returns:
            An instance of `YourPredictor`.
        """
        model_path = os.path.join(model_dir, 'model.joblib')
        model = joblib.load(model_path)

        preprocessor_path = os.path.join(model_dir, 'preprocessor.joblib')
        preprocessor = joblib.load(preprocessor_path)

        return cls(model, preprocessor)