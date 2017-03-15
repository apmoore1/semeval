import os
import sys

sys.path.append(os.path.abspath(os.pardir))

from semeval.lstms.EarlyStoppingLSTM import EarlyStoppingLSTM
from semeval.lstms.TweekedLSTM import TweekedLSTM

from semeval.svrs import finsvr
from semeval.svrs import aspect_finsvr

import semeval.helper as helper




# Example of how to load the test and train data
train_texts, train_sentiments, train_companies = helper.fin_data('train')
test_texts, test_sentiments, test_companies = helper.fin_data('test')
# Example of how to load the word 2 vec model
fin_word2vec_model = helper.fin_word_vector()
# Required to for the results on the test data
true_values = helper.eval_format(test_texts, test_sentiments)

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
helper.stats_report(svr_grid_clf, '../results/best_clf_results.tsv')

# This finds the top 50 errors by default within the test data.
svr_error_details, svr_error_dist = helper.error_analysis(test_texts, test_sentiments,
                                                          test_companies, svr_clf)
pred_values = helper.eval_format(test_texts, svr_clf.predict(test_texts))
print('Metric 1 {}'.format(helper.eval_func(true_values, pred_values, metric=helper.metric1)))
print('Metric 2 {}'.format(helper.eval_func(true_values, pred_values, metric=helper.metric2)))
print('Metric 3 {}'.format(helper.eval_func(true_values, pred_values, metric=helper.metric3)))


# Convert the training and testing data into aspect data format for the aspect_finsvr
aspect_train_data = [{'text':train_texts[i], 'aspects': train_companies[i]}
                     for i in range(len(train_texts))]
aspect_test_data = [{'text':test_texts[i], 'aspects': test_companies[i]}
                     for i in range(len(test_texts))]
aspect_grid_clf = aspect_finsvr.train(aspect_train_data, train_sentiments)
aspect_clf = aspect_grid_clf.best_estimator_
helper.stats_report(aspect_grid_clf, '../results/best_aspect_clf_results.tsv')
asp_error_details, asp_error_dist = helper.error_analysis(aspect_test_data, test_sentiments,
                                                          test_companies, aspect_clf,
                                                          text=test_texts)
pred_values = helper.eval_format(test_texts, aspect_clf.predict(aspect_test_data))
print('Metric 1 {}'.format(helper.eval_func(true_values, pred_values, metric=helper.metric1)))
print('Metric 2 {}'.format(helper.eval_func(true_values, pred_values, metric=helper.metric2)))
print('Metric 3 {}'.format(helper.eval_func(true_values, pred_values, metric=helper.metric3)))

###
#   The following is examples of how to train the LSTM's and use the same
#   error analysis. Also how to show the cross validation results.
###

# Creates an instance that takes a Word Vector model that will be used to convert
# the inputted text into word vectors.
early_lstm = EarlyStoppingLSTM(fin_word2vec_model)

# Get the 10 fold cross validation results
early_res = early_lstm.cross_validate(train_texts, train_sentiments)


early_lstm.fit(train_texts, train_sentiments)
early_error_details, early_error_dist = helper.error_analysis(test_texts, test_sentiments,
                                                            test_companies, early_lstm)

# Train the LSTM model over all the training data

pred_values = helper.eval_format(test_texts, early_lstm.predict(test_texts))

print('Metric 1 {}'.format(helper.eval_func(true_values, pred_values, metric=helper.metric1)))
print('Metric 2 {}'.format(helper.eval_func(true_values, pred_values, metric=helper.metric2)))
print('Metric 3 {}'.format(helper.eval_func(true_values, pred_values, metric=helper.metric3)))

tweeked_lstm = TweekedLSTM(fin_word2vec_model)
tweeked_res = tweeked_lstm.cross_validate(train_texts, train_sentiments)
tweeked_lstm.fit(train_texts, train_sentiments)
tweek_error_details, tweek_error_dist = helper.error_analysis(test_texts, test_sentiments,
                                                            test_companies, tweeked_lstm)


pred_values = helper.eval_format(test_texts, tweeked_lstm.predict(test_texts))
print('Metric 1 {}'.format(helper.eval_func(true_values, pred_values, metric=helper.metric1)))
print('Metric 2 {}'.format(helper.eval_func(true_values, pred_values, metric=helper.metric2)))
print('Metric 3 {}'.format(helper.eval_func(true_values, pred_values, metric=helper.metric3)))

# Print both LSTM's cross validation results
avg_tweek_percentage = (sum(tweeked_res) / len(tweeked_res)) * 100
print('Tweeked lstm cross val score {}'.format(avg_tweek_percentage))

avg_early_percentage = (sum(early_res) / len(early_res)) * 100
print('Early lstm cross val score {}'.format(avg_early_percentage))

import code
code.interact(local=locals())
