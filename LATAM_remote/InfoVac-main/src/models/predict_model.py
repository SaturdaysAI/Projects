import joblib
from src.models.support_functions import NormalizeTextTransformer
from typing import List
from lime.lime_text import LimeTextExplainer

file = '../../models/svm_pipeline_10_Nov_2020_13_10.sav'

try:
    model = joblib.load(file)
except Exception as e:
    print(e)
    # For docker use
    model = joblib.load('models/svm_pipeline_10_Nov_2020_13_10.sav')
class_names = {0: 'no confiable', 1:'confiable'}


def is_list_of_strings(lst: List) -> bool:
    if lst and isinstance(lst, list):
        return all(isinstance(elem, str) for elem in lst)
    else:
        return False


def predict(text: List[str]):
    assert is_list_of_strings(text), 'Input must be a list of strings'
    return model.predict_proba(text)


def explain(text: List[str]):
    assert is_list_of_strings(text), 'Input must be a list of strings'
    print(text)
    explainer = LimeTextExplainer(class_names=class_names)
    explain = explainer.explain_instance(text[0], model.predict_proba)

    response = {
        'conf_words': [line for line in explain.as_list() if line[1] > 0],
        'no_conf_words': [line for line in explain.as_list() if line[1] < 0]

    }

    return response


if __name__ == '__main__':
    pred = predict(['Esto es un texto de prueba para nuestro clasificador svm para detectar información poco confiable',
             'Una receta con aspirinas, jengibre, canela, limón, cebolla y miel cura el COVID-19',
             "Circularon en redes sociales supuestas declaraciones del actor argentino sobre el caso de la joven cordobesa que no pudo ver a su padre antes de morir de cáncer en Córdoba, debido a las medidas de restricción de la pandemia. ”La chica pudo ver a su padre por wassap. No es que no la vio” (sic), es la frase que se le atribuye a Rizzo y que es falsa, ya que no hay registros públicos de que haya hecho tales afirmaciones. ",
            ])

    print(pred)
