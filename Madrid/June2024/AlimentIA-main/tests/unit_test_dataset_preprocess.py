import pandas as pd
import numpy as np
import unittest

df = pd.read_excel('C:\\Users\\Lenovo\\Desktop\\Predicción de ventas\\rawdata\\Reporte Maestro LaPeninsula 24.xlsx', sheet_name='Raw Data')

def modificar_dataset(dataset):
    ''' 
    la función modificar_dataset toma un conjunto de datos y realiza las siguientes operaciones:
    - Reemplazar los valores de la columna Familia mediante replace
    - Reemplazar los valores de la columna Dia mediante replace
    - Reemplazar los valores de la columna Mes mediante replace
    - Eliminar columnas con más del 79600 valores nulos
    - Eliminar filas con valores nulos
    - Crear una nueva columna con la hora de la compra a partir de la columna Fecha Creación
    - Sustituir valores en la columna Dia con replace para convertirlos en números
    - Crear una columna llamada days_since_prior_order que indica el número de días desde la última compra de un producto en función de la columna Fecha
    - Crear columna llamada client_id que indica el id del cliente en función de la columna Número de forma ascendentemente empezando desde 0
    - Crear columna llamada product_id que indica el id del producto en función de la columna Producto de forma ascendentemente empezando desde 0
    - Crear columna llamada user_id en función de la columna order_id de forma aleatoria
    parámetros: 
    - dataset: conjunto de datos
    retorna:
    - dataset: conjunto de datos modificado
    '''
    # se remplazan los valores de la columna Familia mediante replace
    dataset['Familia'] = dataset['Familia'].replace({'BOLSAS': 'Bolsas', 'Sobres al Vacio': 'Sobres al vacio', 'SERVICIOS': 'Servicios'})
    # se reemplazan los valores de la columna Dia mediante replace
    dataset['Dia'] = dataset['Dia'].replace({'Monday': 'lunes', 'Friday': 'viernes', 'Saturday': 'sábado', 'Sunday': 'domingo', 'Thursday': 'jueves', 'Tuesday': 'martes', 'Wednesday': 'miércoles'})
    # se reemplazan los valores de la columna Mes mediante replace
    dataset['Mes'] = dataset['Mes'].replace({'December': 'diciembre', 'November': 'noviembre', 'October': 'octubre', 'September': 'septiembre', 'August': 'agosto', 'July': 'julio', 'June': 'junio', 'May': 'mayo', 'April': 'abril', 'March': 'marzo', 'February': 'febrero', 'January': 'enero'})
    # Eliminar columnas con más del 79600 valores nulos
    dataset = dataset.drop(['Color', 'Cuenta Contable', 'Cód. Descuento', 'Cód. Promoción', 'Talla', 'Cliente', 'País', 'CIF/NIF', 'Dirección', 'Población', 'Provincia', 'Código Postal', 'Usuario', 'Grupo Mayor'], axis=1)
    # eliminar filas con valores nulos
    dataset = dataset.dropna(axis=0)
    dataset = dataset.drop_duplicates()
    # crear una nueva columna con la hora de la compra a partir de la columna Fecha Creación
    dataset['Hora'] = dataset['Fecha Creación'].apply(lambda x: x.hour)
    # sustituir valores en la columna Dia con replace para convertirlos en números
    dataset['Dia'] = dataset['Dia'].replace({'lunes': 1, 'martes': 2, 'miércoles': 3, 'jueves': 4, 'viernes': 5, 'sábado': 6, 'domingo': 7})
    # crear una columna llamada days_since_prior_order que indica el número de días desde la última compra de un producto en funcion de la columna Fecha
    dataset['days_since_prior_order'] = dataset.groupby('Producto')['Fecha'].diff().dt.days
    dataset['days_since_prior_order'].fillna(0, inplace=True)
    dataset['days_since_prior_order'] = dataset['days_since_prior_order'].astype(int)
    # crear columna llamada client_id que indica el id del cliente en función de la columna Número de forma ascendentemente empezando desde 0
    dataset['order_id'] = dataset['Número'].astype('category').cat.codes
    dataset['order_id'] = dataset['order_id'].astype(int)
    # crear columna llamada product_id que indica el id del producto en función de la columna Producto de forma ascendentemente empezando desde 0
    dataset['product_id'] = dataset['Producto'].astype('category').cat.codes
    dataset['product_id'] = dataset['product_id'].astype(int)
    # crear columna llamada user_id en función de la columna order_id de forma aleatoria
    dataset['user_id'] = dataset.groupby('order_id')['order_id'].transform(lambda x: np.random.randint(0, 1000))
    dataset['user_id'] = dataset['user_id'].astype(int)
    return dataset


class TestDatasetPreprocess(unittest.TestCase):
    def setUp(self):
        self.dataset_empty = pd.DataFrame()
        self.dataset_missing_values = pd.DataFrame({'Familia': ['BOLSAS', 'Sobres al Vacio', None], 'Dia': ['Monday', 'Friday', 'Saturday'], 'Mes': ['December', 'November', 'October'],'Fecha Creación': ['2022-01-01 10:00:00', '2022-02-01 12:00:00', '2022-03-01 14:00:00'], 'Número': [1, 2, 3], 'Producto': ['Product A', 'Product B', 'Product C']})
        self.dataset_valid_values = pd.DataFrame({'Familia': ['BOLSAS', 'Sobres al Vacio', 'SERVICIOS'], 'Dia': ['Monday', 'Friday', 'Saturday'], 'Mes': ['December', 'November', 'October'], 'Fecha Creación': ['2022-01-01 10:00:00', '2022-02-01 12:00:00', '2022-03-01 14:00:00'], 'Número': [1, 2, 3],'Producto': ['Product A', 'Product B', 'Product C']})

    def test_modificar_dataset_empty(self):
        modified_dataset_empty = modificar_dataset(self.dataset_empty)
        self.assertTrue(modified_dataset_empty.empty)

    def test_modificar_dataset_missing_values(self):
        modified_dataset_missing_values = modificar_dataset(self.dataset_missing_values)
        self.assertEqual(modified_dataset_missing_values.shape[0], 2)

    def test_modificar_dataset_valid_values(self):
        modified_dataset_valid_values = modificar_dataset(self.dataset_valid_values)
        self.assertEqual(modified_dataset_valid_values.shape[0], 3)

if __name__ == '__main__':
    unittest.main()
