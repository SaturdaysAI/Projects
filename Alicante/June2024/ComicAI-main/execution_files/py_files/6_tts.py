from packages import *

def text_to_audio(file_path, output_path, lang='es'):
    # Lee el contenido del archivo de texto
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().strip()  # Lee y elimina espacios en blanco adicionales
    
    # Verifica si el texto está vacío
    if not text:
        header_text = "La viñeta solo contiene texto"
    else:
        # Agrega el encabezado al texto
        header_text = f"La viñeta contiene:    {text}"
    
    # Genera el objeto gTTS con el acento especificado
    tts = gTTS(text=header_text, lang=lang)
    
    # Define el nombre del archivo de salida
    audio_file = output_path.with_suffix('.mp3')
    
    # Crea el directorio de salida si no existe
    audio_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Guarda el archivo de audio
    tts.save(audio_file)
    
    print(f"Guardado: {audio_file}")

def process_directory(input_dir, output_dir, lang='es'):
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    for text_file in input_path.rglob('*.txt'):
        # Calcula la ruta de salida
        relative_path = text_file.relative_to(input_path)
        output_file = output_path / relative_path.with_suffix('.mp3')  # Ajusta la extensión
        text_to_audio(text_file, output_file, lang)

# Directorio de entrada
input_directory_description = r'.\data\output\output_description_translate_test'

# Directorio de salida
output_directory = r'.\data\output\output_audio_test\description'

# Llama a la función para procesar el directorio
process_directory(input_directory_description, output_directory)

print("Audio de descripciones finalizado")

def text_to_audio(file_path, output_path, lang='es'):
    # Lee el contenido del archivo de texto
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().strip()  # Lee y elimina espacios en blanco adicionales
    
    # Verifica si el texto está vacío
    if not text:
        header_text = "La viñeta no contiene texto"
    else:
        # Agrega el encabezado al texto
        header_text = f"El texto de la viñeta es:    {text}"
    
    # Genera el objeto gTTS con el acento especificado
    tts = gTTS(text=header_text, lang=lang)
    
    # Define el nombre del archivo de salida
    audio_file = output_path.with_suffix('.mp3')
    
    # Crea el directorio de salida si no existe
    audio_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Guarda el archivo de audio
    tts.save(audio_file)
    
    print(f"Guardado: {audio_file}")

def process_directory(input_dir, output_dir, lang='es'):
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    for text_file in input_path.rglob('*.txt'):
        # Calcula la ruta de salida
        relative_path = text_file.relative_to(input_path)
        output_file = output_path / relative_path.with_suffix('.mp3')  # Ajusta la extensión
        text_to_audio(text_file, output_file, lang)

# Directorio de entrada
input_directory_description = r'.\data\output\output_text_test'

# Directorio de salida
output_directory = r'.\data\output\output_audio_test\text'

# Llama a la función para procesar el directorio
process_directory(input_directory_description, output_directory)

print("Audio de texto finalizado")

def merge_audios(description_audio_file, text_audio_file, output_file):
    try:
        description_audio = AudioFileClip(description_audio_file)
        text_audio = AudioFileClip(text_audio_file)
        combined_audio = concatenate_audioclips([description_audio, text_audio])
        combined_audio.write_audiofile(output_file, codec='mp3')
        print(f"Audio combinado guardado: {output_file}")
    except Exception as e:
        print(f"Error al combinar audios: {e}")

def process_and_merge(input_directory_description_audio, input_directory_text_audio, output_directory_combined):
    if not os.path.exists(output_directory_combined):
        os.makedirs(output_directory_combined)
    
    for root, _, files in os.walk(input_directory_description_audio):
        for file in files:
            if file.endswith(".mp3"):
                description_file_path = os.path.join(root, file)
                relative_path = os.path.relpath(description_file_path, input_directory_description_audio)
                text_file_path = os.path.join(input_directory_text_audio, relative_path)

                if os.path.exists(text_file_path):
                    output_file_path = os.path.join(output_directory_combined, relative_path)
                    output_file_dir = os.path.dirname(output_file_path)
                    if not os.path.exists(output_file_dir):
                        os.makedirs(output_file_dir)
                    merge_audios(description_file_path, text_file_path, output_file_path)
                else:
                    print(f"No se encontró el archivo de texto correspondiente para: {description_file_path}")

# Directorios de entrada
input_directory_description_audio = r'.\data\output\output_audio_test\description'
input_directory_text_audio = r'.\data\output\output_audio_test\text'

# Directorio de salida
output_directory_combined = r'.\data\output\output_audio_test\combined'

# Llama a la función para procesar y combinar los audios
process_and_merge(input_directory_description_audio, input_directory_text_audio, output_directory_combined)

print("Audio combinado finalizado")