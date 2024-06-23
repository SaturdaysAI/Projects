import tensorflow as tf
import os
import tensorflow_hub as hub
import keras


from flask import Flask, jsonify, request

import joblib
from text_processingStress import preprocess
from calcular_vector import get_w2v_vectors

from text_processingEmotions import clean_text

#disable CUDA no GPU computers
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

# Load the model with custom objects
with keras.utils.custom_object_scope({"KerasLayer": hub.KerasLayer}):
        model = tf.keras.models.load_model('emotionsModelWithCleanData.h5')

# Load the model from the file
gb_clf3_loaded = joblib.load('gb_clf3_model.joblib')

app = Flask(__name__)

print("endpoint 2")

@app.route('/analyze', methods=['GET'])

def analyzeText():

    text = request.args.get('text', "im forever taking some time out to have a lie down because i feel weird")  # Default to 'World' if no name is provided

    text = clean_text(text)

    predictions = model.predict(tf.convert_to_tensor([text], dtype=tf.string))

    # Convert the NumPy array to a list
    array_list = predictions.tolist()


    return jsonify({
        "sadness"   :      array_list[0][0],
        "joy"       :      array_list[0][1],
        "love"      :      array_list[0][2],
        "anger"     :      array_list[0][3],
        "fear"      :      array_list[0][4],
        "surprise"  :      array_list[0][5]
        
    })

@app.route('/analyzeStress', methods=['GET'])

def analyzeTextStress():
     
    text = request.args.get('text', "keep calm and have a good day") 
    #text = request.args.get('text', tweet) 

    tp = get_w2v_vectors(preprocess(text))

    # Verify the loaded model
    predictions = gb_clf3_loaded.predict([tp])

    return jsonify({ "pred" : str(predictions[0]) })

if __name__ == '__main__':
    app.run(debug=True)


