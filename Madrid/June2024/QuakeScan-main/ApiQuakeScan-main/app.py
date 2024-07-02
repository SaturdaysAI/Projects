
from flask import Flask, json, jsonify, request, make_response
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import sys
import io
import tensorflow as tf

app = Flask(__name__)

longitud, altura = 150, 150
modelo = 'Url del modelo'
pesos = 'url del modelo'



cnn = load_model(modelo, compile=False)
cnn.load_weights(pesos)



@app.route('/')
def Home():  
  return 'API to detect crash in buildings .. '

@app.route('/predict', methods=['POST'] )
def Predict():
  try:
    file = request.files['file'].read()
    image = Image.open(io.BytesIO(file))    
    resizedImage = image.resize((longitud, altura))
    x = np.expand_dims(resizedImage, axis=0)   
    predictions = cnn.predict(x)  
    predicted_class = np.argmax(predictions, axis=1) 
    class_names = ['COLLAPSE', 'COMBINED CORNERS', 'DAMAGE TO INFILL', 'DISLODGEMENTS', 'IP PARTIAL COLLAPSE', 'PARTIAL COLLAPSE', 'POUNDING LEANING',
                   'RC ST FAILURE', 'SPALLING', 'TOE CRUSHING']
    predicted_label = class_names[predicted_class[0]]
    res = jsonify(result=predicted_label, status = True)
    return make_response(res, 200)
  except :
    res = jsonify(status = False, message = str(sys.exc_info() ) )
    return make_response(res, 500)
 

if __name__ == '__main__':
    app.run()
