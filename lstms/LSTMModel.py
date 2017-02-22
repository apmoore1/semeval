from semeval import helper as helper

from keras.utils.visualize_util import plot
import numpy
from scipy.spatial.distance import cosine
from sklearn.model_selection import KFold

class LSTMModel:

    def __init__(self, word2vec_model):
        self._word2vec_model = word2vec_model
        self._max_length = 0
        self._model = None



    def cross_validate(self, train_text, train_sentiments, n_folds=10,
                       shuffle=True, score_function=helper.cosine_score):

        all_results = []
        train_text_array = numpy.asarray(train_text)
        train_sentiments_array = numpy.asarray(train_sentiments)

        kfold = KFold(n_splits=n_folds, shuffle=shuffle)
        for train, test in kfold.split(train_text_array, train_sentiments_array):
            self.fit(train_text_array[train], train_sentiments_array[train])
            predicted_sentiments = self.predict(train_text_array[test])
            result = score_function(predicted_sentiments, train_sentiments_array[test])
            all_results.append(result)
        return all_results

    def _text2vector(self, texts):
        '''Given a list of Strings will convert to a numpy 3D array where each
        token in the text is reprsented as a vector from the self.word2vec_model.

        see semeval.helper.process_data for more details.

        list of strings -> 3D numpy array (len(texts), max_number_tokens,
        self.word2vec_model.vector_size)
        '''

        if self._max_length == 0:
            raise Exception('Your model requires training first')

        return helper.process_data(texts, self._word2vec_model, self._max_length)

    def fit(self):
        '''All sub classes should overide this but pre-filter so that random
        seed can be set and allow all models to be more reprocible.
        '''

        # Required for reproducibility
        numpy.random.seed(1337)

    def predict(self, test_texts):
        '''Given a list of strings will return a list of predicted values based
        on what the LSTM has been trained on.

        List of strings -> list of predicted values.
        '''

        test_vectors = self._text2vector(test_texts)
        if self._model == None:
            raise Exception('Your model requires training first')
        return self._model.predict(test_vectors)

    def _set_max_length(self, texts):

        self._max_length = helper.max_length(texts)
        return self._max_length

    def _set_model(self, model):

        self._model = model
        return model

    def visualise_model(self, f_name):
        '''Given a file path will visulaise the LSTM model.

        String -> Void
        '''

        if self._model == None:
            raise Exception('Your model requires training first')
        plot(self._model, to_file=f_name)
