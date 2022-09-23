# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 13:21:02 2022

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


print('\n'*2,'*'*50,'\n          Data Frame Local\n','*'*50,'\n')

lista=r"D:/06.Datasets/ExoPlanet/Target/positivo_negativo_normal.csv"
data=pd.read_csv(lista)  
data1=pd.DataFrame(data,columns=['id'])
data2=pd.DataFrame(data,columns=['disposition'])


N=len(data)
name0="D:/06.Datasets/ExoPlanet/Train/Normal_Local/"+data.iloc[0,0]+"_local.npy"
print(N)
arr0=np.load(name0)
arr0=arr0.reshape(1,-1)
for j in range(1,N,1):
    
    name="D:/06.Datasets/ExoPlanet/Train/Normal_Local/"+data.iloc[j,0]+"_local.npy"
    arr=np.load(name)
    arr=arr.reshape(1,-1)
    arr_conc=np.concatenate((arr0,arr))
    arr0=arr_conc
   
print(arr_conc,arr_conc.shape) 
    
DF=pd.DataFrame(arr_conc)


DF1=pd.concat([data1,DF],axis=1)
#print(DF1,data2)
#DF1.to_csv('DF_local4.csv',index=False)


#______________________________________________________________________________

print('\n'*2,'*'*50,'\n          Data Frame Global\n','*'*50,'\n')

lista=r"D:/06.Datasets/ExoPlanet/Target/positivo_negativo_normal.csv"
data=pd.read_csv(lista)  
data1=pd.DataFrame(data,columns=['id'])
data2=pd.DataFrame(data,columns=['disposition'])


N=len(data)
name0="D:/06.Datasets/ExoPlanet/Train/Normal_Global/"+data.iloc[0,0]+"_global.npy"
print(N)
arr0=np.load(name0)
arr0=arr0.reshape(1,-1)
for j in range(1,N,1):
    
    name="D:/06.Datasets/ExoPlanet/Train/Normal_Global/"+data.iloc[j,0]+"_global.npy"
    arr=np.load(name)
    arr=arr.reshape(1,-1)
    arr_conc=np.concatenate((arr0,arr))
    arr0=arr_conc
   
print(arr_conc,arr_conc.shape) 
    
DF=pd.DataFrame(arr_conc)


DF2=pd.concat([DF,data2],axis=1)
#print(DF2,data2)
#DF2.to_csv('DF_global3.csv',index=False)


#______________________________________________________________________________

print('\n'*2,'*'*50,'\n          Data Frame\n','*'*50,'\n')
DF_PN=pd.concat([DF1,DF2],axis=1)
print(DF_PN)
DF_PN.to_csv('DF_PN_normal.csv',index=False)