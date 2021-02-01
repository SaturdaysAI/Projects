# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

class criteoClass: 
    
    def __init__(self): 
        self.name = "Clase para poner a punto del dataset de Criteo"    
        
    def map_one_hot(self, df, column_names, result_column_name):
        mapper = {} 
        for i, col_name in enumerate(column_names):
            for val in df[col_name].unique():
                mapper[str(val) + str(i)] = len(mapper)
             
        df_ext = df.copy()
        
        def one_hot(values):
            v = np.zeros( len(mapper) )
            for i, val in enumerate(values): 
                v[ mapper[str(val) + str(i)] ] = 1
            return v    
        
        df_ext[result_column_name] = df_ext[column_names].values.tolist()
        df_ext[result_column_name] = df_ext[result_column_name].map(one_hot)
        
        return df_ext
    
    def features_for_modelling(self, df):
    
        def pairwise_max(series):
            return np.max(series.tolist(), axis = 0).tolist()
          
        def scalar (df):
            min_max_scaler = MinMaxScaler()
            for cname in ('click', 'cost', 'conversion'):
                x = df[cname].values.reshape(-1, 1) 
                df[cname] = min_max_scaler.fit_transform(x)    
            return df
        
        aggregation = {
            'campaigns': pairwise_max,
            'cats': pairwise_max,
            'click': 'sum',
            'cost': 'sum',
            'conversion': 'max'
        }
        df_agg = df.groupby(['jid']).agg(aggregation)
        df_agg = scalar(df_agg)
        
        df_agg['features'] = df_agg[['campaigns', 'cats', 'click', 'cost']].values.tolist()
        
        return (
            np.stack(df_agg['features'].map(lambda x: np.hstack(x)).values),
            df_agg['conversion'].values
        )