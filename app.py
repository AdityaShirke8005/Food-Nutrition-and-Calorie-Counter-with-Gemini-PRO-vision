from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

import streamlit as st
import os
import pathlib
import textwrap
from PIL import Image


import google.generativeai as genai


# Load API key
os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


# Load Gemini model and get response
def get_gemini_response(input,image,prompt):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input,image[0],prompt])
    return response.text
    

def input_image_setup(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type, 
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


# Initialize the streamlit app
st.set_page_config(page_title="Gemini Image Demo")
st.header("Food Nutrition and Calorie Counter")
st.markdown(
            "<p class='footer'>Created with ❤️ by Aditya Shirke</p>",
            unsafe_allow_html=True
        )
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""   
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit=st.button("Ask me 🙂")

input_prompt = """
               You are a Food Nutrition Expert.
               You will receive input images as meal platter or any sort consumables.
               You must analyze the uploaded meal image to identify various food items present. Extract nutritional information (protein, carbohydrates, fat, fiber, vitamins, minerals) for each item and calculate the total nutrition of the meal. Compute the estimated calorie count based on the provided portions.
               Return the response in following way : 1) Total Nutrition of Meal in tabular format only . 2) Total Estimated Calorie count in Kcal in a box. 3) Great Food Combinations from uploaded meal : [List of beneficial food combinations] 4) Harmful food Combinations from uploaded meal : [List of potentially harmful food combinations].
               """

if submit:
    image_data = input_image_setup(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("Nutritional Info : ")
    st.write(response)