import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.decomposition import PCA


class pcaAsierClass:
    
    def __init__(self): 
        self.name = "Cusotm PCA class version"
        
    def relevant(self):
        print('- Los datos tienen que estar escalados. A través de las pendientes se generan los loading scores... ')
        print('- El algoritmo de PCA con el que se calculan los compnentes se llama SVD.')
        print('- SVD cacula el teorema de pitagoras en base del origen de los ejes. Así, los datos tienen que estar centrados.')
        print('- Hay dos formas de crear PCAs. A través del número de componentes o a través del % de varianza que queremos considerar')
        print('- Aunque la varianza acumulada sea bajita, siempre hay que visualizar los datos. Aun se pueden generar clusters.')
        print('- En principio se dice que PCA reduce overfitting porque pieredes información al crear PCAs. No obstante, hay otras variables que tienen impacto en el overfitting como el split en train test ;) ')
        print('- PCA es muy rapido de calcular pero parte de forma lineales al calcular lo cual puede hacer que no sea super práctico siempre! Para eso está t-SNE, MDS, NMF')
        
    
    def dictionary(self):
        self.dict = ['Eigenvalue', 'Loading scores', 'Explained variance']
        print('Relevant concepts to bear on mind!')
        for i in range(0, len(self.dict)):
            print(str(i+1) + ') ' + self.dict[i])
            
    def dict_definition(self, val):
        if val.lower() == 'eigenvalue':
            print('- PCA genera dimesniones adicionales. Estas son caluladas siguiendo el teorema de pitagoras.')
            print('- Eigenvalue represnta el tamaño de la hipotenusa en escala de 1')
            print('- Eigenvalue no da información interpretable')
            print('- Los loading socres son interpretables y calculados a través del Eigenvalue')
            print('- Referencia: https://www.youtube.com/watch?v=FgakZw6K1QQ&list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF&index=24')
            print('- Tiempo: 12:14')
        if val.lower() == 'loading scores':
            print('- Cada PCA dispone de un Eigenvalue. Cada Eigenvalue dispone de multiples loading scores.')
            print('- Se diponde de un loading score por variable del dataset.')
            print('- El loading score representa la relevancia en el componente por cada atributo.')
            print('- Los laoding scores seríían los catetos del triangulo generado escalado a 1')
            print('- Referencia: https://www.youtube.com/watch?v=FgakZw6K1QQ&list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF&index=24')
            print('- Tiempo: 12:14')
        if val.lower() == 'Explained variance':
            print('Define la variabilidad que comprende cada eje y así su relevancia.')
            print('Scree plot es la representación de la variablidad')
            print('- Referencia: https://www.youtube.com/watch?v=FgakZw6K1QQ&list=PLblh5JKOoLUICTaGLRoHQDuF_7q2GfuJF&index=24')
            print('- Tiempo: 16:10')            
        

    def explained_variance(self, pca):   
        # Habremos elegido inicialización por numero de componentes
        plt.figure()
        plt.plot(np.cumsum(pca.explained_variance_ratio_))
        plt.xlabel('Componentes principales')
        plt.ylabel('Varianza (%)')
        plt.title('Varianza explicada')
        plt.show()
        
    def get_eigenvalues(sel, pca):
        # Esto no nos da info adicional pero es la base de todo
        return pca.singular_values_.round(2)

    def loading_scores_plot(self, pca):
        for i in range(0, len(pca.n_components)):
            plt.plot(range(0, pca.components_.shape[1]), pca.components_[i], marker='o', label='componente '+str(i+1))
        plt.xlabel('Número de variable')
        plt.ylabel('Peso')
        plt.legend(prop=dict(size=12))
        plt.show()
        
    def loading_scores_df(self, pca):
        loadings = pd.DataFrame(pca.components_.T)
        cols = []
        for i in range(0, len(pca.n_components)):
            cols.append('Col '+str(i+1))
        loadings.columns= cols
        return loadings
    
    def components_score(self, pca_base, model, dataset_X, base_accuracy):
        # Notebook: MIOTI - S2_ML2_worksheet
        # Puede que se genere una curva en la que con menos componentes mejor accuracy
        # Una especie de montaña rusa
        # Preguntar!
        accuracy = []
        n_components = []
        
        for n in range(1, pca_base.components_ +1):
            pca = PCA(n_components=n)
            pca.fit(dataset_X)
            transformed_X = pca.transform(dataset_X)
            
            scores = cross_val_score(model, transformed_X, dataset_y, cv=5)
            
            n_components.append(n)
            accuracy.append(scores.mean())
            #print("Components: %03d   Accuracy: %.3f" % (n, scores.mean()))
            print(".", end='')
            
        plt.figure(1, figsize=(16, 5))
        plt.clf()
        plt.plot(n_components, accuracy, linewidth=2)
        plt.axis('tight')
        plt.xlabel('n_components')
        plt.ylabel('accuracy')
        axes = plt.gca()
        axes.set_ylim([0, 1])
        plt.axhline(base_accuracy, linestyle=':', label='base_accuracy')
        plt.legend(prop=dict(size=12))
                    
        
#pca = pcaAsierClass()
#pca.dictionary()
#pca.dict_definition('Loading scores')
#pca.tips_pca()