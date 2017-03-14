# Lancaster A [SemEval task 5](http://alt.qcri.org/semeval2017/task5/) track 2 code base. Predicting the sentiment of financial headlines.

The aim of the task was given a financial headline find the sentiment of the
headline with respect to a particular company that is mentioned in the headline.
The data that was associated with this task can be found [here](https://bitbucket.org/ssix-project/semeval-2017-task-5-subtask-2/)
once downloaded if you wish to keep using the same helper functions that I use in
the code please put the individual training, test, trail data in this [folder](./data/finance)
or else change the [config file](./config.yml) appropriately, also please look at
the [config file](./config.yml) to see how the training, test and trial data files
should be named.

This contains all of the code that is associated with the SemEval paper that is
currently being written.

The headlines were predicted using two methods:
1. Support Vector Regression (SVR) used [scikit learns library](http://scikit-learn.org/stable/index.html).
2. Bi-Directional LSTM's used [keras library](https://keras.io/).

The SVR's can be found in their own [directory](./svrs) and likewise for the
[LSTM's](./lstms). [The Early Stopping LSTM](./lstms/EarlyStoppingLSTM.py) performed the best on the finance
dataset.

## How to use the code base

Quick example of all the main features of this code base can be found within the examples folder
in the [run file](./examples/run.py) NOTE that this may take a long time to run with respect to the LSTM's.

## SVR's

There are two SVR's both have been left with features that maximise the performance
on the train finance dataset when cross validation (CV) has been performed. Both of them have
code commented out to show how the different features can be implemented in case
anybody wants to test any of the scores that are in the paper or see how the
features affect the CV score.

Both of these SVR can be used with other data with the same type of properties e.g.
the [finsvr](./svrs/finsvr.py) assumes sentence level sentiment data and the
[aspect svr](./svrs/aspect_finsvr.py) assumes aspect level sentiment data.


[finsvr](./svrs/finsvr.py) is a sentence level sentiment classifier as it only takes
into account the headline sentence and not the company that sentiment is in
respect to which tends to be fine for sentences that are only about one company.

[aspect svr](./svrs/aspect_finsvr.py) compared to finsvr does take into account
the company as well as the sentence. Which tends to perform slightly better.

The [results](./results) folder contains TSV files of the performance of different
feature parameter settings for both SVR's. This will be summarised in the paper being
written.

## LSTM's

There are two LSTM's both sub class [LSTMModel](./lstms/LSTMModel.py). Note that
in the paper the standard LSTM is called the Tweeked LSTM in the code base sorry for any 
confusion.

[Early Stopping LSTM](./lstms/EarlyStoppingLSTM.py) as the name suggests does not have a set number of times
that it iterates over the training data instead it stops based on the number of
times it stops improving this is hard coded as 10. It also has a slightly different
architecture design but not that much different to [Tweeked LSTM](./lstms/TweekedLSTM.py) which stops
after 25 times iterating over the training data. The Early Stopping model performs
worse over CV on the training data but performed the best on test set of the
task (of which true values for that data set has not been released yet hence why I
talk about CV over the training data) this was expected as the model is more
generalisable due to the early stopping condition.

Both of these LSTM's are affectively sentence level classifiers as they only consider
the headline text and nothing else. Also compared to the SVR's they do not have an
feature engineering.

NOTE if you do these for other datasets you may want to change the output dimension
of the LSTMs from the length of the longest sentence in the training data to something
more relevant this was used as it appeared to work well for this task.

## Installs

Require:
1. Python 3.4.3 or above.

If you would like to visualise the LSTM's then GraphViz is required for Debian based
systems this can be installed using:

apt-get install graphviz

### Note on [Unitok-3.0.3](./unitok-3.0.3)

I have included unitok-3.0.3 within this project as this project requires a Python 3
version and the one currently [available](http://corpus.tools/wiki/Unitok) is
Python 2 only therefore this version is Python 3 only for English.

To install go to [Unitok-3.0.3](./unitok-3.0.3) folder and run:

python3 setup.py install

### All of the other pips

All the other pips can be installed using the following command:

pip3 install -r requirements.txt


## [Final output](./final_output)

In this folder are the two submission json files that were submitted to the
SEMEval challenge participating in [Task 5 track 2](http://alt.qcri.org/semeval2017/task5/) headline sentiment prediction. Both submission used a bi-direction LSTM.



### Finance Word2Vec model

None of the data that was used to create the Word2Vec models are allowed to be
released due to license agreements. However the Word2Vec model can be, therefore
the [Finance model (all_fin_model_lower)](./models/word2vec_models/) is released
and it was trained using the following parameters any parameters not mentioned are
just default parameters:

gensim.models.Word2Vec(sentences=self, min_count=40, workers=4, window=10, sample=1e-3, size=300)

number of articles = 189, 206
tokens = 161, 877, 425
number of sections used - 567071

They are a collection of financial news articles such as:
1. The Telegraph.
2. Financial Times.
3. Reuters
4. Press Association
Which were collected from  [Factiva](https://global.factiva.com/factivalogin/login.asp?productname=global)

Word2Vec library used was [Gensim](https://radimrehurek.com/gensim/models/word2vec.html)
all text was lower cased and then tokensied using [unitok](./unitok-3.0.3) before being
fed into the word2vec model. No sentence splitting was used as it was fed news papers broken down into headline, and two main stories.

The reason those parameters were chosen as the [Kaggle blog](https://www.kaggle.com/c/word2vec-nlp-tutorial/details/part-2-word-vectors)
suggested they were good and also I didn't have time to experiment with different model parameters.

## License

[GNU GPLv3](https://choosealicense.com/licenses/gpl-3.0/)
