# -*- coding: utf-8 -*-
import logging
import pandas as pd
import re

from datetime import datetime
from unidecode import unidecode
from pathlib import Path
from dotenv import find_dotenv, load_dotenv

COVID_WORDS = ['covid', 'coronavirus', 'vacuna', 'virus',
               'pandemia', 'sars-cov', 'cuarentena', 'infectado',
               'salud', 'oms', 'hospital', 'medico', 'dioxido', 'cloro',
               'termometro', 'infrarojo',
               'asinto', 'pcr', 'mascar', 'tapaboca', 'cubreboca', 'oximetro',
               'respira', 'contagi', 'desinfecta', 'dieta']

NORMALIZED_COLNAMES = {
      "url": ["url", "link al chequeo"],
      "titulo": ["title", "titulo"],
      "texto": ["text", "descripcion"],
      "categoria": ["textualRating", "calificacion"],
      # "fecha_revision": ["reviewDate", "fecha del chequeo"],
      "fecha_aparicion": ["reviewDate", "fecha del chequeo", 'date'],
      "organizacion": ["publisher.name", "organizacion", 'sitename']
      }

REMOVE_CNN_WORDS = ["Minuto a minuto", "panorama mundial:",  "cosas que debes saber",
                    "encuesta cnn:", "exclusiva de cnn:", "Ver más artículos de opinión sobre CNN",
                    "CNN Español", "CNN Radio Argentina",  "\(CNN\)", "\| cnn",
                    "\#encuentrodigitalcnn",  "Ver más opinión en CNNe\.com\/opinion",
                    "CNN Radio", "nota del editor",  "OPINIÓN \|", "OPINIÓN:", "\[opinión\]", "\(opinión\)",
                    "ANÁLISIS:", "ANÁLISIS \|", "\(análisis\)",
                    "Lea más notas como esta en cnne\.com\/opinión", ]
REMOVE_CNN_WORDS = [word.lower() for word in REMOVE_CNN_WORDS]
EXCLUSIONS = '(' + '|'.join(REMOVE_CNN_WORDS) + ')'

DATA_ROOT_PATH = Path('../../data')
RAW_DATA_PATH = DATA_ROOT_PATH/'raw'


def out_of_context(row: pd.Series) -> bool:
    """ Función que dado un título y una descripción, devuelve
    un booleano indicando si está fuera de contexto o no lo está """
    title, text = row['title'], row['text']
    for w in COVID_WORDS:
        if (w in unidecode(text).lower()) or (w in unidecode(title).lower()):
            return False
    return True


def remove_cnn_words(text):
    return re.sub(EXCLUSIONS, '', text.lower(), flags=re.M)


def extract_date_from_url(url: str) -> str:
    """ Función que extrae una fecha dado una url del dominio maldita.es/malditobulo/2020 """
    splited_text = url.split('/')
    if len(splited_text) > 5:
        return '/'.join(splited_text[4:7])
    return ' '


def change_colnames(column):
    for k, v in NORMALIZED_COLNAMES.items():
        if column in v:
            return k
    return column


def build_google_facts() -> pd.DataFrame:
    dfs = list(RAW_DATA_PATH.glob('google_*'))
    df = pd.concat([pd.read_csv(data) for data in dfs])
    # df = pd.read_csv('../../data/raw/google_facts_api.csv')
    # Removing duplicates
    df.drop_duplicates('title', keep='first', inplace=True)
    # Filling missing text and titles
    df['title'].fillna('no title', inplace=True)
    df['text'].fillna('no text', inplace=True)
    # Removing news out of context
    df['out_of_context'] = df.apply(lambda row: out_of_context(row), axis=1)
    df = df[~df['out_of_context']]

    # Leading with dates
    rows_missing_date = df['reviewDate'].isnull()
    df.loc[rows_missing_date, 'reviewDate'] = df[rows_missing_date]['url'].apply(extract_date_from_url)
    df.loc[104, 'reviewDate'] = '2020/07/22'

    # Convert to datetime
    df['reviewDate'] = pd.to_datetime(df['reviewDate'], yearfirst=True, utc=True, errors='coerce')
    return df

def build_chequeado() -> pd.DataFrame:
    df = pd.read_csv('../../data/raw/chequeado_articles.csv', na_values=' ')
    df = df.convert_dtypes()
    # Removing duplicates
    df.drop_duplicates('descripcion', keep='first', inplace=True)
    # Dealing with missing values
    df['calificacion'].fillna('confiable', inplace=True)
    # Manual fix
    df.loc[3052, 'calificacion'] = df.loc[3052, 'descripcion']
    df.loc[3052, 'descripcion'] = df.loc[3052, 'fecha del chequeo']
    df.loc[3052, 'link a la desinformacion'] = df.loc[3052, 'fecha deteccion desinformacion']
    df.loc[3052, 'fecha del chequeo'] = df.loc[3052, 'organizacion']

    df.loc[1314, 'calificacion'] = df.loc[1314, 'descripcion']
    df.loc[1314, 'descripcion'] = df.loc[1314, 'fecha del chequeo']
    df.loc[1314, 'link a la desinformacion'] = df.loc[1314, 'fecha deteccion desinformacion']
    df.loc[1314, 'fecha del chequeo'] = df.loc[1314, 'organizacion']
    # Filling <NA> using organizacion column
    df['fecha del chequeo'].fillna(df['organizacion'], inplace=True)
    # Convert to 'datetime'
    df['fecha del chequeo'] = pd.to_datetime(df['fecha del chequeo'], dayfirst=True, errors='coerce')
    # Fixing dates manually
    df.loc[2607, 'fecha del chequeo'] = pd.to_datetime('2020/07/22')
    df.loc[1345, 'fecha del chequeo'] = pd.to_datetime('2020/05/10')
    df.loc[1346, 'fecha del chequeo'] = pd.to_datetime('2020/05/10')
    df.loc[1347, 'fecha del chequeo'] = pd.to_datetime('2020/05/10')

    return df


def build_cnn() -> pd.DataFrame:
    df = pd.read_csv('../../data/raw/cnn_articles.csv', encoding='latin-1', na_values=' ')
    df = df.convert_dtypes()
    # Removing duplicates
    df.drop_duplicates('title', keep='first', inplace=True)
    # Dealing with missing values
    df['author'].fillna('CNN', inplace=True)
    df['date'].fillna('2020-03-16', inplace=True)
    # Removing news out of context
    df['out_of_context'] = df.apply(lambda row: out_of_context(row), axis=1)
    df = df[~df['out_of_context']]
    # Removing CNN WORDS
    df['text'] = df['text'].apply(remove_cnn_words)
    df['title'] = df['title'].apply(remove_cnn_words)
    # Dealing with dates
    df['date'] = pd.to_datetime(df['date'], yearfirst=True)
    to_drop = df['date'] < pd.to_datetime('2020/01/01')
    df = df[~to_drop]

    return df

def main():
    """ Runs data processing scripts to turn raw data from (../raw) into
        cleaned data ready to be analyzed (saved in ../processed).
    """
    logger = logging.getLogger(__name__)
    logger.info('making final data set from raw data')

    df_google = build_google_facts()
    df_cheq = build_chequeado()
    df_cnn = build_cnn()
    [df.rename(columns=change_colnames, inplace=True) for df in [df_google, df_cheq, df_cnn]]
    columns = NORMALIZED_COLNAMES.keys()
    df = pd.concat([df_google[columns].copy(),
                    df_cheq[columns].copy(),
                    df_cnn[columns].copy()])

    # Normalizing the categories into 'confiable' and 'no confiable'
    confiable = ['Cierto ', 'Cierto, pero ', 'No es Fake ', 'Verdad', 'Verdad ',
                 'Verdadero', 'Verdadero ', 'Verdadero pero...', 'Verdadero, pero ',
                 'Verificamos', 'confiable']

    # Make the transformation
    df['categoria'] = df['categoria'].apply(lambda x: 'confiable' if x in confiable else 'no confiable')

    # Llenando textos faltantes
    df.loc[df['texto'] == 'no text', 'texto'] = \
        df.loc[df['texto'] == 'no text', 'titulo']

    df['texto'].fillna(df['titulo'], inplace=True)
    # Eliminando duplicados
    df.drop_duplicates('texto', inplace=True)

    # Save the final dataset
    c_day = datetime.now().strftime('%d_%h_%Y_%H_%M')
    df.to_csv(f'../../data/processed/covid_fakenews_es_utf_{c_day}.csv', index=False, encoding='utf-8')



if __name__ == '__main__':
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)

    # not used in this stub but often useful for finding various files
    project_dir = Path(__file__).resolve().parents[2]

    # find .env automagically by walking up directories until it's found, then
    # load up the .env entries as environment variables
    load_dotenv(find_dotenv())

    main()
