###
#
# Funciones auxiliares: debug y complementos
#
###

import pandas as pd
import string
import prg_globales as glb

#
# Devuelve una cadena de texto html en el color indicado
#
def dime_html_texto_color(texto, color):
    return "<span style=""color:" + color + ">" + texto + "</span>"

#
# Imprime un <titulo> seguido por un objeto pandas <variable_pandas>
# Sólo imprimer la <cantidad_lineas> indicadas
#
def debug_pd(titulo, variable_pandas, cantidad_lineas):
    if glb.debug_activado == 1:
        print ("\n*** " + titulo + " ***")
        if (cantidad_lineas >= 1) :
            print (variable_pandas.head(cantidad_lineas))
            print ("*** Fin debug ***\n")

#
# Imprime sólo si el debug está puesto, para acelerar los cálculos cuando se ejecuta en un PC con VS Code
#
def debug_print(texto, *args):
    if glb.debug_activado == 1:
        print (texto, *args)

#
# Elimina los signos de puntuación de la cadena
#
def elimina_signos_puntuacion(cadena): 
    puntuacion = string.punctuation
    # print (puntuacion)    

    for c in puntuacion:
        if c is not None:
            cadena = cadena.replace(c, "")
    for c in ('¡'):
        if c is not None:
            cadena = cadena.replace(c, "")
    return cadena

#
# Dada una lista de listas (una tabla) devuelve la columna indicada (empezando en 0)
#
def dime_columna(tabla, i):
    return [fila[i] for fila in tabla]

#
# No usado finalmente, indicando UTF-8 l latin1 al importar el csv lo convierte bien en un dataframe
#
# def repara_acentos(cadena): # -> no es preciso si se abre en UTF-8
#     # print ('Repara acentos: ' + cadena)
#     acentos = {'Ã¡':'a', 'Ã­':'i', 'Ãº':'u', 'Ã±':'ñ', 'no':'no', 'No': 'No'}
#     # print (puntuacion)    
#     for elemento in acentos:
#         # print ("Cadena: " + cadena)
#         # print ("Elemento:" + elemento)
#         # print (acentos[elemento])
#         cadena = cadena.replace(elemento, '*'+ acentos[elemento] + '*')
#     # print(cadena)
#     return cadena # Prueba