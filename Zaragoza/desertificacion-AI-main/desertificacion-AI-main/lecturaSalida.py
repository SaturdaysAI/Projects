# Tratamiento de datos
# ------------------------------------------------------------------------------
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from rasterio import plot

tfpredicho=open('predicho.txt')
tfreal=open('fotoreal.txt')

a=[]
b=[]

for line in tfpredicho:
    a.append((line.rstrip()).rsplit())
for line2 in tfreal:
    b.append((line2.rstrip()).rsplit())

anp=np.array(a)
anp=np.reshape(anp,(498,498))

org=np.array(b)
org=np.reshape(org,(498,498))    

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
plot.show(anp.astype(np.float64), ax=ax1)
plot.show(org.astype(np.float64), ax=ax2)
fig.tight_layout()
plot.show(anp.astype(np.float64))
plot.show(org.astype(np.float64))
#visualizamos la matriz


