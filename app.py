
"""
Author : Deepesh Mhatre
Written : 1/9/22
"""

import streamlit as st
from PIL import Image
import pytesseract
from transformers import pipeline
from utils import generate_chunks


@st.cache(allow_output_mutation=True)
def load_summarizer():
    print("Loading the Model....")
    model = pipeline("summarization")
    return model


# load model
summarizer = load_summarizer()

task = st.sidebar.radio("What task you want to do ?",
                        ('Text Summarization', 'Text Extraction'), index=0)

# -------------------------------------------------------------------------

if task == "Text Summarization":

    st.markdown("<h1 align='center'> Text Summerization ✂📑📚 </h1>",
                unsafe_allow_html=True)
    st.markdown("<h6 align='center'> A Text Summarization tool that employs NLP to condense large texts and generates a summary. </h6>", unsafe_allow_html=True)

    # options
    max = st.sidebar.slider('Max Output Length (no. of words)', 50, 500, step=10,
                            value=150, help="The Length of Output Summary in terms of number of words.")
    min_output_length = 50
    chunk_size = st.sidebar.slider('Chunk Size (no. of words)', 100, 500, step=100, value=300,
                                   help="Chunk size when dividing the given text into parts. Lower this value when passing very large texts (Eg- 2000-4000 words)")

    # input text
    sentence = st.text_area(' ', height=230,
                            placeholder="Paste your book or article content here ...")

    col1, col2, col3 = st.columns(3)
    with col2:
        st.write("Total words : ", len(sentence.split()))
        button = st.button("SUMMARIZE")

    with st.spinner("Generating Summary...please wait"):
        if button and len(sentence.split()) > 50:
            print("Generating chunks...")
            chunks = generate_chunks(sentence, chunk_size)
            print("Summarizing Text now...")
            res = summarizer(chunks,
                             max_length=max,
                             min_length=min_output_length,
                             do_sample=True)
            print("Summarization completed...")
            text = ' '.join([summ['summary_text'] for summ in res])
            st.write(text)
            col1, col2, col3 = st.columns(3)
            with col2:
                st.write("Total words : ", len(text.split()))
        
        elif len(sentence.split()) < 50:
            st.warning("Input Text must contain atleast 50 words !")


# -------------------------------------------------------------------------

elif task == 'Text Extraction':

    st.markdown("<h1 align='center'> Text Extraction 📑🔍 </h1>",
                unsafe_allow_html=True)
    st.markdown("<h6 align='center'> Avoid manually typing texts from Images with Automatic Text Extraction. </h6>", unsafe_allow_html=True)
    mode = st.sidebar.radio("Do you have an Image to Upload ?",
                            ('Upload Local Image', 'Capture from Camera'), index=1)

    if mode == 'Upload Local Image':
        # Upload the Image
        content_image = st.file_uploader("Upload Image (PNG & JPG images only).",
                                         type=['png', 'jpg', 'jpeg'])
        if content_image is not None:
            with st.spinner("Extracting Text.."):
                # Extract text from image
                uploaded_image = Image.open(content_image)
                print("Extracting Text now...")
                path = "Tesseract-OCR/tesseract.exe"
                pytesseract.pytesseract.tesseract_cmd = path
                text = pytesseract.image_to_string(uploaded_image)

                if len(text.split()) > 0:
                    st.image(content_image)
                    st.markdown("<h5> Extracted Text : </h5>",
                                unsafe_allow_html=True)
                    st.write(text)
                else:
                    st.write(
                        "No Text was discovered inside the given Image ! Try another one.")

    elif mode == 'Capture from Camera':
        # Capture Image
        captured_image = st.camera_input("Take a picture of your text")
        if captured_image is not None:
            with st.spinner("Extracting Text.."):
                # Extract text from image
                uploaded_image = Image.open(captured_image)
                print("Extracting Text now...")
                path = "Tesseract-OCR/tesseract.exe"
                pytesseract.pytesseract.tesseract_cmd = path
                text = pytesseract.image_to_string(uploaded_image)
                if len(text.split()) > 0:
                    st.image(captured_image)
                    st.markdown("<h5> Extracted Text : </h5>",
                                unsafe_allow_html=True)
                    st.write(text)
                else:
                    st.write(
                        "No Text was discovered inside the given Image ! Try another one.")
                         
# hide the watermark
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)                        
                
          
                
                
                
                
                
