# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 19:12:05 2022

@author: franc
"""

import pandas as pd
import numpy as np
import streamlit as st
import tensorflow as tf
import tensorflow_text as text
import tensorflow_hub as hub
from official.nlp import optimization
import string
import nltk

#%%
st.title("ME GUSTA EL HELADO")

st.subheader("Analyze a chat and predict if the text is safe or not")

texto = st.text_area("Copy/paste the chat text in this section.", height=300)

texto = str(texto)

#%%


tfhub_handle_encoder = 'https://tfhub.dev/tensorflow/small_bert/bert_en_uncased_L-4_H-512_A-8/2'
tfhub_handle_preprocess = 'https://tfhub.dev/tensorflow/bert_en_uncased_preprocess/2'

def build_classifier_model():

    #We first preprocess the text which creates the tokens, then encode, which will
    #be the numeric input to the classifier layer
    text_input = tf.keras.layers.Input(shape = (), dtype = tf.string, name = 'text')
    preprocessing_layer = hub.KerasLayer(tfhub_handle_preprocess, name = 'preprocessing')
    encoder_inputs = preprocessing_layer(text_input)
    encoder = hub.KerasLayer(tfhub_handle_encoder, trainable=True, name = 'BERT_encoder')
    outputs = encoder(encoder_inputs)
    net = outputs['pooled_output']
    net = tf.keras.layers.Dropout(0.1)(net)
    net = tf.keras.layers.Dense(1, activation = None, name = 'classifier')(net)
    
    return tf.keras.Model(text_input, net)

model = build_classifier_model()

# Restore the weights
model.load_weights('saved_model/my_checkpoint')

#%% Cleaning

df = pd.Series(data = [texto], index = [0])

df_conv = df.apply(lambda x: x.lower().replace('|', ' '))
print(df_conv)

from num2words import num2words
df_conv = df_conv.apply(lambda x: ' '.join([num2words(word) if word.isnumeric() and int(word)<1000000000 else word for message in x.split('|') for word in message.split(' ')]))
print(df_conv)

df_conv = df_conv.apply(lambda x: x.translate(str.maketrans('', '', string.punctuation)))
print(df_conv)


import json
with open('abbreviations.json', 'r') as fp:
    abbr_dict = json.load(fp)

df_conv = df_conv.apply(lambda x: ' '.join([abbr_dict[word] if word in abbr_dict.keys() else word for word in x.split(' ') ]))

#%%

prediction = model.predict(df_conv)

ypred_values = np.squeeze(tf.sigmoid(prediction))

ypred_values = (ypred_values>0.5).astype(int)

if ypred_values == 1:
    text2print = "STRANGER DANGER!!!"
else:
    text2print = "Normal Chat"
    
st.write("The text is:")
st.write(text2print)

