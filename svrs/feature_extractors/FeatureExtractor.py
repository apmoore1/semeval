from sklearn.base import TransformerMixin
from sklearn.base import BaseEstimator


class FeatureExtractor(BaseEstimator, TransformerMixin):

    def __init__(self, feature='title'):

        self.feature = feature

    def fit(self, feature_list, y=None):
        '''Kept for consistnecy with the TransformerMixin'''

        return self

    def fit_transform(self, feature_list, y=None):
        '''See self.transform'''

        return self.transform(feature_list)

    def transform(self, feature_list):
        return [feature[self.feature] for feature in feature_list]
