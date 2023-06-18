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

from .feature_graph import InputFeature
from .feature_graph import NumericalFeature
from .feature_graph import CategoricalFeature
from .feature_graph import ConcatenateFeatures

# Implements a recursive-descent parser for the
# model definition language file

def parse_mdl(model_def):
    if not isinstance(model_def, abc.Mapping):
        raise TypeError("Model definition object must be of type Mappable")
    
    # check for required keys
    for key in ["target_column", "ml_model", "features"]:
        if key not in model_def:
            raise TypeError("Missing required key '{}'".format(key))
            
    if not isinstance(model_def["target_column"], str):
        raise TypeError("Target column must be specified as a string.")
    
    parse_ml_model(model_def["ml_model"])
    feature_graph = parse_features(model_def["features"])
    
    return feature_graph

def parse_ml_model(model_def):
    if not isinstance(model_def, abc.Mapping):
        raise TypeError("ML model definition object must be of type Mappable")
    
    # check for required keys
    for key in ["model_type"]:
        if key not in model_def:
            raise TypeError("Missing required key '{}'".format(key))
    
    allowed_model_types = ["DummyClassifier",
                           "RandomForestClassifier",
                           "LogisticRegressionNormal",
                           "LogisticRegressionSGD",
                           "DummyRegressor",
                           "RandomForestRegressor",
                           "LinearRegressionNormal",
                           "LinearRegressionSGD"]
    if model_def["model_type"] not in allowed_model_types:
        raise ValueError("Only the model types {} are allowed".format(", ".join(allowed_model_types)))
    
    return True
    
def parse_features(features_def):
    if not isinstance(features_def, abc.Mapping):
        raise TypeError("ML model definition object must be of type Mappable")
    
    for key in features_def.keys():
        if not isinstance(key, str):
            raise TypeError("Feature names must be specified as strings.")
    
    all_outputs = []
    for output_name, feature_def in features_def.items():
        feature_node = parse_feature(output_name, feature_def)
        all_outputs.append(feature_node)
    
    return ConcatenateFeatures(all_outputs)
    
def parse_feature(output_name, feature_def):
    if not isinstance(feature_def, abc.Mapping):
        raise TypeError("Feature definition object must be of type Mappable")
    
    required_keys = ["column", "type"]
    for key in required_keys:
        if key not in feature_def:
            raise TypeError("Missing required key '{}'".format(key))
            
    if not isinstance(feature_def["column"], str):
        raise TypeError("Feature column names must be specified as strings.")
        
    input_node = InputFeature(feature_def["column"], feature_def["column"])
    
    if feature_def["type"] == "numerical":
        return NumericalFeature(output_name, feature_def["column"])
    elif feature_def["type"] == "categorical":
        return CategoricalFeature(output_name, feature_def["column"])
    else:
        raise ValueError("'{}' is not one of the allowed feature types".format(feature_df["type"]))
    
    return True