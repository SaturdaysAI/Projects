import io
from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from PIL import Image
from keras._tf_keras.keras.preprocessing import image as keras_image
from keras._tf_keras.keras.models import load_model
import numpy as np

# FastAPI setup
predict_app = APIRouter()

# Cargar el modelo Keras y los pesos
model = load_model('ModelsAndWeights/resnet50_model.h5')
model.load_weights('ModelsAndWeights/best_model.weights.h5')

# Definir las etiquetas
labels = [
    'Bacterial_spot', 'Early_blight', 'Late_blight', 'Leaf_Mold', 
    'Septoria_leaf_spot', 'Spider_mites_Two-spotted_spider_mite', 
    'Target_Spot', 'Tomato_Yellow_Leaf_Curl_Virus', 'Tomato_mosaic_virus', 
    'healthy', 'powdery_mildew'
]

def predict(image_bytes):
    # Convertir bytes a imagen
    image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    # Redimensionar y preprocesar la imagen
    img = keras_image.img_to_array(image)
    img = keras_image.smart_resize(img, (224, 224))
    img = np.expand_dims(img, axis=0)
    # Realizar predicción
    prediction = model.predict(img)
    predicted_label = labels[np.argmax(prediction)]
    return predicted_label

@predict_app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    # Log para verificar que se recibió el archivo
    print("Received file for prediction:", file.filename)
    image_bytes = await file.read()
    # Realizar la predicción
    prediction = predict(image_bytes)
    # Log del resultado de la predicción
    print("Prediction result:", prediction)
    # Devolver la predicción como respuesta JSON
    return JSONResponse(content={"prediction": prediction})
