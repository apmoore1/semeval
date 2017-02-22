from sklearn.base import TransformerMixin
from sklearn.base import BaseEstimator


class ToList(BaseEstimator, TransformerMixin):

    def __init__(self):
        pass

    def fit(self, data, y=None):
        '''Kept for consistnecy with the TransformerMixin'''

        return self

    def fit_transform(self, data, y=None):
        '''See self.transform'''

        return self.transform(data)

    def transform(self, data):
        return [[item] for item in data]
