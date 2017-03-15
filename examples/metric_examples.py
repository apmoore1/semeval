import os
import sys

sys.path.append(os.path.abspath(os.pardir))

import helper

def eval(pred_values, true_values, metric):
    total_score = 0
    for index in range(len(pred_values)):
        total_score += metric(pred_values[index], true_values[index])
    return total_score

ex1 = [[[0.2], [0.5]], [[-0.4], [-0.1]]]
ex2 = [[[0.9], [0.2]], [[0.8], [0.3]]]
ex3 = [[[0.2, 0.3]], [[-0.1, -0.2]]]

all_examples = [('Example 1', ex1), ('Example 2', ex2), ('Example 3', ex3)]
all_metrics  = [helper.metric1, helper.metric2, helper.metric3]

flatten = lambda values: [value for sublist in values for value in sublist]

for name, example in all_examples:
    print(name)
    for i, metric in enumerate(all_metrics):
        pred_values = example[0]
        true_values = example[1]
        no_sentences = len(example)
        no_samples = len(flatten(pred_values))
        if i == 0:
            # Reference: http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
            flatten = lambda values: [value for sublist in values for value in sublist]
            pred_values = flatten(pred_values)
            true_values = flatten(true_values)
            metric_score = metric(pred_values, true_values)

        elif i == 1:
            metric_score = eval(pred_values, true_values, metric) / no_sentences
        elif i == 2:
            metric_score = eval(pred_values, true_values, metric) / no_samples

        print('metric {}, value {}'.format(i+1, round(metric_score, 3)))
