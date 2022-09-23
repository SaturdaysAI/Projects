"""
Created on Mon Jun  6 23:01:20 2022

@author: GONZALO
"""

# Importamos los módulos necesarios
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.layers import Activation
from keras.callbacks import EarlyStopping
import tensorflow as tf


print('\n','*'*50,'\n          Ejemplo\n','*'*50,'\n')
name="D:/06.Datasets/ExoPlanet/Train/Global/K00001.01_global.npy"
arr = np.load(name)
 
print(arr, arr.shape)
arr_norm=arr
media=arr.mean()
std=arr.std()
N2=len (arr)
 
for i in range(0,N2,1):
    arr_norm[i]=(media-arr[i])/std

print('\nK00001.01_global.npy modificado \n',arr_norm)



#______________________________________________________________________________

print('\n','*'*50,'\n          Global en proceso\n','*'*50,'\n')
lista=r"D:/06.Datasets/ExoPlanet/Train/Listas/lista_Global.csv"
data=pd.read_csv(lista)   
N=len(data)
for j in range(0,N,1):
    name="D:/06.Datasets/ExoPlanet/Train/Global/"+data.iloc[j,0]
    arr = np.load(name)
    
    #print(arr, arr.shape)
    arr_norm=arr
    media=arr.mean()
    std=arr.std()
    N2=len (arr)
    
    for i in range(0,N2,1):
        arr_norm[i]=(media-arr[i])/std
    
    np.save('D:/06.Datasets/ExoPlanet/Train/Normal_Global/normal_'+data.iloc[j,0],arr_norm)



print('\n'*2,'*'*50,'\n          Local en proceso\n','*'*50,'\n')
lista=r"D:/06.Datasets/ExoPlanet/Train/Listas/lista_Local.csv"
data=pd.read_csv(lista)   
N=len(data)
for j in range(0,N,1):
    name="D:/06.Datasets/ExoPlanet/Train/Local/"+data.iloc[j,0]
    arr = np.load(name)
    
    #print(arr, arr.shape)
    arr_norm=arr
    media=arr.mean()
    std=arr.std()
    N2=len (arr)
    
    for i in range(0,N2,1):
        arr_norm[i]=(media-arr[i])/std
    
    np.save('D:/06.Datasets/ExoPlanet/Train/Normal_Local/normal_'+data.iloc[j,0],arr_norm)
 