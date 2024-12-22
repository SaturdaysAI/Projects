# app.py

import streamlit as st
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import io
import time

# Set page config
st.set_page_config(page_title="Malaria Detection App", layout="wide", initial_sidebar_state="expanded")

# Custom CSS to improve the app's appearance
st.markdown("""
<style>
    /* Main content */
    .main > div {
        padding-top: 2rem;
    }
    .block-container {
        max-width: 80rem;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    /* Headings */
    h1, h2, h3 {
        color: #1E88E5;
    }
    /* Custom classes */
    .big-font {
        font-size: 3rem !important;
        font-weight: bold;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .subtitle {
        font-size: 1.5rem;
        color: #424242;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result {
        font-size: 2rem;
        font-weight: bold;
        margin-top: 2rem;
        text-align: center;
    }
    .upload-box {
        border: 3px dashed #1E88E5;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stAlert {
        font-size: 1.2rem;
    }
    /* Sidebar */
    .css-1d391kg {
        padding-top: 3rem;
    }
    .sidebar .sidebar-content {
        background-color: #f1f8fe;
    }
    .sidebar .img{
            width:64px;
            witdth:64px;
            }
</style>
""", unsafe_allow_html=True)

# Load the model
@st.cache_resource
def load_malaria_model():
    try:
        model = load_model("new_model_new_update.hdf5", compile=False)
        model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
        return model
    except Exception as e:
        st.error(f"Error loading the model: {str(e)}")
        st.error(f"TensorFlow version: {tf.__version__}")
        st.error(f"Keras version: {tf.keras.__version__}")
        return None

model = load_malaria_model()


from tensorflow.keras.utils import img_to_array  # Changed import
import numpy as np
from PIL import Image

def preprocess_image(input_image):  # Changed parameter name to avoid confusion
    # Ensure input is a PIL Image
    if not isinstance(input_image, Image.Image):
        input_image = Image.fromarray(input_image)
    
    # Resize image
    resized_img = input_image.resize((224, 224))
    
    # Convert PIL Image to numpy array
    img_array = img_to_array(resized_img)  # Using img_to_array directly
    
    # Add batch dimension
    img_array = np.expand_dims(img_array, axis=0)
    
    # Normalize pixel values
    return img_array / 255.0
# Main app
st.markdown('<h1 class="big-font">Malaria Cell Detection</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload an image of a cell to detect if it\'s infected with malaria.</p>', unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns([1, 1])

with col1:
    st.markdown('<div class="upload-box">', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    st.markdown('</div>', unsafe_allow_html=True)

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption='Uploaded Image', use_column_width=True)

with col2:
  if uploaded_file is not None:
        
    if st.button('Analyze Image'):
        # Show spinner while processing
        with st.spinner('Analyzing image...'):
            processed_image = preprocess_image(image)
            prediction = model.predict(processed_image)
            time.sleep(2)  # Simulate delay for processing
        
        st.markdown('<p class="result">Result:</p>', unsafe_allow_html=True)
        
        # Adjusted the logic to show correct confidence for both cases
        if prediction[0][0] < 0.5:
            st.error(f"The cell is likely infected with malaria. (Confidence: {prediction[0][0]:.4f})")
        else:
            st.success(f"The cell is likely uninfected. (Confidence: {prediction[0][0]:.4f})")

        # Add additional information about the prediction
        st.info("Note: This prediction is based on the model's analysis. For accurate medical diagnosis, please consult with a healthcare professional.")
    else:
        st.markdown('<p class="subtitle">Upload an image to start the analysis.</p>', unsafe_allow_html=True)


# Sidebar
st.sidebar.image("https://www.manomedical.com/medias/product/big/6635/b01-microscope.png", use_column_width=True)
st.sidebar.title("About")
st.sidebar.info("This app uses a deep learning model to detect malaria-infected cells from cell images. Upload an image to get started.")

# Add instructions
st.sidebar.title("Instructions")
st.sidebar.markdown("""
1. Click on 'Choose an image...' or drag and drop an image file.
2. The app will display the uploaded image.
3. Click the 'Analyze Image' button to process the image.
4. The model will analyze the image and provide a prediction.
5. The result will show whether the cell is likely infected or uninfected.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("Created with ❤️")

st.markdown("---")
st.markdown("## Frequently Asked Questions")

faq_data = [
    ("What is malaria?", "Malaria is a life-threatening disease caused by parasites that are transmitted to people through the bites of infected female Anopheles mosquitoes."),
    ("How accurate is this model?", "This model is for demonstration purposes and should not be used for actual medical diagnosis. Always consult with a healthcare professional for accurate diagnosis."),
    ("Can I use my own images?", "Yes, you can upload your own cell images. However, the model is trained on specific types of cell images, so results may vary with different image types."),
    ("How does the model work?", "The model uses a deep learning algorithm trained on thousands of cell images to distinguish between infected and uninfected cells based on their visual characteristics.")
]

for question, answer in faq_data:
    with st.expander(question):
        st.write(answer)
