import streamlit as st
import time
import json
import os
from PIL import Image
from utils.text_getter import generate_result
from utils.list_of_fileds_question import fields_questions_list_for_invoice

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
    time.sleep(3)
    success_msg.empty()
    
    image = Image.open(uploaded_image)
    
    # after uploading image successfully show the fields to be extracted from side bar
    st.sidebar.subheader('Select the fiels to be extracted.')
    
    # Initialize a dictionary to store extracted data
    extracted_data = {}
    
    # setting up the form in sidebar for feilds to be extracted.
    with st.form(key ='Form1'):
        with st.sidebar:
            for field,question in fields_questions_list_for_invoice.items():
                st.sidebar.checkbox(field)
            submit = st.form_submit_button(label='Extract Fields',type='primary')
            
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
            with open('extracted_data/extracted_data.json', 'w') as json_file:
                json.dump(extracted_data, json_file, indent=4)

            st.success("Extracted data saved to 'extracted_data.json'")    
else:
    st.warning('Upload Image')   

                