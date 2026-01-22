import os
import google.generativeai as genai
import streamlit as st
from pdfextractor import text_extractor
from Docx2text import doc_text_extract
from image2text import extract_text_image


# lets configure genai model
key = os.getenv("Google_API_Key1")
genai.configure(api_key=key)
model = genai.GenerativeModel('gemini-2.5-flash-lite',
                                  generation_config={'temperature':0.9})


# lets create the sidebar

st.sidebar.title(':red[UPLOAD YOUR NOTES:]')
st.sidebar.subheader(':blue[Only upload Images, PDFs and DOCX]')
user_file = st.sidebar.file_uploader('UPLOAD HERE:',type=['pdf','docx','png','jpeg','jpg','jfif'])

if user_file:
    st.sidebar.success('File Uploaded Successfully')
    if user_file.type == 'application/pdf':
        user_text = text_extractor(user_file)
    elif user_file.type in ['image/png','image/jpeg','image/jpg','image/jfif']:
        user_text = extract_text_image(user_file)
    elif user_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
        user_text = doc_text_extract(user_file)
    else:
        print('ERROR : Enter correct file type')

# Lets CReate the main page
st.title(':orange[MoM GENERATOR:-] :blue[AI ASSISTED MINUTES OF MEETING GENERATOR]')
st.subheader(':green[This Application creates a generalized minutes of meeting from the Handwritten Notes]')
st.write('''
Follow these steps :-
1. Upload the notes in PDF, DOCX or image Format in sidebar
2. Click "GENERATE" to generate the MoM.
''')

if st.button('GENERATE'):
    with st.spinner('Please Wait....'):
        prompt = f'''
        <Role> You are an expert in formatting and writing minutes of meeting with 30+ years of experience.
        <Goal> Create minutes of meetings from the notes user have provided
        <Context> The user has provided some rough notes as text. Here are the notes : {user_text}
        <Format> The output must follow the below format:
        *  Title : assume  A good Professional title for the minutes of meeting
        * Agenda :  Assume agenda of the meeting
        * Attendance : Name of the attendes (If name of the atendees is not there keep it blank or N/A)
        * Date and Place : Date and the place of the meeting (If not provided keep it online by default)
        * Body : The body should follow the following sequence of points
                 * Mention Key points discussed.
                 * highlight and decision that has been taken.
                 * Mention Actionable Items.
                 * Mention any deadline if discussed
                 * Mention next meeting date if discussed
                 * Add a 2-3 line of summary.
        <Instructions>
        * Use bullets points and highlight the important keywords by making it bold
        * Generate  the output in docx format
        * Dont use htlm command/codes.
        '''
        response = model.generate_content(prompt)
        st.write(response.text)

        st.download_button(label='DOWNLOAD',
                              data=response.text,
                              file_name='MoM generator.txt',
                              mime='text/plain',
                              on_click=lambda: st.toast("✅ Download started!")
                              )