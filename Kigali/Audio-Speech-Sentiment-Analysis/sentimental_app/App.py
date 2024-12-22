from flask import Flask, request, jsonify
import os
from werkzeug.utils import secure_filename
from model import SentimentModel
from utils import preprocess_audio
import torch
from flask_cors import CORS
from flasgger import Swagger, swag_from 

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'wav', 'mp3'}

app = Flask(__name__)
CORS(app)
Swagger(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize model
model = SentimentModel()
model.load_state_dict(torch.load('model/best_model.pth', map_location=torch.device('cpu')))
model.eval()

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_audio_tensor(tensor):
    """
    Validate and reshape audio tensor if necessary.
    """
    if not isinstance(tensor, torch.Tensor):
        raise ValueError("Invalid audio format")
    
    if len(tensor.shape) == 1:
        tensor = tensor.unsqueeze(0)
    
    expected_feature_size = 2048
    
    if tensor.shape[1] != expected_feature_size:
        if tensor.shape[1] > expected_feature_size:
            tensor = tensor[:, :expected_feature_size]
        else:
            padding_size = expected_feature_size - tensor.shape[1]
            tensor = torch.nn.functional.pad(tensor, (0, padding_size))
    
    return tensor

@app.route('/predict', methods=['POST'])
@swag_from('docs/predict.yml')
def upload_and_predict():
    if 'file' not in request.files:
        return jsonify({
            "success": False,
            "message": "Please select an audio file"
        }), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({
            "success": False,
            "message": "No file selected"
        }), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        try:
            # Process audio and make prediction
            audio_tensor = preprocess_audio(file_path)
            audio_tensor = validate_audio_tensor(audio_tensor)
            
            with torch.no_grad():
                output = model(audio_tensor)
                prediction = torch.argmax(output, dim=1).item()
                sentiment = ['negative', 'neutral', 'positive'][prediction]
                
                # Clean up the uploaded file
                os.remove(file_path)
                
                return jsonify({
                    "success": True,
                    "sentiment": sentiment,
                    "message": f"Analysis complete: {sentiment} sentiment detected"
                }), 200
                
        except Exception as e:
            # Clean up the uploaded file in case of error
            if os.path.exists(file_path):
                os.remove(file_path)
            
            return jsonify({
                "success": False,
                "message": "Unable to process audio file. Please ensure it's a valid audio recording."
            }), 500
    
    return jsonify({
        "success": False,
        "message": "Please upload a WAV or MP3 file"
    }), 400

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=False, host='0.0.0.0')