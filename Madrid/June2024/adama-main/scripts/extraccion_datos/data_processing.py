"""
Autor: Alejandro Alvarez Tenedor
Fecha: 31 de mayo de 2024
Funcionalidad: Este script procesa y consolida datos de archivos CSV que contienen información de densidad de tráfico.
Lee los archivos CSV de una carpeta especificada, filtra y agrupa los datos, y guarda el resultado consolidado en un único archivo CSV.
"""


import os
import pandas as pd

# Ruta de la carpeta con los archivos CSV
csv_folder = r"C:\Users\ezxt99454\Desktop\crisa\Personal\SaturdaysAI\clases\proyecto_final\data\densidad_trafico\raw files"

# Ruta donde se guardará el archivo CSV final
output_csv = r"C:\Users\ezxt99454\Desktop\crisa\Personal\SaturdaysAI\clases\proyecto_final\data\densidad_trafico\final csv\flujo_Trafico.csv"

# Columnas seleccionadas para el dataset final
selected_columns = ["id", "fecha", "tipo_elem", "intensidad", "ocupacion", "carga", "vmed", "error", "periodo_integracion"]

# Escribir la cabecera en el archivo CSV
header_written = False

# Leer y procesar los datos de los archivos CSV en la carpeta
for csv_file in os.listdir(csv_folder):
    if csv_file.endswith('.csv'):
        print(f"Procesando fichero {csv_file}")

        df = pd.read_csv(os.path.join(csv_folder, csv_file), sep=';', encoding='utf-8')

        # Convertir la columna 'fecha' a datetime y extraer la hora inicial
        df['fecha'] = pd.to_datetime(df['fecha'])
        df['hora_inicial'] = df['fecha'].dt.floor('H')

        # Seleccionar las filas con tipo_elem igual a "M30" o "URB"
        df = df[df['tipo_elem'].isin(["M30", "URB"])]

        # Agrupar por hora y realizar cálculos para las variables
        grouped_df = df.groupby(['id', 'hora_inicial', 'tipo_elem']).agg({
            'intensidad': 'mean',
            'ocupacion': 'mean',
            'carga': 'mean',
            'vmed': 'mean',
            'periodo_integracion': 'mean',
            'error': 'first'  # Utilizar la función definida
        }).reset_index()

        # Seleccionar solo la primera fila de cada grupo para obtener una fila por cada 1 hora
        filtered_df = grouped_df.groupby(['id', 'hora_inicial', 'tipo_elem']).first().reset_index()

        # Renombrar la columna 'hora_inicial' a 'fecha'
        filtered_df = filtered_df.rename(columns={"hora_inicial": "fecha"})

        # Escribir la cabecera en el archivo CSV solo si es el primer archivo
        if not header_written:
            filtered_df.to_csv(output_csv, mode='w', index=False)
            header_written = True
        else:
            filtered_df.to_csv(output_csv, mode='a', header=False, index=False)

        # Imprimir información por pantalla
        print(f"Guardado en {output_csv}: {len(filtered_df)} registros del archivo {csv_file}")

print("Proceso completado.")
