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

all = ["CategoricalInputVariable", "NumericalInputVariable", "ConcatenateVariables",
       "CategoricalOutputVariable", "NumericalOutputVariable", "DataGraph"]
        
class CategoricalInputVariable:
    def __init__(self, column_name, prefix=None):
        self.column_name = column_name
        if prefix is None:
            prefix = column_name
        self.prefix = prefix
    
    def fit_transform(self, df):
        df = df[[self.column_name]]
        df.columns = [self.prefix]
        self.encoder = OneHotEncoder(sparse_output=False).set_output(transform="pandas")
        dummies_df = self.encoder.fit_transform(df)
        return dummies_df
        
    def transform(self, df):
        df = df[[self.column_name]]
        dummies_df = self.encoder.transform(df)
        return dummie_df
        
class NumericalInputVariable:
    def __init__(self, column_name, output_name=None):
        self.column_name = column_name
        self.output_name = output_name
    
    def fit_transform(self, df):
        df = df[[self.column_name]]
        df = df.astype("float32")
        if self.output_name is not None:
            df.columns = [self.output_name]
        return df
    
    def transform(self, df):
        df = df[[self.column_name]]
        df = df.astype("float32")
        if self.output_name is not None:
            df.columns = [self.output_name]
        return df
        
class ConcatenateVariables:
    def __init__(self, parents):
        self.parents = parents
        
    def fit_transform(self, df):
        parent_outputs = []
        for parent in self.parents:
            parent_df = parent.fit_transform(df)
            parent_outputs.append(parent_df)
        # stack horizontally
        return pd.concat(parent_outputs, axis=1)
    
    def transform(self, df):
        parent_outputs = []
        for parent in self.parents:
            parent_df = parent.transform(df)
            parent_outputs.append(parent_df)
        # stack horizontally
        return pd.concat(parent_outputs, axis=1)
        
class CategoricalOutputVariable:
    def __init__(self, column_name):
        self.column_name = column_name
    
    def fit_transform(self, df):
        series = df[self.column_name]
        self.label_encoder = LabelEncoder()
        encoded_series = pd.Series(self.label_encoder.fit_transform(series.values))
        return encoded_series
        
    def transform(self, df):
        series = df[self.column_name]
        encoded_series = pd.Series(self.label_encoder.transform(series.values))
        return encoded_series

class NumericalOutputVariable:
    def __init__(self, column_name):
        self.column_name = column_name
    
    def fit_transform(self, df):
        series = df[self.column_name]
        series = series.astype("float32")
        return series
        
    def transform(self, df):
        series = df[self.column_name]
        series = series.astype("float32")
        return series
        
class DataGraph:
    def __init__(self, input_graph, output_graph):
        self.input_graph = input_graph
        self.output_graph = output_graph
        
    def fit_transform(self, df):
        input_df = self.input_graph.fit_transform(df)
        output_series = self.output_graph.fit_transform(df)
        return input_df, output_series
    
    def transform(self, df):
        input_df = self.input_graph.transform(df)
        output_series = self.output_graph.transform(df)
        return input_df, output_series
