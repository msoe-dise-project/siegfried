# Siegfried
Siegfried is a command-line tool and library for training and evaluating machine learning models. There are two
notable features:

1. Models are specified using a model definition language.  The software takes a tabular data set as input.
A model definition specifies:
  1. The label column
  1. The columns to use as features
  1. Transformations such as standardization, imputation, and vectorization
1. The software outputs a serialized pipeline for generating predictions on tabular data in the same
format as the training data.


