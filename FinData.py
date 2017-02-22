import helper

import gensim

class FinData:
    '''Stores models that reprsent the financial text that cannot be released
    due to license conditions.
    '''

    def __init__(self):

        fin_word2vec_path = helper.config_path(['models', 'fin_word2vec'])
        self._word2vec = gensim.models.Word2Vec.load(fin_word2vec_path)
