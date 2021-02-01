import pandas as pd
import numpy as np
import emoji 
import nltk
import es_core_news_md
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer

class nlpClass:
    def __init__(self): 
        nltk.download('wordnet')
        nltk.download('punkt')
        self.name = "Clase para NLP - problemas en el cloud"
        self.tokenizer = RegexpTokenizer(r'\w+')
        self.sw = stopwords.words('spanish')
        self.lemmatizer = WordNetLemmatizer()
        self.nlp_ = es_core_news_md.load() 
    
    def char_is_emoji(self,character):
        return character in emoji.UNICODE_EMOJI
    
    def text_has_emoji(self, text):
        for character in text:
            if character in emoji.UNICODE_EMOJI:
                return True
        return False
    
    def applyBrand_subjectLine(self, s):
            if 'bion' in s or 'oral' in s or 'braun' in s  or 'unstop' in s or 'gille' in s or 'kukid' in s or 'venu' in s or 'evax' in s or 'pro' in s or 'discreet' in s or 'platin' in s or 'ausoni' in s or 'olay' in s or 'fair' in s or 'lenor' in s or 'don lim' in s or 'ambipur' in s or 'tampax' in s or 'zzzqui' in s  or 'ariel' in s  or 'swiffe' in s:
                return 1
            else:
                return 0
            
    def applyRet_subjectLine(self, s):
            if 'carref' in s or 'aldi' in s or 'amazon' in s  or 'mercad' in s:
                return 1
            else:
                return 0
            
    def process_message(self, message, lower_case = True, lemmat = False, stem = True, stop_words = True, gram = 1):
        #(message, lower_case = True, stem = True, stop_words = True, gram = 1):
        message = str(message)
        if lower_case:
            message = message.lower()    
        words = self.tokenizer.tokenize(message)
        words = [w for w in words if len(w) > 2]
        if gram > 1:
            w = []
            for i in range(len(words) - gram + 1):
                w += [' '.join(words[i:i + gram])]
            return w
        if stop_words:
            words = [word for word in words if word not in self.sw]
        #Al no ser texto excesivamente voluminoso, OK con lemmatización y no estammatización
        if lemmat:
            pruebas = ' '.join(words)
            pruebas_ = []
            for pru in self.nlp_(pruebas):
                pruebas_.append(pru.lemma_)
            words = pd.Series(pruebas_)
            words = words.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
            words = words.tolist()
            #words = [self.lemmatizer.lemmatize(word) for word in words]   
        if stem:
            stemmer = PorterStemmer()
            words = [stemmer.stem(word) for word in words]   
        words = ' '.join(words) # Si queremos hacer la parte de la lista, tenemos que quitar esta linea
        return words
    
    def convert_arry(self, message):
        words = self.tokenizer.tokenize(message)
        return words
    
    def process_message_list(self, message, lower_case = True, lemmat = True, stem = False, stop_words = True, gram = 1):
        #(message, lower_case = True, stem = True, stop_words = True, gram = 1):
        message = str(message)
        if lower_case:
            message = message.lower()    
        words = self.tokenizer.tokenize(message)
        words = [w for w in words if len(w) > 2]
        if gram > 1:
            w = []
            for i in range(len(words) - gram + 1):
                w += [' '.join(words[i:i + gram])]
            return w
        if stop_words:
            words = [word for word in words if word not in self.sw]
        #Al no ser texto excesivamente voluminoso, OK con lemmatización y no estammatización
        if lemmat:            
            #words = [self.lemmatizer.lemmatize(word) for word in words]   
            pruebas = ' '.join(words)
            pruebas_ = []
            for pru in self.nlp_(pruebas):
                pruebas_.append(pru.lemma_)
            words = pd.Series(pruebas_)
            words = words.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
            words = words.tolist()
        if stem:
            stemmer = PorterStemmer()
            words = [stemmer.stem(word) for word in words]   
        return words
    
    def create_keywords(self, dff, colname):
        lista = list(dff[colname])
        flat_list = [item for sublist in lista for item in sublist]
        flat_list = set(flat_list)
        flat_list = list(flat_list)
        flat_list = pd.DataFrame(flat_list) 
        flat_list.columns = ['keyword']
        flat_list.to_csv('keywords_s1.csv', index=False, encoding='latin-1',)
        
    def bag_of_words(self, dff, colname):
        data = dff[colname]
        matrix = CountVectorizer()
        X = matrix.fit_transform(data)
        dfa = pd.DataFrame(X.toarray())
        dfa.columns = matrix.get_feature_names()
        df_f = pd.concat([dff,dfa], axis=1)
        return df_f
    
    def tfidf(self, dff, colname):
        data = dff[colname]
        matrix = TfidfVectorizer()
        X = matrix.fit_transform(data)
        dfa = pd.DataFrame(X.toarray())
        dfa.columns = matrix.get_feature_names()
        df_f = pd.concat([dff,dfa], axis=1)
        return df_f
                
    