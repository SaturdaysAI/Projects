import streamlit as st
from tensorflow.keras.models import load_model
from ecg import ECG
import matplotlib.pyplot as plt

# Añadir una imagen en la parte superior de la aplicación
st.image("img.png", use_column_width=True)

# Título de la aplicación
st.title("Predicción de Infarto de Miocardio mediante ECG")

# Descripción breve
st.markdown("""
Esta aplicación permite cargar una imagen de un electrocardiograma (ECG), procesarla y utilizar un modelo de aprendizaje automático para predecir la posibilidad de un infarto de miocardio.
""")

# Initialize ECG object
ecg = ECG()

# Requires model in local repository
model = load_model("models/cnn_model.h5")

# Upload image
uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    """#### **UPLOADED IMAGE**"""
    ecg_user_image_read = ecg.getImage(uploaded_file)
    st.image(ecg_user_image_read)

    """#### **GRAY SCALE IMAGE**"""
    ecg_user_gray_image_read = ecg.GrayImage(ecg_user_image_read)
    my_expander = st.expander(label="Gray SCALE IMAGE")
    with my_expander:
        st.image(ecg_user_gray_image_read)

    """#### **DIVIDING LEADS**"""
    dividing_leads = ecg.DividingLeads(ecg_user_image_read)
    my_expander1 = st.expander(label="DIVIDING LEAD")
    with my_expander1:
        for lead in dividing_leads:
            st.image(lead)

    """#### **PREPROCESSED LEADS**"""
    ecg_preprocessed_leads = ecg.PreprocessingLeads(dividing_leads)
    my_expander2 = st.expander(label="PREPROCESSED LEAD")
    with my_expander2:
        for lead in ecg_preprocessed_leads:
            fig, ax = plt.subplots()
            ax.imshow(lead, cmap="gray")
            st.pyplot(fig)

    """#### **EXTRACTING SIGNALS(1-12)**"""
    ec_signal_extraction = ecg.SignalExtraction_Scaling(ecg_preprocessed_leads)
    my_expander3 = st.expander(label="CONTOUR LEADS")
    with my_expander3:
        for signal in ec_signal_extraction:
            fig, ax = plt.subplots()
            ax.plot(signal)
            st.pyplot(fig)

    """#### **CONVERTING TO 1D SIGNAL**"""
    ecg_1dsignal = ecg.CombineConvert1Dsignal(ec_signal_extraction)
    my_expander4 = st.expander(label="1D Signals")
    with my_expander4:
        st.write(ecg_1dsignal)

    """#### **PERFORM DIMENSIONALITY REDUCTION**"""
    ecg_final = ecg.DimensionalReduction(ecg_1dsignal)
    my_expander4 = st.expander(label="Dimensional Reduction")
    with my_expander4:
        st.write(ecg_final)

    """#### **PASS TO PRETRAINED ML MODEL FOR PREDICTION**"""
    ecg_model = ecg.ModelLoad_predict(ecg_final, model)
    my_expander5 = st.expander(label="PREDICTION")
    with my_expander5:
        st.write(ecg_model)
        if ecg_model[0][0] > 0.5:
            st.write("La predicción es: MI (Infarto de Miocardio)")
        else:
            st.write("La predicción es: NORMAL")
else:
    st.write("Esperando una imagen para predecir...")
