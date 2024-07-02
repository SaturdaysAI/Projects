import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import os
import glob

st.title("Diagnóstico de Plantas de Tomate")

st.write("Toma una foto de la planta de tomate para obtener un diagnóstico.")

uploaded_file = st.file_uploader("Elige una imagen...", type=["jpg", "jpeg", "png"], accept_multiple_files=False)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Imagen subida.', use_column_width=True)

    save_dir = "C:\\Users\\ferna\\OneDrive\\Escritorio\\GitHub\\AITomato\\image_files"
    os.makedirs(save_dir, exist_ok=True)

    # Eliminar imágenes anteriores
    files = glob.glob(os.path.join(save_dir, '*'))
    for f in files:
        os.remove(f)

    save_path = os.path.join(save_dir, uploaded_file.name)
    image.save(save_path)

    if st.button("Enviar para Diagnóstico"):
        st.write("Enviando imagen...")

        # Convertir la imagen a un formato que pueda ser enviado
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        buffered.seek(0)

        files = {'file': ("uploaded_image.jpg", buffered, "image/jpeg")}

        try:
            # Enviar la imagen para diagnóstico
            response = requests.post("http://localhost:8000/predict", files=files)
            if response.status_code == 200:
                result = response.json()
                st.write("Resultado del diagnóstico:")
                st.write(result['prediction'])  # Mostrar solo la predicción
                prediction = result['prediction']
            else:
                st.write("Error al enviar la imagen para diagnóstico.")
                st.write(f"Status code: {response.status_code}")
                st.write(response.text)
                raise Exception("Error en el diagnóstico")

            # Enviar datos al LLM
            st.write("Obteniendo recomendaciones del LLM...")
            response_llm = requests.post(
                "http://localhost:8000/llm_model",
                json={'ruta_imagen': save_path, 'prediction': prediction}
            )
            if response_llm.status_code == 200:
                result_llm = response_llm.json()
                st.write("Recomendaciones del LLM:")
                st.write(result_llm['response'])
            else:
                st.write("Error al obtener la recomendación del LLM.")
                st.write(f"Status code: {response_llm.status_code}")
                st.write(response_llm.text)
                raise Exception("Error en el LLM")
        except requests.exceptions.RequestException as e:
            st.write("Ocurrió una excepción al enviar la imagen")
            st.write(e)
        except Exception as e:
            st.write(f"Ocurrió una excepción: {e}")
