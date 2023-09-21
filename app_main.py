import streamlit as st
import time
import json
from PIL import Image
from utils.text_getter import generate_result

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
            checkbox_invoice = st.sidebar.checkbox('Invoice Number')
            checkbox_date_of_issue = st.sidebar.checkbox('Date of issue')
            checkbox_iban_code = st.sidebar.checkbox('IBAN code')
            checkbox_net_worth = st.sidebar.checkbox('Total Net Worth')
            checkbox_gross_worth = st.sidebar.checkbox('Total Gross Worth')
            submit = st.form_submit_button(label='Extract Fields',type='primary')
        if submit:
            col2.subheader('Extracted Details')
            col2.markdown('-----------')
            if checkbox_invoice:
                user_question = 'What is the Invoice Number?'
                answer = generate_result(user_question,image)
                col2.text_input('Invoice Number',value=answer)
                extracted_data['Invoice Number'] = answer
                
            if checkbox_date_of_issue:
                user_question = 'What is the date of issue?'
                answer = generate_result(user_question, image)
                col2.text_input('Date of Issue',value=answer)
                extracted_data['Date of Issue'] = answer
                
            if checkbox_iban_code:
                user_question = 'What is the IBAN:?'
                answer = generate_result(user_question, image)
                col2.text_input('IBAN',value=str.upper(answer))
                extracted_data['IBAN'] = str.upper(answer)
                
            if checkbox_net_worth:
                user_question = 'What is the Total Net worth?'
                answer = generate_result(user_question, image)
                col2.text_input('Net Worth',value=answer)
                extracted_data['Net Worth'] = answer
                
            if checkbox_gross_worth:
                user_question = 'What is the Total Gross worth?'
                answer = generate_result(user_question, image)
                col2.text_input('Gross Worth',value=answer)
                extracted_data['Gross Worth'] = answer    
                    
            # After the form submission, you can convert the extracted_data dictionary to JSON
            if extracted_data:
                extracted_data_json = json.dumps(extracted_data, indent=4)
                st.write("Extracted Data (JSON format):")
                st.code(extracted_data_json)
            
                # Save the JSON data to a file
            with open('extracted_data/extracted_data.json', 'w') as json_file:
                json.dump(extracted_data, json_file, indent=4)

            st.success("Extracted data saved to 'extracted_data.json'")
            
else:
    st.warning('Upload Image')   



            


        
    

        