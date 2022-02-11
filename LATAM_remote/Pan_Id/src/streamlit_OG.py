# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 19:12:05 2022

@author: franc
"""

import pandas as pd
import numpy as np
import streamlit as st
import string
import nltk
from nltk.corpus import stopwords
import joblib
from nltk.stem import WordNetLemmatizer
import os
from num2words import num2words
import json
from PIL import Image

#%%

image = Image.open('Totem.jpeg')

st.image(image, width=200)

#st.title("TOTEM AI")

st.subheader("Analyze a chat and predict if the text is safe or not")

texto = st.text_area("Copy/paste the chat text in this section.", height=300)

texto = str(texto)

#%% Cleaning

df = pd.Series(data = [texto], index = [0])

df_conv = df.apply(lambda x: x.lower().replace('|', ' '))
print(df_conv)

df_conv = df_conv.apply(lambda x: ' '.join([num2words(word) if word.isnumeric() and int(word)<1000000000 else word for message in x.split('|') for word in message.split(' ')]))
print(df_conv)

df_conv = df_conv.apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))
print(df_conv)

with open('abbreviations.json', 'r') as fp:
    abbr_dict = json.load(fp)

df_conv = df_conv.apply(lambda x: ' '.join([abbr_dict[word] if word in abbr_dict.keys() else word for word in x.split(' ') ]))

stop = stopwords.words('english')
df_conv = df_conv.apply(lambda x: ' '.join([word for word in x.split() if word not in (stop)]))

df_conv = df_conv.apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))

df_conv = df_conv.apply(lambda x: ' '.join([word for word in x.split(' ') if word.isalpha()]))


wordnet_lemmatizer = WordNetLemmatizer()
df_conv = df_conv.apply(lambda x: ' '.join([wordnet_lemmatizer.lemmatize(word, pos='v') for word in x.split(' ')]))

vectorizer = joblib.load(os.path.join(os.getcwd(), "vectorizer.joblib"))
model = joblib.load(os.path.join(os.getcwd(), "modeloOG.joblib"))

Xtest = vectorizer.transform(df_conv)
#%%

prediction = model.predict(Xtest)

st.button("Analize")

if prediction == 1:
    text2print = "STRANGER DANGER!!!"
    st.error(text2print)
else:
    text2print = "Normal Chat"
    st.success(text2print)
    
#st.write("The text is:")
#st.write(text2print)
