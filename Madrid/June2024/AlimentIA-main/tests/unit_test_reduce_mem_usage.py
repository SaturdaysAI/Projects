import unittest
import numpy as np
import pandas as pd

def reduce_mem_usage(df):
    """ 
    la función itera a través de todas las columnas de un conjunto de datos y modifica el tipo de datos
    para reducir el uso de la memoria
    parámetros:
    - df: conjunto de datos
    retorna:
    - df: conjunto de datos con uso de memoria reducido     
    """
    start_mem = df.memory_usage().sum() / 1024**2
    print('El uso de la memoria del dataframe es {:.2f} MB'.format(start_mem))
    
    for col in df.columns:
        col_type = df[col].dtype
        col_type2 = df[col].dtype.name
        
        if ((col_type != object) and (col_type2 != 'category')):
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)  
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
        else:
            df[col] = df[col].astype('category')

    end_mem = df.memory_usage().sum() / 1024**2
    print('El uso de la memoria después de la optimizacion es: {:.2f} MB'.format(end_mem))
    print('Disminuido en un {:.1f}%'.format(100 * (start_mem - end_mem) / start_mem))
    
    return df

class TestReduceMemUsage(unittest.TestCase):
    def test_reduce_mem_usage(self):
        # Create a sample DataFrame
        df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': [4, 5, 6],
            'col3': ['a', 'b', 'c']
        })

        # Call the reduce_mem_usage function
        reduced_df = reduce_mem_usage(df)

        # Assert that the DataFrame has the expected memory usage
        expected_start_mem = df.memory_usage().sum() / 1024**2
        expected_end_mem = reduced_df.memory_usage().sum() / 1024**2
        self.assertAlmostEqual(expected_start_mem, expected_end_mem, places=2)

        # Assert that the DataFrame has the expected data types
        expected_dtypes = {
            'col1': np.int8,
            'col2': np.int8,
            'col3': 'category'
        }
        for col, dtype in expected_dtypes.items():
            self.assertEqual(reduced_df[col].dtype, dtype)

if __name__ == '__main__':
    unittest.main()