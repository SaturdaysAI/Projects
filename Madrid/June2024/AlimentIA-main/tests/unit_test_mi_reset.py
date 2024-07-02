import unittest

def mi_reset(varnames):
    """
    la función mi_reset toma una lista de nombres de variables y las guarda en un diccionario para luego reiniciar el kernel y cargar las variables guardadas
    parámetros:
    - varnames: lista de nombres de variables
    retorna:
    - variables guardadas
    """
    globals_ = globals()
    to_save = {v: globals_[v] for v in varnames}
    to_save['mi_reset'] = mi_reset  # lets keep this function by default
    del globals_
    get_ipython().magic("reset")
    globals().update(to_save)
    
class MiResetTests(unittest.TestCase):
    def test_reset_variables(self):
        # Arrange
        features_df = [1, 2, 3]
        varnames = ['features_df']
        to_save = {'features_df': features_df, 'mi_reset': mi_reset}

        # Act
        globals().update(to_save)
        mi_reset(varnames)

        # Assert
        self.assertEqual(features_df, globals()['features_df'])

if __name__ == '__main__':
    unittest.main()