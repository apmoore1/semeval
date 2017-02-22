from semeval import helper as helper

from sklearn.base import TransformerMixin
from sklearn.base import BaseEstimator


class Tokeniser(BaseEstimator, TransformerMixin):

    def __init__(self, ngram_range=(1,1), tokeniser_func=helper.unitok_tokens):

        self.ngram_range = ngram_range
        self.tokeniser_func = tokeniser_func

    def fit(self, texts, y=None):
        '''Kept for consistnecy with the TransformerMixin'''

        return self

    def fit_transform(self, texts, y=None):
        '''See self.transform'''

        return self.transform(texts)

    def transform(self, texts):
        '''Given a list of texts it will return a list of lists contain
        Strings of which these are tokens of the text. Note that the index of
        the tokens list matches the index of which the list of texts was given
        e.g. texts[0] tokens are within the output[0].

        The tokeniser is defined by self.tokeniser and stopwords can be applied
        by setting self.stopword and normalising the text can be done through
        self.normalise. All of this is an interface to:
        SentimentPipeline.pre_processing.process method tokenise'''


        tokens = [self.tokeniser_func(text) for text in texts]
        n_gram_tokens = helper.ngrams(tokens, self.ngram_range)
        return n_gram_tokens
