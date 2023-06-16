"""
Copyright 2023 MSOE DISE Project

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from collections import abc

# Implements a recursive-descent parser for validating
# the model definition language file

def validate_mdl(model_def):
    if not isinstance(model_def, abc.Mapping):
        raise TypeError("Model definition object must be of type Mappable")
    
    # check for required keys
    for key in ["ml_problem", "ml_model", "features"]:
        if key not in model_def:
            raise TypeError("Missing required key '{}'".format(key))
            
    validate_ml_problem(model_def["ml_problem"])
    validate_ml_model(model_def["ml_model"])
            
    return True
    
def validate_ml_problem(problem_def):
    if not isinstance(problem_def, abc.Mapping):
        raise TypeError("ML problem definition object must be of type Mappable")
    
    # check for required keys
    for key in ["label_column", "output_variable_type"]:
        if key not in problem_def:
            raise TypeError("Missing required key '{}'".format(key))
    
    allowed_output_types = ["regression", "classification_binary", "classification_probability"]
    if problem_def["output_variable_type"] not in allowed_output_types:
        raise ValueError("Only the output variable types 'regression', 'classification_binary', and 'classification_probability' are allowed")
    
    if not isinstance(problem_def["label_column"], str):
        raise TypeError("Label column must be specified as a string.")
    
    return True

def validate_ml_model(model_def):
    if not isinstance(model_def, abc.Mapping):
        raise TypeError("ML model definition object must be of type Mappable")
    
    # check for required keys
    for key in ["model_type"]:
        if key not in model_def:
            raise TypeError("Missing required key '{}'".format(key))
    
    allowed_model_types = ["RandomForestClassifier",
                           "LogisticRegressionNormal",
                           "LogisticRegressionSGD",
                           "RandomForestRegressor",
                           "LinearRegressionNormal",
                           "LinearRegressionSGD"]
    if model_def["model_type"] not in allowed_model_types:
        raise ValueError("Only the model types {} are allowed".format(", ".join(allowed_model_types)))
    
    return True
    
def validate_features(features_def):
    if not isinstance(features_def, abc.Mapping):
        raise TypeError("ML model definition object must be of type Mappable")
    
    for key in features_def.keys():
        if not isinstance(key, str):
            raise TypeError("Feature names must be specified as strings.")
    
    return True
    
def validate_feature(feature_def):
    if not isinstance(feature_def, abc.Mapping):
        raise TypeError("Feature definition object must be of type Mappable")
    
    required_keys = ["column", "type"]
    for key in required_keys:
        if key not in feature_def:
            raise TypeError("Missing required key '{}'".format(key))
            
    allowed_types = ["numerical", "categorical", "string", "date", "datetime"]
    if feature_df["type"] not in allowed_type:
        raise ValueError("'{}' is not one of the allowed feature types: {}".format(feature_df["type"], ", ".join(allowed_types)))
    
    return True