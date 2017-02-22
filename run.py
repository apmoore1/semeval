import os
import sys

sys.path.append(os.getcwd())

from semeval.lstms.EarlyStoppingLSTM import EarlyStoppingLSTM
from semeval.lstms.TweekedLSTM import TweekedLSTM

from semeval.svrs import finsvr
from semeval.svrs import aspect_finsvr

import semeval.helper as helper




# Example of how to load the test and train data
train_texts, train_sentiments, train_companies = helper.fin_data('train')
test_texts, _, test_companies = helper.fin_data('test')
# Example of how to load the word 2 vec model
fin_word2vec_model = helper.fin_word_vector()

###
#   The following is exmaples of how to train the SVR's and how to perform
#   error analysis using them.
###

# Training the SVR's performs a grid search over the possible parameters have
# been selected in that module.
svr_grid_clf = finsvr.train(train_texts, train_sentiments)
svr_clf = svr_grid_clf.best_estimator_

# Example of how to report the best parameter results found using the
# grid search this can only be done on the SVR which return a Grid Search.
helper.stats_report(svr_grid_clf, './results/all_clf_results.tsv')

# This finds the top 50 errors by default. error_details
svr_error_details, svr_error_dist = helper.error_analysis(train_texts, train_sentiments,
                                                          train_companies, svr_clf)


# Convert the training data into aspect data format for the aspect_finsvr
aspect_train_data = [{'text':train_texts[i], 'aspects': train_companies[i]}
                     for i in range(len(train_texts))]
aspect_grid_clf = aspect_finsvr.train(aspect_train_data, train_sentiments)
aspect_clf = aspect_grid_clf.best_estimator_
helper.stats_report(aspect_grid_clf, './results/comp_aspect_clf_results.tsv')
asp_error_details, asp_error_dist = helper.error_analysis(aspect_train_data, train_sentiments,
                                                          train_companies, aspect_clf,
                                                          train_text=train_texts)

###
#   The following is examples of how to train the LSTM's and use the same
#   error analysis. Also how to show the cross validation results.
###

# Trains the LSTM
early_lstm = EarlyStoppingLSTM(fin_word2vec_model)
# Get the 10 fold cross validation results
early_res = early_lstm.cross_validate(train_texts, train_sentiments)
# Error analysis just like the SVR's
early_error_details, svr_error_dist = helper.error_analysis(train_texts, train_sentiments,
                                                            train_companies, early_lstm)


tweeked_lstm = TweekedLSTM(fin_word2vec_model)
tweeked_res = tweeked_lstm.cross_validate(train_texts, train_sentiments)
tweek_error_details, svr_error_dist = helper.error_analysis(train_texts, train_sentiments,
                                                            train_companies, tweeked_lstm)

# Print both LSTM's cross validation results
avg_tweek_percentage = (sum(tweeked_res) / len(tweeked_res)) * 100
print('Tweeked lstm cross val score {}'.format(avg_tweek_percentage))

avg_early_percentage = (sum(early_res) / len(early_res)) * 100
print('Early lstm cross val score {}'.format(avg_early_percentage))

import code
code.interact(local=locals())
