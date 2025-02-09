from flask import Flask, request, jsonify
import joblib
import pandas as pd

# Cargar el modelo
model = joblib.load('taxi_fare_model.pkl')

# Crear la aplicación Flask
app = Flask(__name__)

# Definir la ruta para la predicción
@app.route('/predict', methods=['POST'])
def predict():
    # Obtener los datos de la solicitud
    data = request.get_json(force=True)
    
    # Convertir los datos a un DataFrame
    df = pd.DataFrame(data)
    
    # Realizar la predicción
    prediction = model.predict(df)
    
    # Devolver la predicción como respuesta JSON
    return jsonify({'prediction': prediction.tolist()})

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
