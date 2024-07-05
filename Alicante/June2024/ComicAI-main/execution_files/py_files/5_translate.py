from packages import *


# Función para traducir texto usando GoogleTranslator
def traducir_texto(texto):
    if texto.strip().lower() == "nan":
        return ""
    try:
        return GoogleTranslator(source='en', target='es').translate(texto)
    except Exception as e:
        print(f'Error en la traducción: {e}')
        return ""

# Función para procesar archivos en un directorio y sus subdirectorios
def procesar_directorio(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".txt"):
                input_path = os.path.join(root, file)
                relative_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, relative_path)

                # Crear directorio de salida si no existe
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Leer contenido del archivo
                with open(input_path, 'r', encoding='utf-8') as f:
                    contenido = f.read()

                # Traducir contenido
                traduccion = traducir_texto(contenido)

                # Imprimir texto original y traducción
                print(f'Texto original: {contenido}')
                print(f'Traducción: {traduccion}')

                # Guardar traducción en archivo de salida
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(traduccion)

# Ruta del directorio de entrada y salida
input_dir = r".\data\output\output_description_test"
output_dir = r".\data\output\output_description_translate_test"

# Procesar el directorio
procesar_directorio(input_dir, output_dir)