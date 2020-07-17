#!/usr/bin/env python
# coding: utf-8

# In[1]:


## Python
import os
import random
import sys
import warnings
warnings.filterwarnings('ignore')


## Package
import glob 
import keras
import IPython.display as ipd
import librosa

import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.offline as py
import plotly.tools as tls
import seaborn as sns
import scipy.io.wavfile
import tensorflow as tf
py.init_notebook_mode(connected=True)


## Keras
from keras import regularizers
from keras.callbacks import ModelCheckpoint, LearningRateScheduler, EarlyStopping
from keras.callbacks import  History, ReduceLROnPlateau, CSVLogger
from keras.models import Model, Sequential
from keras.layers import Dense, Embedding, LSTM
from keras.layers import Input, Flatten, Dropout, Activation, BatchNormalization
from keras.layers import Conv1D, MaxPooling1D, AveragePooling1D
from keras.preprocessing import sequence
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from keras.utils import np_utils
from keras.utils import to_categorical

from keras.models import Model, Sequential
from keras import optimizers
from keras.layers import Input, Conv1D, Conv2D,BatchNormalization, MaxPooling1D,MaxPooling2D, LSTM, Dense, Activation, Layer,Reshape

from keras.utils import to_categorical
import keras.backend as K
from keras.callbacks import EarlyStopping
from keras.callbacks import ModelCheckpoint
from keras.models import load_model


## Sklearn
from sklearn.metrics import confusion_matrix
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split


## Rest
from scipy.fftpack import fft
from scipy import signal
from scipy.io import wavfile
from tqdm import tqdm_notebook as tqdm

input_duration=3
# % pylab inline


# In[2]:


# Data Directory
# Please edit according to your directory change.
Ravdess_paths= np.array(("D:\AISaturday\AISaturday2020\sound file"))
dir_list = os.listdir("D:\AISaturday\AISaturday2020\sound file")
dir_list.sort()
print (dir_list)


# In[3]:


# Create DataFrame for Data intel
ravdess_db = pd.DataFrame(columns=['path','source','actor', 'gender', 'emotion','emotion_lb'])
count = 0
#for data_path in Ravdess_paths:
 #   dir_list = os.listdir(data_path)
  #  dir_list.sort()
for i in dir_list:
        file_list = os.listdir("D:\AISaturday\AISaturday2020\sound file"+ '/' + i)
        for f in file_list:
            nm = f.split('.')[0].split('-')
            path = "D:\AISaturday\AISaturday2020\sound file"+ '/' + i + '/' + f
            src = int(nm[1])
            actor = int(nm[-1])
            emotion = int(nm[2])
            source = "Ravdess"

            if int(actor)%2 == 0:
                gender = "female"
            else:
                gender = "male"

            if nm[3] == '01':
                intensity = 0
            else:
                intensity = 1

            if nm[4] == '01':
                statement = 0
            else:
                statement = 1

            if nm[5] == '01':
                repeat = 0
            else:
                repeat = 1

            if emotion == 1:
                lb = "neutral"
            elif emotion == 2:
                lb = "calm"
            elif emotion == 3:
                lb = "happy"
            elif emotion == 4:
                lb = "sad"
            elif emotion == 5:
                lb = "angry"
            elif emotion == 6:
                lb = "fearful"
            elif emotion == 7:
                lb = "disgust"
            elif emotion == 8:
                lb = "surprised"
            else:
                lb = "none"

            ravdess_db.loc[count] = [path,source,actor, gender, emotion,lb]
            count += 1


# In[4]:


ravdess_db.shape


# In[5]:


ravdess_db


# In[6]:


ravdess_db['split'] =  np.where((ravdess_db.actor ==23) | (ravdess_db.actor ==24), 'Test', 
                                (np.where((ravdess_db.actor ==21) | (ravdess_db.actor ==22),'Val','Train')))


# In[7]:


ravdess_db['split'].value_counts()


# In[8]:


ravdess_db.drop(ravdess_db.index[ravdess_db['emotion_lb'] == 'surprised'], inplace = True)
ravdess_db.loc[ravdess_db.emotion_lb=='calm',['emotion','emotion_lb']]= 1,'neutral'


# In[9]:


ravdess_db.emotion_lb.value_counts()


# In[10]:


dataset_db = ravdess_db.copy()
dataset_db.emotion_lb = dataset_db.gender+"_"+dataset_db.emotion_lb
dataset_db.index=range(len(dataset_db.index))
#dataset_db.to_csv("/content/gdrive/My Drive/Colab Notebooks/list2.csv")


# In[11]:


dataset_db.emotion_lb.value_counts()
dataset_db.sort_values(by=['path'], inplace=True)
dataset_db.head()


# In[12]:


dataset_db.index = range(len(dataset_db.index))
dataset_db.shape


# In[13]:


import h5py
with h5py.File('D:/AISaturday/AISaturday2020/DeteccionAudio/modelos/Ravdess_audio_Mel_spec.h5', 'r') as hf:
  audios = hf['Ravdess_audio_Mel_spec'][:]


# In[14]:


librosa.display.specshow(audios[0].reshape(128,259))


# In[15]:


x_train = audios[(dataset_db['split'] == 'Train')]
y_train = dataset_db.emotion_lb[(dataset_db['split'] == 'Train')]

print(x_train.shape,y_train.shape)


# In[16]:


x_test = audios[(dataset_db['split'] == 'Val')]
y_test = dataset_db.emotion_lb[(dataset_db['split'] == 'Val')]
print(x_test.shape,y_test.shape)


# In[17]:


y_train = np.array(y_train)
y_test = np.array(y_test)

lb = LabelEncoder()
y_train = np_utils.to_categorical(lb.fit_transform(y_train))
y_test = np_utils.to_categorical(lb.fit_transform(y_test))


# In[19]:


# loading json and creating model
from keras.models import model_from_json
json_file = open('D:/AISaturday/AISaturday2020/DeteccionAudio/modelos/Audio_2DCNN_LogMelModel_4L.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)


# In[20]:


from keras.models import load_model
# Returns a compiled model identical to the previous one
loaded_model.load_weights('D:/AISaturday/AISaturday2020/DeteccionAudio/modelos/Audio_2DCNN_4L.h5')


# In[21]:


audio_duration = 3
sampling_rate = 22050*2
input_length = sampling_rate * audio_duration
n_mfcc = 20
data_sample= np.zeros(input_length)
MFCC = librosa.feature.mfcc(data_sample, sr=sampling_rate, n_mfcc=n_mfcc)

signal, sample_rate = librosa.load("D:/AISaturday/AISaturday2020/sound file/Actor_24/03-01-01-01-01-01-24.wav", res_type='kaiser_fast',sr=sampling_rate)
signal,index = librosa.effects.trim(signal,top_db = 25)
signal = scipy.signal.wiener(signal)

if len(signal) > input_length:
    signal = signal[0:input_length]
elif  input_length > len(signal):
    max_offset = input_length - len(signal)  
    signal = np.pad(signal, (0, max_offset), "constant")


# In[22]:


audios= np.empty(shape=(1,128, MFCC.shape[1], 1))
signal, sample_rate = librosa.load("D:/AISaturday/AISaturday2020/sound file/Actor_24/03-01-01-01-01-01-24.wav", res_type='kaiser_fast',sr=sampling_rate)
signal,index = librosa.effects.trim(signal,top_db = 25)
signal = scipy.signal.wiener(signal)
if len(signal) > input_length:
        signal = signal[0:input_length]
elif  input_length > len(signal):
        max_offset = input_length - len(signal)  
        signal = np.pad(signal, (0, max_offset), "constant")
        melspec = librosa.feature.melspectrogram(signal, sr=sample_rate, n_mels=128,n_fft=2048,hop_length=512)   
        logspec = librosa.amplitude_to_db(melspec)
        logspec = np.expand_dims(logspec, axis=-1)
        audios[0,]= logspec 
    #count+=1


# In[23]:


audios.shape


# In[24]:


audio_duration = 3
sampling_rate = 22050*2
input_length = sampling_rate * audio_duration
n_mfcc = 20
data_sample= np.zeros(input_length)
MFCC = librosa.feature.mfcc(data_sample, sr=sampling_rate, n_mfcc=n_mfcc)
MFCC.shape


# In[25]:


x_test_data = audios
preds = loaded_model.predict(x_test_data,batch_size=16,verbose=1)
preds1=preds.argmax(axis=1)
abc = preds1.astype(int).flatten()
predictions = (lb.inverse_transform((abc)))
print(predictions)


# In[26]:


print(predictions)


# In[ ]:





# In[ ]:




