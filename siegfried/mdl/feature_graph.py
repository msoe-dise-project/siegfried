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

class InputFeature:
    def __init__(self, output_name, column_name):
        self.output_name = output_name
        self.column_name = column_name
    
    def get(self, df):
        df = df[[self.column_name]]
        df = df.rename({ self.column_name : self.output_name })
        return (self.output_name, df)
        
class CategoricalFeature:
    def __init__(self, output_name, parent):
        self.output_name = output_name
        self.parent = parent
    
    def get(self, df):
        parent_name, parent_df = self.parent.get(df)
        dummies_df = pd.get_dummies(parent_df,
                                    prefix=self.output_name)
        return (self.output_name, dummies_df)
        
class NumericalFeature:
    def __init__(self, output_name, parent):
        self.output_name = output_name
        self.parent = parent
    
    def get(self, df):
        parent_name, parent_df = self.parent.get(df)
        output_df = parent_df.astype("float32")
        return (self.output_name, output_df)
        
class ConcatenateFeatures:
    def __init__(self, parents):
        self.parents = parents
    
    def get(self, df):
        parent_outputs = []
        for parent in self.parents:
            parent_name, parent_df = parent.get(df)
            parent_outputs.append(parent_df)
        # stack horizontally
        return pd.concat(parent_outputs, axis=1)
