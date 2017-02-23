import json
import os
import sys

sys.path.append(os.path.abspath(os.pardir))

import helper

# Change the path name to point to the correct files the first being the json
# file you submitted the second to the gold standard data
with open('../final_output/early_stopping_submission.json', 'r') as mp:
    with open('../data/finance/Headlines_Testdata_withscores.json', 'r') as fp:
        print(helper.eval_func(json.load(fp), json.load(mp)))
