from sklearn.base import TransformerMixin
from sklearn.base import BaseEstimator

class WordReplacement(BaseEstimator, TransformerMixin):



    def __init__(self, words_replace=('name', []), replacement='', expand=None,
                 expand_top_n=10, disimlar=('disimlar_name', [])):

        self.words_replace = words_replace
        self.replacement = replacement
        self.expand = expand
        self.expand_top_n = expand_top_n
        self.disimlar = disimlar

    def fit(self, token_list, y=None):
        '''Kept for consistnecy with the TransformerMixin'''

        return self

    def fit_transform(self, token_list, y=None):
        '''See self.transform'''

        return self.transform(token_list)

    def transform(self, token_list):
        '''Given a list of texts it will return a list of lists contain
        Strings of which these are tokens of the text. Note that the index of
        the tokens list matches the index of which the list of texts was given
        e.g. texts[0] tokens are within the output[0].

        The tokeniser is defined by self.tokeniser and stopwords can be applied
        by setting self.stopword and normalising the text can be done through
        self.normalise. All of this is an interface to:
        SentimentPipeline.pre_processing.process method tokenise'''


        # Expands thwe words_replace with Word2Vec
        if self.expand:
            expand_replace_words = set()
            for replace_word in self.words_replace[1]:
                expand_replace_words.add(replace_word)
                if replace_word in self.expand.vocab:
                    similar_words = self.expand.most_similar(positive=[replace_word],
                                                             negative=self.disimlar[1],
                                                             topn=self.expand_top_n)
                    for sim_word, sim_score in similar_words:
                        expand_replace_words.add(sim_word)
            self.words_replace = (self.words_replace[0], expand_replace_words)

        all_replace_tokens = []

        for tokens in token_list:
            replace_token_list = []
            for token in tokens:
                token_split = token.split()
                replace_tokens = []
                for token_part in token_split:
                    if token_part in self.words_replace[1]:
                        replace_tokens.append(self.replacement)
                    else:
                        replace_tokens.append(token_part)
                replace_token_list.append(' '.join(replace_tokens))
            all_replace_tokens.append(replace_token_list)

        return all_replace_tokens
