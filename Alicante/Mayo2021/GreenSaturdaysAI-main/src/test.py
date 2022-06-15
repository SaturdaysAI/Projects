import numpy as np
import pandas as pd
import folium as fol

def main():
    path = 'C:/Users/cesar/Desktop/Proyecto/GreenSaturdaysAI/datasets/estaciones/2018/2018_qualitat_aire_estaciones_bcn.csv'
    # Leemos el .csv
    data = pd.read_csv(path)
    # creamos la variable que guarda el mapa con las coord. de la ciudad de Barcelona
    m = fol.Map(location = [45.5236, -122.6750],
                zoom_start = 13)
    

    print('Todo correcto')




if __name__ == '__main__':
    import sys
    sys.exit(main())



