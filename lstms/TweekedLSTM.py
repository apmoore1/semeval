from semeval import helper as helper
from semeval.lstms.LSTMModel import LSTMModel

import numpy

from keras.models import Sequential
from keras.layers import Dense, Activation, Bidirectional, LSTM

class TweekedLSTM(LSTMModel):
    '''Model that can train an LSTM and apply the trainned model to unseen
    data. Inherits from LSTMModel.

    Instance Arguments:
    self._word2vec_model - gensim.models.Word2Vec required as an argument to __init__
    self._max_length = 0
    self._model = None

    public methods:
    train - trains a Bi-directional LSTM with dropout and manually set stopping
    on the texts and sentiment values given.

    test - Using the trained model saved at self._model will return a list of
    sentiment values given the texts in the argument of the method.
    '''



    def __init__(self, word2vec_model):
        super().__init__(word2vec_model)

    def fit(self, train_texts, sentiment_values):
        '''Given a list of Strings and a list of floats (sentiments) or numpy
        array of floats. It will return a trained LSTM model and `save` the model to
        self._model for future use using self.test(texts).

        The model converts the list of strings into list of numpy matrixs
        which has the following dimensions:
        length of the longest train text broken down into tokens
        by
        the vector size of the word2vec model given in the constructor

        e.g. 21, 300 if the word2vec model vector size if 300 and the length of
        the longest train text in tokens is 21.

        For more details on the layers use read the source or after training
        visualise using visualise_model function.
        '''

        super().fit()

        # Required for any transformation of text latter.
        max_length    = self._set_max_length(train_texts)
        vector_length = self._word2vec_model.vector_size

        train_vectors = self._text2vector(train_texts)

        model = Sequential()
        # Output of this layer is of max_length by max_length * 2 dimension
        # instead of max_length, vector_length
        model.add(Bidirectional(LSTM(max_length, activation='softsign',
                                     dropout_W=0.2, dropout_U=0.2,
                                     return_sequences=True),
                                input_shape=(max_length, vector_length)))
        model.add(Bidirectional(LSTM(max_length, activation='softsign',
                                     dropout_W=0.2, dropout_U=0.2)))
        model.add(Dense(1))
        model.add(Activation('linear'))

        model.compile(loss='mse',
                      optimizer='rmsprop',
                      metrics=['cosine_proximity'],
                      clipvalue=5)

        model.fit(train_vectors, sentiment_values, nb_epoch=25)

        return self._set_model(model)
