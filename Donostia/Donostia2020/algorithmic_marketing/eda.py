import pandas as pd
import numpy as np

class EDAClass:
    def __init__(self, df, nombre, descripcion):
        self.df = df
        self.nombre = nombre
        self.descripcion = descripcion
        print("Cargado dataframe: " + nombre)
 
    
    def fillna_eda(self, lista, values):
        for i in range(0, len(lista)):
            self.df[lista[i]] = self.df[lista[i]].fillna(values[i])
        return self.df
    
    def get_null_cols (self):
        return list(self.df[self.df.columns[self.df.isna().any()]].columns)
    
    def render_null_cols(self):
        print('Dataframe '+ self.nombre+ ' - Null columns '+ str(list(self.df[self.df.columns[self.df.isna().any()]].columns)))
        
    
    