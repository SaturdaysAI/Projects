import os
import torch
import numpy as np
from flask import Flask, render_template, request, jsonify, redirect
from werkzeug.utils import secure_filename
import librosa
import soundfile as sf
import logging
import io
from scipy.io import wavfile

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Flask app setup
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'webm'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Limit file size to 16MB

# Ensure the upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Load the model
checkpoint = torch.load("best_model.pth", map_location=torch.device('cpu'))

# Initialize the model architecture
from architecture import CNNNetwork
model = CNNNetwork(num_mfcc=40)
model.load_state_dict(checkpoint['model_state_dict'])
model.eval()  # Set model to evaluation mode

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_audio_features(audio_data, sr=22050, n_mfcc=40, max_length=500):
    # Ensure audio_data is the correct shape (handle mono and stereo)
    if audio_data.ndim > 1:
        audio_data = np.mean(audio_data, axis=1)
    
    # Compute MFCC features
    mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=n_mfcc)
    
    # Pad or truncate to max_length
    if mfccs.shape[1] < max_length:
        mfccs = np.pad(mfccs, ((0, 0), (0, max_length - mfccs.shape[1])), mode='constant')
    else:
        mfccs = mfccs[:, :max_length]
    
    return mfccs

def predict_audio(model, features):
    features_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
    logging.debug(f"Input tensor shape: {features_tensor.shape}")
    
    with torch.no_grad():
        output = model(features_tensor)
        prediction = torch.sigmoid(output).item()
    
    logging.debug(f"Raw prediction: {prediction}")
    return prediction

def process_audio_in_chunks(audio_data, sr, chunk_duration=5):
    chunk_size = int(sr * chunk_duration)
    predictions = []
    
    for i in range(0, len(audio_data), chunk_size):
        chunk = audio_data[i:i+chunk_size]
        if len(chunk) < chunk_size:
            chunk = np.pad(chunk, (0, chunk_size - len(chunk)), mode='constant')
        features = extract_audio_features(chunk, sr=sr)
        pred = predict_audio(model, features)
        predictions.append(pred)
    
    return predictions

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            try:
                y, sr = librosa.load(file_path, sr=22050)
                predictions = process_audio_in_chunks(y, sr)
                
                is_real = "Real Voice" if sum(pred >= 0.5 for pred in predictions) / len(predictions) > 0.5 else "Fake Voice"
                
                os.remove(file_path)

                return render_template("index.html", pred=is_real)
            
            except Exception as e:
                logging.error(f"Error processing audio file: {str(e)}")
                return render_template("index.html", pred="Error processing audio")

    return render_template("index.html")

@app.route("/predict_chunk", methods=["POST"])
def predict_chunk():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No audio chunk provided"}), 400

        audio_chunk = request.files['file']
        
        # Process the audio chunk
        audio_data = audio_chunk.read()
        sr, y = wavfile.read(io.BytesIO(audio_data))
        
        # Convert int16 to float32
        y = y.astype(np.float32) / np.iinfo(np.int16).max
        
        # Extract features
        features = extract_audio_features(y, sr=sr)
        
        # Predict using the model
        pred = predict_audio(model, features)
        logging.debug(f"Backend prediction: {pred}")

        return jsonify({"prediction": float(pred)})

    except Exception as e:
        logging.error(f"Error processing audio chunk: {str(e)}", exc_info=True)
        return jsonify({"error": "Error processing audio"}), 500

if __name__ == "__main__":
    app.run(debug=True)