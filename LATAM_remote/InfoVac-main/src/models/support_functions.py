import numpy as np
import unicodedata
import re
import nltk
import unicodedata
import es_core_news_md

from nltk.corpus import stopwords
from sklearn.base import BaseEstimator, TransformerMixin

nlp = es_core_news_md.load()

def load_stopwords():
    # Build stop words list
    stop_words_es = stopwords.words('spanish')  # Spanish's stop words
    stop_words_es = stop_words_es + ['cnn', 'mas', 'si']
    sw_es = nlp.Defaults.stop_words
    stop_words_es = sw_es.union(stop_words_es)
    return stop_words_es


def normalize_document(doc:str, rm_sw:bool=True, rm_symb:bool=True, lemmatize:bool=True) -> str:
    """
    Cleans text including removal of whitespace, punctuation, accented characters,
    special characters and transforming to lowercase. Assumes input text is string.
    Returns clean string.
    """
    stop_words_es = load_stopwords()

    # lower case and remove special characters\whitespaces
    if rm_symb:
      # Remove accents
      doc = unicodedata.normalize(u'NFKD', doc)\
                       .encode('ascii', 'ignore')\
                       .decode('utf8')
      # Remove numbers and punctuations
      doc = re.sub(r'[^a-zA-Z\s]', '', doc)
    # To lowercase
    doc = doc.lower()
    # Remove extra space
    doc = doc.strip()

    if rm_sw:
      # tokenize document
      tokens = nltk.word_tokenize(doc)
      # filter stopwords out of document
      filtered_tokens = [token for token in tokens if token not in stop_words_es]
      # re-create document from filtered tokens
      doc = ' '.join(filtered_tokens)

    if lemmatize:
      doc = nlp(doc)
      tokens = [token.lemma_.strip() for token in doc]
      doc = ' '.join(tokens)

    return doc


normalize_corpus = np.vectorize(normalize_document)


class NormalizeTextTransformer(BaseEstimator, TransformerMixin):
    def __init__(self, rm_sw, rm_symb, lemmatize):
        self.rm_sw = rm_sw
        self.rm_symb = rm_symb
        self.lemmatize = lemmatize

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X_norm = normalize_corpus(X, rm_sw=self.rm_sw,  rm_symb=self.rm_symb, lemmatize=self.lemmatize)
        return X_norm
