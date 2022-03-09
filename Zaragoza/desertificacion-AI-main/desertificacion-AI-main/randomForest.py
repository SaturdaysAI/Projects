# Tratamiento de datos
# ------------------------------------------------------------------------------
import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error

# Gráficos
# ------------------------------------------------------------------------------
import matplotlib.pyplot as plt
import sklearn

# Preprocesado y modelado
# ------------------------------------------------------------------------------
from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.tree import plot_tree
from sklearn.tree import export_graphviz
from sklearn.tree import export_text
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_squared_error


# Tratamiento de datos
# ==============================================================================
import pandas as pd
import numpy as np

# Gráficos
# ==============================================================================
import matplotlib.pyplot as plt
from matplotlib import style
import seaborn as sns

# Preprocesado y modelado
# ==============================================================================
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

from sklearn.ensemble import RandomForestRegressor


#Necesitamos transformar la imagen tiff a una matriz de datos

from PIL import Image 
from numpy import asarray   
outfile_name='./out/T31TBG_20210219T104959_B_NDVI.tif' 
image1 = Image.open(outfile_name) 
outfile_name='./out/T31TBG_20210316T105031_B_NDVI.tif' 
image2 = Image.open(outfile_name) 
outfile_name='./out/T31TBG_20210405T105021_B_NDVI.tif' 
image3 = Image.open(outfile_name) 
outfile_name='./out/T31TBG_20210505T105031_B_NDVI.tif' 
image4 = Image.open(outfile_name) 
outfile_name='./out/T31TBG_20210614T105031_B_NDVI.tif' 
image5 = Image.open(outfile_name) 
outfile_name='./out/T31TBG_20210714T105031_B_NDVI.tif' 
image6 = Image.open(outfile_name) 

outfile_name='./out/T31TBG_20210813T105031_B_NDVI.tif'
image7 = Image.open(outfile_name) 
outfile_name='./out/T31TBG_20210912T105031_B_NDVI.tif'
image8 = Image.open(outfile_name) 
outfile_name='./out/T31TBG_20211027T105049_B_NDVI.tif'
image9 = Image.open(outfile_name) 
outfile_name='./out/T31TBG_20211116T105229_B_NDVI.tif'
image10 = Image.open(outfile_name) 
outfile_name='./out/T31TBG_20211206T105329_B_NDVI.tif'
image11 = Image.open(outfile_name) 
outfile_name='./out/T31TBG_20220120T105351_B_NDVI.tif'
image12 = Image.open(outfile_name) 
    
'''print(image.format) 
print(image.size) 
print(image.mode)'''

#Imagenes de entrenamiento
numpydata1 = asarray(image1) 
numpydata2 = asarray(image2)
numpydata3 = asarray(image3)
numpydata4 = asarray(image4)
numpydata5 = asarray(image5)
numpydata6 = asarray(image6)

#Imagenes para test
numpydata7 = asarray(image7)
numpydata8 = asarray(image8) 
numpydata9 = asarray(image9)
numpydata10 = asarray(image10)
numpydata11 = asarray(image11)
numpydata12 = asarray(image11)
  
X=[]
Y=[]
for i in range (3000,4000-2) :
    for j in range (3000,4000-2) :        
        '''X entrada
        Y salida'''
        X.append([numpydata1[i,j],numpydata1[i,j+1],numpydata1[i,j+2],
                 numpydata1[i+1,j],numpydata1[i+1,j+1],numpydata1[i+1,j+2],
                 numpydata1[i+2,j],numpydata1[i+2,j+1],numpydata1[i+2,j+2],
                 numpydata2[i,j],numpydata2[i,j+1],numpydata2[i,j+2],
                 numpydata2[i+1,j],numpydata2[i+1,j+1],numpydata2[i+1,j+2],
                 numpydata2[i+2,j],numpydata2[i+2,j+1],numpydata2[i+2,j+2],
                 numpydata3[i,j],numpydata3[i,j+1],numpydata3[i,j+2],
                 numpydata3[i+1,j],numpydata3[i+1,j+1],numpydata3[i+1,j+2],
                 numpydata3[i+2,j],numpydata3[i+2,j+1],numpydata3[i+2,j+2],
                 numpydata4[i,j],numpydata4[i,j+1],numpydata4[i,j+2],
                 numpydata4[i+1,j],numpydata4[i+1,j+1],numpydata4[i+1,j+2],
                 numpydata4[i+2,j],numpydata4[i+2,j+1],numpydata4[i+2,j+2],
                 numpydata5[i,j],numpydata5[i,j+1],numpydata5[i,j+2],
                 numpydata5[i+1,j],numpydata5[i+1,j+1],numpydata5[i+1,j+2],
                 numpydata5[i+2,j],numpydata5[i+2,j+1],numpydata5[i+2,j+2]                 
        ])
        '''Y.append([numpydata6[i,j],numpydata6[i,j+1],numpydata6[i,j+2],
                 numpydata6[i+1,j],numpydata6[i+1,j+1],numpydata6[i+1,j+2],
                 numpydata6[i+2,j],numpydata6[i+2,j+1],numpydata6[i+2,j+2]])'''
for i in range (3000,4000-2) :
    for j in range (3000,4000-2) :     
        Y.append(numpydata6[i+1,j+1])

Xnp=np.array(X)
Ynp=np.array(Y)
np.savetxt('entrada2.txt', Xnp)
#Clasificador
cls=RandomForestRegressor()
#Entrenamiento
#Found input variables with inconsistent numbers of samples: [4356, 39204]
print(len(X))
print(len(Y))
cls.fit(X,Y)
A=[]
B=[]
for i in range (4000,5000-2) :
    for j in range (4000,5000-2) :        
        '''X entrada
        Y salida'''
        A.append([numpydata1[i,j],numpydata1[i,j+1],numpydata1[i,j+2],
                 numpydata1[i+1,j],numpydata1[i+1,j+1],numpydata1[i+1,j+2],
                 numpydata1[i+2,j],numpydata1[i+2,j+1],numpydata1[i+2,j+2],
                 numpydata2[i,j],numpydata2[i,j+1],numpydata2[i,j+2],
                 numpydata2[i+1,j],numpydata2[i+1,j+1],numpydata2[i+1,j+2],
                 numpydata2[i+2,j],numpydata2[i+2,j+1],numpydata2[i+2,j+2],
                 numpydata3[i,j],numpydata3[i,j+1],numpydata3[i,j+2],
                 numpydata3[i+1,j],numpydata3[i+1,j+1],numpydata3[i+1,j+2],
                 numpydata3[i+2,j],numpydata3[i+2,j+1],numpydata3[i+2,j+2],
                 numpydata4[i,j],numpydata4[i,j+1],numpydata4[i,j+2],
                 numpydata4[i+1,j],numpydata4[i+1,j+1],numpydata4[i+1,j+2],
                 numpydata4[i+2,j],numpydata4[i+2,j+1],numpydata4[i+2,j+2],
                 numpydata5[i,j],numpydata5[i,j+1],numpydata5[i,j+2],
                 numpydata5[i+1,j],numpydata5[i+1,j+1],numpydata5[i+1,j+2],
                 numpydata5[i+2,j],numpydata5[i+2,j+1],numpydata5[i+2,j+2]                 
        ])
        '''B.append([numpydata6[i,j],numpydata6[i,j+1],numpydata6[i,j+2],
                 numpydata6[i+1,j],numpydata6[i+1,j+1],numpydata6[i+1,j+2],
                 numpydata6[i+2,j],numpydata6[i+2,j+1],numpydata6[i+2,j+2]])'''
for i in range (4000,5000-2) :
    for j in range (4000,5000-2) :     
        B.append(numpydata6[i+1,j+1])
Bpredicho=cls.predict(A)
print(mean_squared_error(B, Bpredicho))
#Mostramos B y cls.predict(a)
np.savetxt('fotoreal.txt',B)
np.savetxt('predicho.txt',cls.predict(A))
