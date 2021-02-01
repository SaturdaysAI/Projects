import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from sklearn.cluster import KMeans

class clustersClass:
    
    def __init__(self): 
        self.name = "Cusotm Clustering class version"
        
    def dict_definition(self, val):
        if val.lower() == 'kmeans':
            print('- Kmeans puede dar resultados diferentes. Por lo tanto, se define un parametro "n_init" que comprende varias ejecuciones del modelo.')
            print('- El mejor resultado es aquel que da un menor valor para la varianza. Estaría bien comprobar en su totalidad y por centroide.')
            print('- Se habla de varianza porque en Kmeans se generan centroides y se calcula la variabilidad como la distancia de cada punto hasta el centroide. ')
            print('- A diferencia del DBSCAN o Agglomerative (Hierarch) se indican los clusters de antemano siempre')
            print('- Siempre se calcula la distancia euclidea. Considera que la distnacia euclidea, si un dataset tiene 1000 columnas sería la raiz del cuadrado de cada uno de esos mil componentes')
            print('- El algoritmo de iniciación es clave')
            print('- Es muy sensible a outliers porque clasifica todo')
            print('- Comptuacionalmente lleva tiempo porque calcula todas las distancias por iteración de cada ejecución')
            print('- Cada punto calculado es en bas')
            print('- Refernecia: https://www.youtube.com/watch?v=4b5d3muPQmA&list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF&index=34')
        if val.lower() == 'agglomerative':
            print('- Dentro del hierarchical clustering, hay agglomerative (Bottom up) y divisive (top down). Ambos dan resultados parecidos pero el agglomerative es matemáticamente más sencillo. ')
            print('- Es mas preciso que Kmeans pero computacionalmente mas costoso')
            print('- Capaz de econtrar clusters con formas geometricas aribtrarias')
            print('- El dendograma representa como se crean los clusters')
            print('- Tres ejes principales a considerar: ')
            print('- 1) Como representar el cluster: centroide (euclidea) o clustroide (no euclidea)')
            print('- 1.1) Esto sería el parametro affinity')
            print('- 2) Determinar la cercanía entre clusters: Distancia entre centroides o clustroides - Tipos de distnacias: Euclidea / No euclidea - Manhattan')
            print('- 2.1) Esto sería el parametro linkage')
            print('- 3) Cuando parar: ')
            print('- 3.1) Podemos definir los clusters de antemano o hacerlo dependiente de una función - Min 12:10')            
            print('- Refernecia: https://www.youtube.com/watch?v=rg2cjfMsCk4')

        if val.lower() == 'dbscan':
            print('- Muy robusto frente a outliers')
            print('- Capaz de econtrar clusters con formas geometricas aribtrarias')
            print('- Dipone de dos parametros: Epsilon y minimum points')
            print('- Hay tres tipos de puntos: Core, border y outlier - Min: 2:15')
            print('- Asume densidades similares en todos los clusters y eso puede ser un problema')
            print('- Valores noisy tienen el label de -1. Es decir, los outliers')
            print('- Refernecia: https://www.youtube.com/watch?v=sJQHz97sCZ0')
        
        
    def kmeans_elbow(self, val, X):
        # Con mas clusters siempre habrá menos varianza pelo la caida no será tan agresiva! Puntos de inflexión!
        
        if val.lower() == 'inertia':
            desajuste = []
            for i in range(1, 11):
                km = KMeans(n_clusters=i, random_state=0)
                km.fit(X)
                desajuste.append(km.inertia_)
            
            plt.plot(range(1, 11), desajuste, marker='o')
            plt.xlabel('k')
            plt.ylabel('SSE')
            plt.show()
        if val.lower() == 'score':
            score = []
            for i in range(1, 11):
                km = KMeans(n_clusters=i, random_state=0)
                km.fit(X)
                score.append(km.fit(X).score(X))
            
            plt.plot(range(1, 11), score, marker='o')
            plt.xlabel('k')
            plt.ylabel('Score')
            plt.show()           