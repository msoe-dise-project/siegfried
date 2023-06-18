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

import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder

all = ["Variable", "CategoricalInputVariable", "NumericalVariable", "ConcatenateVariables",
       "CategoricalOutputVariable", "OutputVariable", "DataGraph"]

class Variable:
    def __init__(self, column_name, output_name = None):
        self.column_name = column_name
        if output_name is None:
            output_name = column_name
        self.output_name = output_name
        
    def fit_transform(self, df):
        return self.transform(df)
    
    def transform(self, df):
        df = df[[self.column_name]]
        df.columns = [self.output_name]
        return df
        
class CategoricalInputVariable:
    def __init__(self, parent, prefix=None):
        self.prefix = prefix
        self.parent = parent
    
    def fit_transform(self, df):
        parent_df = self.parent.fit_transform(df)
        self.encoder = OneHotEncoder(sparse_output=False).set_output(transform="pandas")
        dummies_df = self.encoder.fit_transform(parent_df)
        if self.prefix is None:
            self.prefix = parent_df.columns[0]
        dummies_df.columns = [self.prefix + "_" + c for c in dummies_df.columns]
        return dummies_df
        
    def transform(self, df):
        parent_df = self.parent.transform(df)
        dummies_df = self.encoder.transform(parent_df)
        dummies_df.columns = [self.prefix + "_" + c for c in dummies_df.columns]
        return dummie_df
        
class NumericalVariable:
    def __init__(self, parent, output_name=None):
        self.output_name = output_name
        self.parent = parent
    
    def fit_transform(self, df):
        return self.transform(df)
    
    def transform(self, df):
        parent_df = self.parent.transform(df)
        df = parent_df.astype("float32")
        if self.output_name is not None:
            df.columns = [self.output_name]
        return df
        
class ConcatenateVariables:
    def __init__(self, parents):
        self.parents = parents
        
    def fit_transform(self, df):
        return self.transform(df)
    
    def transform(self, df):
        parent_outputs = []
        for parent in self.parents:
            parent_name, parent_df = parent.get(df)
            parent_outputs.append(parent_df)
        # stack horizontally
        return pd.concat(parent_outputs, axis=1)
        
class CategoricalOutputVariable:
    def __init__(self, output_name, parent):
        self.output_name = output_name
        self.parent = parent
    
    def fit_transform(self, df):
        parent_name, parent_df = self.parent.get(df)
        self.label_encoder = LabelEncoder().set_output(transform="pandas")
        encoded_df = self.label_encoder.fit_transform(parent_df)
        output_df = encoded_df.rename({ self.column_name : self.output_name })
        return (self.output_name, encoded_df)
        
    def transform(self, df):
        parent_name, parent_df = self.parent.get(df)
        encoded_df = self.label_encoder.fit_transform(parent_df)
        output_df = encoded_df.rename({ self.column_name : self.output_name })
        return (self.output_name, encoded_df)

class OutputVariable:
    def __init__(self, output_name, parent):
        self.output_name = output_name
        self.parent = parent
    
    def fit_transform(self, df):
        return self.transform(df)
        
    def transform(self, df):
        parent_name, parent_df = self.parent.get(df)
        series = parent_df[parent_name]
        return (self.output_name, series)
        
class DataGraph:
    def __init__(self, input_graph, output_graph):
        self.input_graph = feature_graph
        self.output_graph = output_graph
        
    def fit_transform(self, X, y):
        input_df = self.input_graph.fit_transform(X)
        output_series = self.output_graph.fit_transform(y)
        return input_df, output_series
    
    def transform(self, X, y):
        input_df = self.input_graph.transform(X)
        output_series = self.output_graph.transform(y)
        return input_df, output_series
    
