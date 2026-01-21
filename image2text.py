import google.generativeai as genai
import cv2
import numpy as np
from PIL import Image
import os

def extract_text_image(image_path):
    file_bytes = np.asarray(bytearray(image_path.read()), dtype=np.uint8)  # to convert image to array because cv2 read only array
    image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)  # to use cv2 code to read the image
    # lets Load and Process the image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # To convert BGR to RGB
    image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # To convert BGR to Grey
    _,image_bw = cv2.threshold(image_grey,150,255,cv2.THRESH_BINARY) # B&W conversion

    # The image that CV2 gives is in numpy array format, we need to convert it to image object
    final_image = Image.fromarray(image_bw) 

    # Configure genai Model
    key = os.getenv("Google_API_Key1")
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-2.5-flash-lite',
                                  generation_config={'temperature':0.5})

    # Lets write prompt for OCR
    prompt ='''
        <Role> YOu are an OCR(Optical Character Application)
        <Goal> Identify the characters in handwritten notes
        <Context> User has provided the image of the handwritten notes.
        <Instruction> 
        * Do not generate any new content.
        * You can complete a word which is not recognised based on the english dictionary with coorect grammer.
        * Output should be well formatted
        '''
    # Lets extrcat and return the text
    response = model.generate_content([prompt,final_image])
    output_text = response.text
    return output_text