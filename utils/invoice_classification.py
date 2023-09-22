import streamlit as st
import time
from PIL import Image,ImageOps
import tensorflow as tf
import numpy as np

# setting up the side bar for image upload.
st.sidebar.title('Image Classification')
st.sidebar.divider()
uploaded_image = st.sidebar.file_uploader('Upload Image Document',type=['jpg','jpeg','png'])
st.sidebar.divider()

# title of the application
st.title('Invoice Classification Application.')
st.divider()

# Initialize the columns
col1, col2 = st.columns(2,gap='large')

# display image in the column 2 and display success message for 3 sec and then disappear
if uploaded_image is not None:
    col1.subheader('Uploaded Image')
    col1.markdown('-----------')
    col1.image(uploaded_image)
    success_msg = col1.success('Image uploaded successfully')
    time.sleep(3)
    success_msg.empty()
    
    #image = Image.open(uploaded_image)

    col2.subheader('Image Classified As')
    col2.markdown('-----------')
    
    @st.cache_resource()
    def load_keras_model():
        return tf.keras.models.load_model("models/keras_Model.h5", compile=False)

    model = load_keras_model()  
    
    # Load the image classification labels
    with open("models/labels.txt", "r") as labels_file:
        class_names = [line.strip() for line in labels_file.readlines()]
    
    # Preprocess the uploaded image for classification
    image_classify = Image.open(uploaded_image).convert("RGB")
    size_classify = (224, 224)
    image_classify = ImageOps.fit(image_classify, size_classify, Image.Resampling.LANCZOS)
    image_array_classify = np.asarray(image_classify)
    normalized_image_array_classify = (image_array_classify.astype(np.float32) / 127.5) - 1
    data_classify = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data_classify[0] = normalized_image_array_classify

    # Make a prediction for image classification
    prediction_classify = model.predict(data_classify)
    index_classify = np.argmax(prediction_classify)
    class_name_classify = class_names[index_classify]
    confidence_score_classify = prediction_classify[0][index_classify]

    # Display the classification prediction and confidence score
    #st.subheader("Image Classification Prediction:")
    col2.text_input(label='Image Class Prediction',value=f"{class_name_classify[2:]}")
    col2.text_input(label='Confidence of Predicted Class',value=f"{confidence_score_classify:.2f}")    
    
    