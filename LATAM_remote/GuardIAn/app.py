from msilib.schema import CheckBox
import cv2
import streamlit as st
import  detect




st.title("GuardIAn")
FRAME_WINDOW = st.image([])
detect.run(source = 0,output = FRAME_WINDOW.image)


