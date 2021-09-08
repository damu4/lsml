import joblib

import mlflow
from sklearn.datasets import load_iris
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
from sklearn.base import (
    BaseEstimator,
    TransformerMixin,
)


class ModelTransformer(TransformerMixin, BaseEstimator):
    def __init__(self, mdl):
        self.mdl = mdl

    def fit(self, X, y=None):
        return self.mdl.fit(X, y)

    def transform(self, X):
        return self.mdl.predict(X)


class JSONResponse(TransformerMixin, BaseEstimator):
    def __init__(self, key_name):
        self.key_name = key_name

    def fit(self, X, y=None):
        return X

    def transform(self, X):
        result = {self.key_name: X[0]}
        return result

    def predict(self, X):
        return self.transform(X)


if __name__ == '__main__':
    MLFLOW_SERVER_URL = 'http://127.0.0.1:5000/'
    data = load_iris()
    params = {
        "learning_rate": 0.05,
        "n_estimators": 1000,
        "max_depth": 3,
        "objective": 'multi:softmax',
        "num_class": 3,
    }
    mdl = XGBClassifier(**params)
    mdl.fit(data['data'], data['target'])
    mdl_api = Pipeline([("mdl", ModelTransformer(mdl)), ("pack", JSONResponse('iris'))])
    joblib.dump(mdl, 'iris.mdl')
    with mlflow.start_run(run_name='Experiment 1'):
        mlflow.sklearn.log_model(mdl_api, 'prod_mdl')
