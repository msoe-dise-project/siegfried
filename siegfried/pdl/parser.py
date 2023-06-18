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

from ..data_graph import *

from sklearn.dummy import DummyClassifier
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import RandomForestRegressor

# Implements a recursive-descent parser for the
# model definition language file

def parse_pdl(pipeline_def):
    if not isinstance(pipeline_def, abc.Mapping):
        raise TypeError("Pipeline definition object must be of type Mappable")
    
    # check for required keys
    for key in ["output_variable", "ml_model", "input_variables"]:
        if key not in pipeline_def:
            raise TypeError("Missing required key '{}'".format(key))
    
    model = parse_ml_model(pipeline_def["ml_model"])
    input_graph = parse_input_variables(pipeline_def["input_variables"])
    output_graph = parse_output_variable(pipeline_def["output_variable"])
    
    return DataGraph(input_graph, output_graph)
    
def parse_output_variable(output_variable_def):
    if not isinstance(output_variable_def, abc.Mapping):
        raise TypeError("Output variable definition object must be of type Mappable")
    
    # check for required keys
    for key in ["column", "type"]:
        if key not in output_variable_def:
            raise TypeError("Missing required key '{}'".format(key))
    
    if not isinstance(output_variable_def["column"], str):
        raise TypeError("Output variable column name must be specified as strings.")
    
    if not isinstance(output_variable_def["type"], str):
        raise TypeError("Output variable type must be specified as strings.")
        
    if output_variable_def["type"] == "numerical":
        return NumericalOutputVariable(output_variable_def["column"])
    elif output_variable_def["type"] == "categorical":
        return CategoricalOutputVariable(output_variable_def["column"])
    else:
        raise ValueError("'{}' is not one of the allowed variable types".format(feature_df["type"]))
        
    return None
    

def parse_ml_model(model_def):
    if not isinstance(model_def, abc.Mapping):
        raise TypeError("ML model definition object must be of type Mappable")
    
    # check for required keys
    for key in ["model_type"]:
        if key not in model_def:
            raise TypeError("Missing required key '{}'".format(key))
    
    if model_def["model_type"] == "DummyClassifier":
        return parse_dummy_classifier(model_def)
    elif model_def["model_type"] == "RandomForestClassifier":
        return parse_rf_classifier(model_def)
    elif model_def["model_type"] == "DummyRegressor":
        return parse_dummy_regressor(model_def)
    elif model_def["model_type"] == "RandomForestRegressor":
        return parse_rf_regressor(model_def)
    else:
        raise ValueError("Unknown model type '{}'".format(model_def["model_type"]))
    
    return True
    
def parse_dummy_classifier(model_def):
    return DummyClassifier()
    
def parse_rf_classifier(model_def):
    return RandomForestClassifier()
    
def parse_dummy_regressor(model_def):
    return DummyRegressor()

def parse_rf_regressor(model_def):
    return RandomForestRegressor()
    
def parse_input_variables(input_variables_def):
    if not isinstance(input_variables_def, abc.Mapping):
        raise TypeError("Input variables definition object must be of type Mappable")
    
    for key in input_variables_def.keys():
        if not isinstance(key, str):
            raise TypeError("Input variable names must be specified as strings.")
    
    all_outputs = []
    for output_name, input_variable_def in input_variables_def.items():
        input_variable_node = parse_input_variable(output_name, input_variable_def)
        all_outputs.append(input_variable_node)
    
    return ConcatenateVariables(all_outputs)
    
def parse_input_variable(output_name, input_variable_def):
    if not isinstance(input_variable_def, abc.Mapping):
        raise TypeError("Input variable definition object must be of type Mappable")
    
    required_keys = ["column", "type"]
    for key in required_keys:
        if key not in input_variable_def:
            raise TypeError("Missing required key '{}'".format(key))
    
    if not isinstance(input_variable_def["column"], str):
        raise TypeError("Input variable column names must be specified as strings.")
    
    if not isinstance(input_variable_def["type"], str):
        raise TypeError("Input variable types must be specified as strings.")
        
    if input_variable_def["type"] == "numerical":
        return NumericalInputVariable(input_variable_def["column"], output_name=output_name)
    elif input_variable_def["type"] == "categorical":
        return CategoricalInputVariable(input_variable_def["column"], prefix=output_name)
    else:
        raise ValueError("'{}' is not one of the allowed variable types".format(feature_df["type"]))
    
    return True