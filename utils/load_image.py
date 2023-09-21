import streamlit as st
from PIL import Image


def image_loader():
    # load image in side bar
    st.sidebar.title("Upload image")
    uploaded_image = st.sidebar.file_uploader("Upload a document image",type=['jpg','jpeg','png',])
    return uploaded_image
    
    

    
