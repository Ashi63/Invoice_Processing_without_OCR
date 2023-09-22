import streamlit as st
import time
import json
import os
from PIL import Image,ImageOps
from utils.text_getter import generate_result
from utils.list_of_fileds_question import fields_questions_list_for_invoice,fields_questions_list_for_bills
#from utils.invoice_classification import class_name_classify,confidence_score_classify
import subprocess
import tensorflow as tf
import numpy as np

# setting up the side bar for image upload.
st.sidebar.title('Upload Invoice Image')
st.sidebar.divider()
uploaded_image = st.sidebar.file_uploader('Upload Image Document',type=['jpg','jpeg','png'])
st.sidebar.divider()

# title of the application
st.title('Invoice Processing Application.')
st.divider()

# Initialize the columns
col1, col2 = st.columns(2,gap='large')

# display image in the column 2 and display success message for 3 sec and then disappear
if uploaded_image is not None:
    col1.subheader('Uploaded Image')
    col1.markdown('-----------')
    col1.image(uploaded_image)
    success_msg = col1.success('Image uploaded successfully')
    time.sleep(1)
    success_msg.empty()
    
    image = Image.open(uploaded_image)
     
    button_placeholder = st.empty()
    show_button = button_placeholder.button("Click to classify the image",type='primary')
        
    if show_button:
        col1.subheader('Image Classified As')
        col1.markdown('-----------')
        
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
        col1.text_input(label='Image Class Prediction',value=f"{class_name_classify[2:]}")
        col1.text_input(label='Confidence of Predicted Class',value=f"{confidence_score_classify:.2f}")    
        st.divider()
        
        # Clear the button_placeholder to remove the button    
        button_placeholder.empty()
        
        if class_name_classify[2:] == 'Restaurant_Bill':
            #from utils.list_of_fileds_question import fields_questions_list_for_bills
            # after uploading image successfully show the fields to be extracted from side bar
            st.sidebar.subheader('Select the fiels to be extracted.')
            
            # Initialize a dictionary to store extracted data
            extracted_data = {}
            
            # setting up the form in sidebar for feilds to be extracted.
            with st.form(key ='Form1'):
                with st.sidebar:
                    for field,question in fields_questions_list_for_bills.items():
                        st.sidebar.checkbox(field)
                    submit = st.form_submit_button(label='Extract Fields',type='secondary')
                    
                if submit:
                    st.subheader('Extracted Details')
                    st.markdown('-----------')

                    for field,question in fields_questions_list_for_bills.items():
                        user_question = question
                        answer = str.upper(generate_result(user_question,image))
                        st.text_input(field,value=answer)
                        extracted_data[field] = answer 
                                        
                    # After the form submission, you can convert the extracted_data dictionary to JSON
                    if extracted_data:
                        extracted_data_json = json.dumps(extracted_data, indent=4)
                        st.write("Extracted Data (JSON format):")
                        st.code(extracted_data_json)
                    
                    # make extracted_data folder for saving the extracted data from image
                    if 'extracted_data' not in os.listdir():
                        os.makedirs('extracted_data',exist_ok=True)
                        
                    # Save the JSON data to a file
                    with open('extracted_data/extracted_restaurant_data.json', 'w') as json_file:
                        json.dump(extracted_data, json_file, indent=4)

                    st.success("Extracted data saved to 'extracted_data.json'")
                
        elif class_name_classify[2:] == 'Invoices':
            #from utils.list_of_fileds_question import fields_questions_list_for_invoice
            # after uploading image successfully show the fields to be extracted from side bar
            st.sidebar.subheader('Select the fiels to be extracted.')
            
            # Initialize a dictionary to store extracted data
            extracted_data = {}
            
            # setting up the form in sidebar for feilds to be extracted.
            with st.form(key ='Form1'):
                with st.sidebar:
                    for field,question in fields_questions_list_for_invoice.items():
                        st.sidebar.checkbox(field)
                    submit = st.form_submit_button(label='Extract Fields',type='secondary')
                    
                if submit:
                    col2.subheader('Extracted Details')
                    col2.markdown('-----------')

                    for field,question in fields_questions_list_for_invoice.items():
                        user_question = question
                        answer = str.upper(generate_result(user_question,image))
                        col2.text_input(field,value=answer)
                        extracted_data[field] = answer 
                                        
                    # After the form submission, you can convert the extracted_data dictionary to JSON
                    if extracted_data:
                        extracted_data_json = json.dumps(extracted_data, indent=4)
                        st.write("Extracted Data (JSON format):")
                        st.code(extracted_data_json)
                    
                    # make extracted_data folder for saving the extracted data from image
                    if 'extracted_data' not in os.listdir():
                        os.makedirs('extracted_data',exist_ok=True)
                        
                    # Save the JSON data to a file
                    with open('extracted_data/extracted_invoice_data.json', 'w') as json_file:
                        json.dump(extracted_data, json_file, indent=4)

                    st.success("Extracted data saved to 'extracted_data.json'")
        else:
            st.warning("Document Image can't be classified we are working on it.")
            
