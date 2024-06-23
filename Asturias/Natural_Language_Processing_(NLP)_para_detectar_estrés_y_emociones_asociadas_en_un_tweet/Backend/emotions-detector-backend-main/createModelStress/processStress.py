import pandas as pd
import ast
from text_processingStress import preprocess
from calcular_vector import get_w2v_vectors

from langdetect import detect
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import joblib


print("Lee CSV")
# Leemos el CSV que contiene los datos y lo cargamos en memoria
df = pd.read_csv('./Twitter_Stress.csv', sep=";")

df = df.drop(df.columns[[1, 3, 4]],axis = 1)
df['text'] = df['text'].astype("string")
df = df.dropna(axis=0)
df['language'] = df['text'].apply(detect)
df = df[df['language']=='en']
df['word_count'] = df['text'].apply(lambda x: len(x.split()))
df['preprocess_text'] = df['text'].apply(preprocess)

df['text_vector'] = df['preprocess_text'].apply(get_w2v_vectors)

print("Pasar a otro csv")
df.to_csv('./base de conocimiento.csv', index=False)


def loadlist(cadena):
  t= cadena[1:-1].replace('\n','')
  t=' '.join(t.split()).replace(' ',',')
  t='['+t+']'
  t = ast.literal_eval(t)
  return t

df1 = pd.read_csv('./base de conocimiento.csv',converters={'text_vector': loadlist})

train_set, test_set = train_test_split(df1, test_size=0.20, random_state=0)

X_train = list(train_set['text_vector'])
y_train = train_set['labels']

print("Training")
gb_clf3 = GradientBoostingClassifier(n_estimators=200, learning_rate=0.3, max_depth=3, random_state=0)
gb_clf3.fit(X_train, y_train)


print("Saving")
joblib.dump(gb_clf3, 'gb_clf3_model.joblib')

