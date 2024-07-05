from packages import *

# Función para crear directorios si no existen
def crear_directorios_si_no_existen():
    # Directorio de salida para las imágenes
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Directorio '{output_directory}' creado correctamente.")
    else:
        print(f"El directorio '{output_directory}' ya existe.")
    
    # Directorio para el archivo CSV de rutas
    routes_directory = os.path.dirname(output_directory_csv)
    if not os.path.exists(routes_directory):
        os.makedirs(routes_directory)
        print(f"Directorio '{routes_directory}' creado correctamente.")
    else:
        print(f"El directorio '{routes_directory}' ya existe.")

# Función para dividir las páginas del pdf
def extract_images_from_pdf(pdf_path, output_folder):
    document = fitz.open(pdf_path)
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        images = page.get_images(full=True)
        for img_index, img in enumerate(images):
            xref = img[0]
            base_image = document.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            image_path = os.path.join(output_folder, f"page{page_num+1}_img.{image_ext}")
            with open(image_path, "wb") as img_file:
                img_file.write(image_bytes)
    print(f"Images extracted and saved to {output_folder}")

# Función para crear un archivo con todas las rutas de las páginas separadas anteriormente
def create_image_list(input_folder, output_csv):
    # Crear y escribir en el archivo CSV
    with open(output_csv, mode='a', newline='') as file:
        writer = csv.writer(file)
        for img_name in os.listdir(input_folder):
            img_path = os.path.join(input_folder, img_name)
            writer.writerow([img_path])

# Definir los directorios de entrada y salida
input_directory = r'.\data\input\Comic_test'
output_directory = r'.\data\output\divide_pages_test\pages_raw'
output_directory_csv = r'.\data\output\divide_pages_test\pages_routes\images_routes.csv'

# Verificar y crear directorios necesarios
crear_directorios_si_no_existen()

# Procesar archivos y crear listas de rutas
for raiz, subcarpetas, archivos in os.walk(input_directory):
    for subcarpeta in subcarpetas:
        ruta_carpeta_salida = os.path.join(output_directory, subcarpeta)
        if not os.path.exists(ruta_carpeta_salida):
            os.makedirs(ruta_carpeta_salida)
            print(f"Directorio '{ruta_carpeta_salida}' creado correctamente.")
        directorio_procesado = os.path.join(input_directory, subcarpeta)
        for nombre_archivo in os.listdir(directorio_procesado):
            archivo_completo = os.path.join(directorio_procesado, nombre_archivo)
            extract_images_from_pdf(archivo_completo, ruta_carpeta_salida)
            create_image_list(ruta_carpeta_salida, output_directory_csv)
            print(f"Fichero de rutas creado en {output_directory_csv} !")