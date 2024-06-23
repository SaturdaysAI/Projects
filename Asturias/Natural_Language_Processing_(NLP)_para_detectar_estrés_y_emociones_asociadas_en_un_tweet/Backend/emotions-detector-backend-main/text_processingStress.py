import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize
import re


emojis = {':)': 'smile', ':-)': 'smile', ';d': 'wink', ':-E': 'vampire', ':(': 'sad',
          ':-(': 'sad', ':-<': 'sad', ':P': 'raspberry', ':O': 'surprised',
          ':-@': 'shocked', ':@': 'shocked',':-$': 'confused', ':\\': 'annoyed',
          ':#': 'mute', ':X': 'mute', ':^)': 'smile', ':-&': 'confused', '$_$': 'greedy',
          '@@': 'eyeroll', ':-!': 'confused', ':-D': 'smile', ':-0': 'yell', 'O.o': 'confused',
          '<(-_-)>': 'robot', 'd[-_-]b': 'dj', ":'-)": 'sadsmile', ';)': 'wink',
          ';-)': 'wink', 'O:-)': 'angel','O*-)': 'angel','(:-D': 'gossip', '=^.^=': 'cat'}

# Función para preprocesar el texto en crudo
def preprocess(text):
    # Crear stemmer.
    stemmer = SnowballStemmer(language='english')

    # Crear lista de stopwords
    en_stop = stopwords.words('english')

    # Definir patrones para reemplazar/eliminar.
    urlPattern        = r"((http://)[^ ]*|(https://)[^ ]*|( www\.)[^ ]*)"
    userPattern       = '@[^\s]+'
    alphaPattern      = "[^a-zA-Z0-9]"
    sequencePattern   = r"(.)\1\1+"
    seqReplacePattern = r"\1\1"

    # Lower Casing
    text = text.lower()
    # Reemplazar URLs
    text = re.sub(urlPattern,' URL', text)
    # Reemplazar emojis.
    for emoji in emojis.keys():
        text = text.replace(emoji, "EMOJI" + emojis[emoji])
    # Reemplazar @Nombres con 'USER'.
    text = re.sub(userPattern,' USER', text)
    # Reemplazar non-alphabets.
    text = re.sub(alphaPattern, " ", text)
    # Reemplazar letras consecutivas.
    text = re.sub(sequencePattern, seqReplacePattern, text)

    # Tokenizar texto
    tokens = word_tokenize(text)

    # Eliminar palabras con menos de dos letras
    tokens = [word for word in tokens if len(word)>2]

    # Eliminar stopwords
    tokens = [word for word in tokens if word not in en_stop]

    # Aplicar stemmer o "stemmizar"
    tokens = [stemmer.stem(word) for word in tokens]

    return tokens