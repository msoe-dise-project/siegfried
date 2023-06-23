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

import unittest

import pandas as pd
from pandas.api.types import is_float_dtype

from siegfried.data_graph import *

class TestDataGraph(unittest.TestCase):
    def setUp(self):
        data = {
            "price" : [50000, 750000, 100000],
            "bedrooms" : [2, 2, 3],
            "bathrooms" : [1, 1.5, 2],
            "type": ["condo", "single_family_home", "single_family_home"]
        }
        self.df = pd.DataFrame(data = data)
        
    def test_numerical_input_variables(self):
        variable_1 = NumericalInputVariable("bedrooms")
        df1 = variable_1.fit_transform(self.df)
        
        self.assertEqual(len(self.df), len(df1))
        self.assertEqual(1, df1.shape[1])
        self.assertEqual(["bedrooms"], df1.columns)
        self.assertTrue(is_float_dtype(df1.dtypes[0]))
        
        variable_2 = NumericalInputVariable("price", output_name="sale_price")
        df2 = variable_2.fit_transform(self.df)
        
        self.assertEqual(len(self.df), len(df2))
        self.assertEqual(1, df2.shape[1])
        self.assertEqual(["sale_price"], df2.columns)
        self.assertTrue(is_float_dtype(df2.dtypes[0]))
        
    def test_categorical_input_variables(self):
        variable_1 = CategoricalInputVariable("bedrooms")
        df1 = variable_1.fit_transform(self.df)
        
        self.assertEqual(len(self.df), len(df1))
        # 2 columns
        self.assertEqual(2, df1.shape[1])
        self.assertEqual(set(df1.columns), set(["bedrooms_2", "bedrooms_3"]))
        self.assertTrue(is_float_dtype(df1.dtypes[0]))
        
        variable_2 = CategoricalInputVariable("price")
        df2 = variable_2.fit_transform(self.df)
        
        self.assertEqual(len(self.df), len(df2))
        # 3 columns
        self.assertEqual(3, df2.shape[1])
        self.assertEqual(set(df2.columns), set(["price_50000", "price_750000", "price_100000"]))
        self.assertTrue(is_float_dtype(df2.dtypes[0]))
        
    def test_concatenate_variables(self):
        variable_1 = NumericalInputVariable("price")
        variable_2 = CategoricalInputVariable("bedrooms")
        variable_3 = ConcatenateVariables([variable_1, variable_2])
        df1 = variable_3.fit_transform(self.df)
        
        self.assertEqual(len(self.df), len(df1))
        # 1 price, 2 bedrooms
        self.assertEqual(3, df1.shape[1])
        self.assertEqual(list(df1.columns), ["price", "bedrooms_2", "bedrooms_3"])
        
    def test_numerical_output_variables(self):
        variable_1 = NumericalOutputVariable("bedrooms")
        series1 = variable_1.fit_transform(self.df)
        
        self.assertEqual(len(series1.shape), 1)
        self.assertEqual(len(self.df), len(series1))
        self.assertTrue(is_float_dtype(series1.dtypes))
        
        variable_2 = NumericalOutputVariable("price")
        series2 = variable_2.fit_transform(self.df)
        
        self.assertEqual(len(series2.shape), 1)
        self.assertEqual(len(self.df), len(series2))
        self.assertTrue(is_float_dtype(series2.dtypes))
        
    def test_categorical_output_variables(self):
        variable_1 = CategoricalOutputVariable("bedrooms")
        series1 = variable_1.fit_transform(self.df)
        
        self.assertEqual(len(series1.shape), 1)
        self.assertEqual(len(self.df), len(series1))
        
        variable_2 = CategoricalOutputVariable("price")
        series2 = variable_2.fit_transform(self.df)
        
        self.assertEqual(len(series2.shape), 1)
        self.assertEqual(len(self.df), len(series2))
        