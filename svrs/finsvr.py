from semeval import helper as helper
from semeval.svrs.feature_extractors.Tokeniser import Tokeniser
from semeval.svrs.feature_extractors.WordReplacement import WordReplacement


from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import make_scorer
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn import svm


def train(train_text, train_sentiments, n_jobs=-1, n_cv=10,
          scorer=make_scorer(helper.cosine_score)):

    _, _, train_comp_names = helper.fin_data('train')
    train_comp_names = ('train companies', train_comp_names)

    pos_word = ('Excellent word', ['excellent'])
    neg_word = ('Poor word', ['poor'])

    fin_word2vec_model = helper.fin_word_vector()

    parameters = {
        'tokeniser__ngram_range' : [(1,2)],
        'tokeniser__tokeniser_func' : [helper.unitok_tokens],
        'compextract__words_replace' : [train_comp_names],
        'compextract__replacement' : ['companyname'],
        'compextract__expand' : [None],
        'posextract__words_replace' : [pos_word],
        'posextract__replacement' : ['posword'],
        'posextract__expand' : [fin_word2vec_model],
        'posextract__expand_top_n' : [10],
        'negextract__words_replace' : [neg_word],
        'negextract__replacement' : ['negword'],
        'negextract__expand' : [fin_word2vec_model],
        'negextract__expand_top_n' : [10],
        'count_grams__binary' : [True],
        'clf__C' : [0.1],
        'clf__epsilon' : [0.01]
    }


    pipeline = Pipeline([
        ('tokeniser', Tokeniser()),
        ('compextract', WordReplacement()),
        ('posextract', WordReplacement()),
        ('negextract', WordReplacement()),
        ('count_grams', CountVectorizer(analyzer=helper.analyzer)),
        ('clf', svm.LinearSVR())
    ])



    grid_search = GridSearchCV(pipeline, param_grid=parameters, cv=n_cv,
                               scoring=scorer, n_jobs=n_jobs)
    grid_clf    = grid_search.fit(train_text, train_sentiments)

    return grid_clf
