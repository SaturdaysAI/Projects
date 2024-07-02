from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import requests

class LLMRequest(BaseModel):
    ruta_imagen: str
    prediction: str

llm_app = APIRouter()

@llm_app.post('/llm_model', description="Ruta para tener acceso al LLM multimodal LLAVA")
async def obtener_recomendacion_imagen(data: LLMRequest):
    # Define the API endpoint URL
    url = "http://localhost:11434/v1/chat/completions"

    # Prepare the request data as a dictionary
    request_data = {
        "model": "llava-phi3",  # Corrected model name
        "messages": [
            {
                "role": "system",
                "content": "You are a very helpful assistant. Responde en Español."
            },
            {
                "role": "user",
                "content": f"{data.ruta_imagen} describe la planta de tomate y dame recomendaciones para su salud. Esta es la enfermedad que se predijo en ella: {data.prediction}."  # Interpolate the variable
            }
        ],
        "options": {
            "num_predict": 10,
            "num_ctx": 16384
        }
    }

    # Set the headers indicating JSON content type
    headers = {"Content-Type": "application/json"}

    try:
        # Send the POST request with JSON data
        response = requests.post(url, headers=headers, json=request_data)

        # Check for successful response
        if response.status_code == 200:
            # Parse the JSON response
            response_data = response.json()

            # Extract the content values from each message
            messages = [choice.get("message", {}).get("content", "Contenido no disponible")
                        for choice in response_data.get("choices", [])]

            return {"response": messages}
        else:
            raise HTTPException(status_code=response.status_code, detail=f"Error: {response.status_code}")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))
