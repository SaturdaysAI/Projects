from fastapi import FastAPI, APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

upload_app = APIRouter()

# Función para enviar la imagen al modelo y obtener el resultado
def predict_plant_health(image_bytes: bytes) -> str:
    logger.info("Sending image to model for prediction...")
    model_endpoint = "http://localhost:8000/predict"  # Cambia esto por la URL de tu modelo
    files = {"file": ("image.jpg", image_bytes, "image/jpeg")}
    response = requests.post(model_endpoint, files=files)
    if response.status_code == 200:
        result = response.json()
        logger.info("Received prediction: %s", result["prediction"])
        return result["prediction"]
    else:
        logger.error("Error in model prediction: %s", response.text)
        raise HTTPException(status_code=response.status_code, detail="Error al procesar la imagen")

@upload_app.post("/upload/")
async def upload_files(file: UploadFile = File(...)):
    logger.info("Received file: %s", file.filename)
    image_bytes = await file.read()
    logger.info("Read file contents successfully")
    prediction = predict_plant_health(image_bytes)
    logger.info("Prediction result: %s", prediction)
    return JSONResponse(content={"prediction": prediction})