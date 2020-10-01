import os
import sys
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import clear_output
from six.moves import urllib


dftrain = pd.read_csv("./data/train.csv")
dfeval = pd.read_csv("./data/eval.csv")

y_train = dftrain.pop('survived')
y_eval = dfeval.pop('survived')

CATEGORICAL_COLUMNS = ['sex', 'sibsp',
                       'parch', 'pclass',  'home_dest']
NUMERIC_COLUMNS = ['age', 'fare']

feature_columns = []

for feature_name in CATEGORICAL_COLUMNS:
    # gets alist of all uniquue valueus from given feature column
    vocabulary = dftrain[feature_name].unique()
    feature_columns.append(
        tf.feature_column.sequence_categorical_column_with_vocabulary_list(feature_name, vocabulary))

for feature_name in NUMERIC_COLUMNS:
    feature_columns.append(tf.feature_column.numeric_column(
        feature_name, dtype=tf.float32))
# print(feature_columns)
# print(dftrain["embarked"].unique())


def make_input_fn(data_df, label_df, num_epochs=10, shuffle=True, batch_size=32):
    def input_function():
        ds = tf.data.Dataset.from_tensor_slices((dict(data_df), label_df))
        if shuffle:
            ds = ds.shuffle(1000)
        ds = ds.batch(batch_size).repeat(num_epochs)
        return ds
    return input_function


train_input_fn = make_input_fn(dftrain, y_train)
eval_input_fn = make_input_fn(dfeval, y_eval, num_epochs=1, shuffle=False)

linear_est = tf.estimator.LinearClassifier(
    feature_columns=feature_columns)

linear_est.train(train_input_fn)
#result = linear_est.evaluate(eval_input_fn)
result = list(linear_est.predict(eval_input_fn))

# clear_output()
print(dfeval.loc[0])
print(result[0]["probabilities"][1])
