# %% [markdown]
'''
# Cleaning Data for Preprocessing a Time Series
'''
# %%
from nltk import data
from numpy.lib.shape_base import column_stack
import pandas as pd
import numpy as np
import glob

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
#from sklearn.impute import KNNImputer
from sklearn.preprocessing import OrdinalEncoder
import string
import unidecode
import re
from fancyimpute import KNN
import class_words_all
import complete_stem_words

# %%
class Preprocess():

    def __init__(self, rootDir, word_dict, inv_words):
        self.rootDir_ = rootDir
        self.class_words_dict_ = word_dict
        self.inv_words_dict_ = inv_words
        self.imputer_ = KNN(k=1)
        self.enc_ = OrdinalEncoder()
        self.spanish_stemmer_ = SnowballStemmer('spanish')
        self.special_words_ = ['piez']
        self.stopwords_spanish_ = stopwords.words('spanish')
        self.df_ = pd.DataFrame(columns=['Tipo','Tipo_2','Tipo_3','Tipo_4','Marca','Submarca','Empaque','Contenido','UnidadMedida','LocalidadGeografica','Fuente','precio','fecha'])

        self.data_ = self.import_data()
        self.add_stop_words()
        self.preprocess('descripcion')
        self.categorize()
        self.append_df()
        self.join_marca_submarca_drop_null()
        self.imputation()
        self.inv_words_funct()
        self.drop_unused_columns()

    def import_data(self):
        '''
        Import all files in a library without subfolders
        '''
        data = {}
        path = self.rootDir_+'*.csv'
        for fname in glob.glob(path):
            data[fname.split('\\')[1].split('.csv')[0]] = pd.read_csv(fname, index_col=0)
            try:
                data.get(fname.split('\\')[1].split('.csv')[0])['fecha'] = pd.to_datetime(data.get(fname.split('\\')[1].split('.csv')[0])['fecha'], format='%d-%m-%Y')
            except KeyError:
                print('Check datetime values, as I didnt find them.')
        return data

    def add_stop_words(self):
        new_stop_words = ['s']
        self.stopwords_spanish_.extend(new_stop_words)

        return self

    def tokenize(self,data):
        '''
        Input: the complete strins
        Output: the tokenize string in a list of strings
        '''
        return word_tokenize(data)

    def remove_stopwords_punctuation(self, data):
        clean_description = []
        for word in data:
            if (word not in self.stopwords_spanish_ and
                word not in string.punctuation):
                clean_description.append(word)
        
        return clean_description

    def remove_accents(self,data):

        return [unidecode.unidecode(word) for word in data]

    def lowercasing(self, data):

        return [word.lower() for word in data]

    def stemming(self, data):

        return [self.spanish_stemmer_.stem(word) for word in data]

    def remove_duplicates(self, data):
        seen = set()
        result = []
        for item in data:
            if item not in seen:
                seen.add(item)
                result.append(item)
        
        return result

    def split_number_letter(self, data):
        result = []
        for word in data:
            match = re.match(r'([0-9]+)([a-z]+)', word, re.I)
            if match:
                for element in match.groups():
                    result.append(element)
            else:
                result.append(word)
        return result

    def remove_special_char(self, data):
        result = []
        for word in data:
            if (word not in self.special_words_):
                result.append(word)
        return result

    def preprocess(self, column_name):
        for values in self.data_.values():
            values[column_name] = values.apply(lambda row: self.tokenize(row[column_name]), axis=1)
            values[column_name] = values.apply(lambda row: self.remove_accents(row[column_name]),axis=1)
            values[column_name] = values.apply(lambda row: self.lowercasing(row[column_name]),axis=1)
            values[column_name] = values.apply(lambda row: self.split_number_letter(row[column_name]),axis=1)
            values[column_name] = values.apply(lambda row: self.remove_stopwords_punctuation(row[column_name]),axis=1)
            values[column_name] = values.apply(lambda row: self.stemming(row[column_name]),axis=1)
            values[column_name] = values.apply(lambda row: self.remove_special_char(row[column_name]),axis=1)
            values[column_name] = values.apply(lambda row: self.remove_duplicates(row[column_name]),axis=1)
        return self

    def append_df(self):
        for element in self.data_.keys():
            self.df_ = self.df_.append(self.data_.get(element), ignore_index=True)
                
        return self

    def categorize(self):
        for base_key in self.data_.keys():
            self.data_.get(base_key).reset_index(drop=True,inplace=True)
            columns_to_add = ['Tipo','Tipo_2','Tipo_3','Tipo_4','Marca','Submarca','Empaque','Contenido','UnidadMedida']
            for i in columns_to_add:
                self.data_.get(base_key)[i] = np.nan
            self.data_.get(base_key)['Fuente'] = base_key
            for row in range(len(self.data_.get(base_key))):
                for element in self.data_.get(base_key)['descripcion'][row]:
                    if element in self.class_words_dict_.get('Tipo'):
                        self.data_.get(base_key)['Tipo'].loc[row] = element
                    if element in self.class_words_dict_.get('Tipo_2'):
                        self.data_.get(base_key)['Tipo_2'].loc[row] = element
                    if element in self.class_words_dict_.get('Tipo_3'):
                        self.data_.get(base_key)['Tipo_3'].loc[row] = element
                    if element in self.class_words_dict_.get('Tipo_4'):
                        self.data_.get(base_key)['Tipo_4'].loc[row] = element
                    if element in self.class_words_dict_.get('Marca'):
                        self.data_.get(base_key)['Marca'].loc[row] = element
                    if element in self.class_words_dict_.get('Submarca'):
                        self.data_.get(base_key)['Submarca'].loc[row] = element
                    if element in self.class_words_dict_.get('Empaque'):
                        self.data_.get(base_key)['Empaque'].loc[row] = element
                    if element in self.class_words_dict_.get('Contenido'):
                        self.data_.get(base_key)['Contenido'].loc[row] = element
                    if element in self.class_words_dict_.get('UnidadMedida'):
                        self.data_.get(base_key)['UnidadMedida'].loc[row] = element
                    
        return self
    
    def join_marca_submarca_drop_null(self):
        self.df_['Submarca'].fillna('',inplace=True)
        self.df_['Marca'] = self.df_['Marca'] + self.df_['Submarca']
        self.df_.drop(['Submarca'],axis=1,inplace=True)
        self.df_.dropna(subset=['Tipo'], inplace=True)
        
        return self

    def imputation(self):
        self.df_.fillna('',inplace=True)
        self.df_.reset_index(drop=True, inplace=True)
        for row in range(len(self.df_)):
            if self.df_.Tipo.loc[row] == 'huev' and self.df_.UnidadMedida.loc[row] == '':
                self.df_['UnidadMedida'].loc[row] = 'pz'
            if self.df_.Tipo.loc[row] == 'tortill' and self.df_.UnidadMedida.loc[row] == '':
                self.df_['UnidadMedida'].loc[row] = 'pz'
            if self.df_.Tipo.loc[row] == 'papel' and self.df_.UnidadMedida.loc[row] == '':
                self.df_['UnidadMedida'].loc[row] = 'roll'
            if self.df_.Tipo.loc[row] == 'lech' and self.df_.UnidadMedida.loc[row] == '':
                self.df_['UnidadMedida'].loc[row] = 'l'
            if self.df_.Contenido.loc[row] == '':
                self.df_['Contenido'].loc[row] = '1'
            if self.df_.Marca.loc[row] == '':
                self.df_['Marca'].loc[row] = 'no_especificado'
            if self.df_['Tipo_2'].loc[row] == '':
                if self.df_['Tipo_4'].loc[row] == '' and self.df_['Tipo_3'].loc[row] == '':
                    self.df_['Tipo_2'].loc[row] = 'no_especificado'
                else:
                    if self.df_['Tipo_4'].loc[row] == '':
                        self.df_['Tipo_2'].loc[row] = self.df_['Tipo_3'].loc[row]
                    else:
                        if self.df_['Tipo_3'].loc[row] == '':
                            self.df_['Tipo_2'].loc[row] = self.df_['Tipo_4'].loc[row]
                        else:
                            self.df_['Tipo_2'].loc[row] = self.df_['Tipo_3'].loc[row] + '_' + self.df_['Tipo_4'].loc[row]
            else:
                if self.df_['Tipo_4'].loc[row] == '' and self.df_['Tipo_3'].loc[row] == '':
                    self.df_['Tipo_2'].loc[row] = self.df_['Tipo_2'].loc[row]
                else:
                    if self.df_['Tipo_4'].loc[row] == '':
                        self.df_['Tipo_2'].loc[row] = self.df_['Tipo_2'].loc[row] + '_' + self.df_['Tipo_3'].loc[row]
                    else:
                        if self.df_['Tipo_3'].loc[row] == '':
                            self.df_['Tipo_2'].loc[row] = self.df_['Tipo_2'].loc[row] + '_' + self.df_['Tipo_4'].loc[row]
                        else:
                            self.df_['Tipo_2'].loc[row] = self.df_['Tipo_2'].loc[row] + '_' + self.df_['Tipo_3'].loc[row] + '_' + self.df_['Tipo_4'].loc[row]
        self.knn_imputer_for_empaque()

        return self
    def knn_imputer_for_empaque(self):
        data = self.df_.copy(deep=True)
        data['Empaque'][(data['Empaque']=='')] = np.nan
        # initialize variables
        ordinal_enc_dict = {}
        columns_to_encode = ['Tipo','Tipo_2','Empaque']
        # loop over columns to encode
        for col_name in data[columns_to_encode]:
            # create ordinal encoder for the column
            ordinal_enc_dict[col_name] = OrdinalEncoder()
            # select the non-null values in the column
            col = data[col_name]
            col_not_null = col[col.notnull()]
            reshaped_vals = col_not_null.values.reshape(-1,1)
            # encode the non-null values of the column
            encoded_vals = ordinal_enc_dict[col_name].fit_transform(reshaped_vals)
            # store the values to non-null values of the column in data
            data.loc[col.notnull(), col_name] = np.squeeze(encoded_vals)
        # imputing with KNN
        data.iloc[:,[data.columns.get_loc(col_) for col_ in columns_to_encode]] = np.round(self.imputer_.fit_transform(data[columns_to_encode]))
        for col_name in data[columns_to_encode]:
            # reshape the data
            reshaped = data[col_name].values.reshape(-1,1)
            # perform inverse transformation of the ordinally encoded columns
            data[col_name] = ordinal_enc_dict[col_name].inverse_transform(reshaped)
        
        self.df_ = data.copy(deep=True)
       
        return self

    def search_in_dict(self, data):
        for key, value in self.inv_words_dict_.items():
            for i in value:
                if i == data:
                    return key
                else:
                    pass
        return data
    
    def inv_words_funct(self):
        column_name = ['Tipo','Tipo_2','Marca','Empaque','UnidadMedida','Contenido']
        for element in column_name:
            self.df_[element] = self.df_.apply(lambda row: self.search_in_dict(row[element]), axis=1)
        return self
    
    def drop_unused_columns(self):
        columns_to_drop = ['descripcion','producto','LocalidadGeografica','Tipo_3','Tipo_4']
        self.df_.drop(columns_to_drop, axis=1, inplace=True)

        return self
# %% 
rootDir = 'Dataset/'
clean_class = Preprocess(rootDir=rootDir, word_dict=class_words_all.class_words_dict, inv_words=complete_stem_words.inv_class_words)
# %%
clean_class.df_
# %%
clean_class.df_.to_csv('clean_data.csv', index=False)