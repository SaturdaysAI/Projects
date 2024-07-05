from packages import *

# Configurar el dispositivo (GPU o CPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Cargar el modelo afinado y moverlo al dispositivo
finetuned_model = BlipForConditionalGeneration.from_pretrained(r"./train/results").to(device)
finetuned_processor = BlipProcessor.from_pretrained(r"./train/results")

# Cargar el procesador y el modelo
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to(device)

# Directorio de imágenes y directorio de salida
base_image_dir = r'./data/output/divide_images_test'
output_dir = r'./data/output/output_description_test'

# Función para cargar y preprocesar una imagen
def load_and_preprocess_image(image_path):
    image = Image.open(image_path).convert("RGB")
    inputs = processor(images=image, return_tensors="pt")
    return inputs, image

# Función para crear un archivo .txt con el nombre de la imagen y contenido "Finetuned"
def create_txt_file(image_file, output_file_dir):
    txt_path = os.path.join(output_file_dir, f"{os.path.splitext(image_file)[0]}.txt")
    with open(txt_path, 'w') as f:
        f.write(finetuned_caption)

# Recorre todas las carpetas y archivos dentro de base_image_dir
for root, dirs, files in os.walk(base_image_dir):
    for file in files:
        if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')):
            # Construir la ruta completa de la imagen
            image_path = os.path.join(root, file)
            
            # Procesar la imagen
            inputs, image = load_and_preprocess_image(image_path)
            
            # Mover los datos al dispositivo
            inputs = {key: tensor.to(device) for key, tensor in inputs.items()}
            
            # Generar descripción con el modelo original
            original_outputs = model.generate(
                **inputs,
                max_length=100,
                num_beams=5,
                length_penalty=2.0,
                early_stopping=True
            )
            original_caption = processor.decode(original_outputs[0], skip_special_tokens=True)
            
            # Generar descripción con el modelo afinado
            finetuned_outputs = finetuned_model.generate(
                **inputs,
                max_length=100,
                num_beams=5,
                length_penalty=2.0,
                early_stopping=True
            )
            finetuned_caption = finetuned_processor.decode(finetuned_outputs[0], skip_special_tokens=True)
            
            # Crear la estructura de carpetas en el directorio de salida
            relative_path = os.path.relpath(root, base_image_dir)
            output_file_dir = os.path.join(output_dir, relative_path)
            os.makedirs(output_file_dir, exist_ok=True)
            
            # Crear el archivo .txt con el nombre de la imagen y contenido "Finetuned"
            create_txt_file(file, output_file_dir)