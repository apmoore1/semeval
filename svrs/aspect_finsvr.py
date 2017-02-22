from semeval import helper as helper
from semeval.svrs.feature_extractors.Tokeniser import Tokeniser
from semeval.svrs.feature_extractors.WordReplacement import WordReplacement
from semeval.svrs.feature_extractors.FeatureExtractor import FeatureExtractor
from semeval.svrs.feature_extractors.ToList import ToList


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import FeatureUnion
from sklearn.pipeline import Pipeline
from sklearn import svm


def train(train_data, train_sentiments, n_jobs=-1, n_cv=10,
                scorer=make_scorer(helper.cosine_score)):

    train_comp_names = ('train companies', [data['aspects'] for data in train_data])

    union_parameters = {
        'union__ngrams__tokeniser__ngram_range' : [(1,2)],
        'union__ngrams__tokeniser__tokeniser_func' : [helper.unitok_tokens],
        'union__ngrams__text_extract__feature' : ['text'],
        'union__ngrams__compextract__words_replace' : [train_comp_names],
        'union__ngrams__compextract__replacement' : ['companyname'],
        'union__ngrams__compextract__expand' : [None],
        'union__ngrams__count_grams__binary' : [True],
        'union__target_extract__aspect__feature' : ['aspects'],
        'union__target_extract__count_grams__binary': [True],
        'clf__C' : [0.1],
        'clf__epsilon' : [0.01]
    }

    union_pipeline = Pipeline([
        ('union', FeatureUnion([
            ('ngrams', Pipeline([
                ('text_extract', FeatureExtractor()),
                ('tokeniser', Tokeniser()),
                ('compextract', WordReplacement()),
                ('count_grams', CountVectorizer(analyzer=helper.analyzer))
            ])),
            ('target_extract', Pipeline([
                ('aspect', FeatureExtractor()),
                ('aspect_list', ToList()),
                ('count_grams', CountVectorizer(analyzer=helper.analyzer))
            ])),
        ])),
        ('clf', svm.LinearSVR())
    ])


    grid_search = GridSearchCV(union_pipeline, param_grid=union_parameters, cv=n_cv,
                               scoring=scorer, n_jobs=n_jobs)
    grid_clf    = grid_search.fit(train_data, train_sentiments)

    return grid_clf
