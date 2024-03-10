import streamlit as st 
import google.generativeai as genai
from PIL import Image
from dotenv import load_dotenv
import os 

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_repsonse(input,image,prompt):
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
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")
    
##initialize our streamlit app

st.set_page_config(page_title="Financial Chart Detective App")

st.header("Financial Chart Detective App")

# Text input for user prompt
input_text = st.text_input("Input Prompt (Optional):", key="input")

# File uploader for image
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Display the uploaded image
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


submit=st.button("Analyze the image")

input_prompt="""
        you are expert in predicting the future trends and patterns in the stock market,cryptocurrency, and financial markets. 
        Please analyze the given stock,crytocurrency or financial markets chart image and predict the future trends and patterns in the stock market,cryptocurrency, and financial markets.

        
        Trend Analysis:
        Identify the current trend in the chart and provide any additional insights that can be derived from visual analysis.

        Support and Resistance Levels:
        Identify the support and resistance levels in the chart.

        Volume Analysis:
        Identify the volume of the stock and provide any additional insights that can be derived from visual analysis.

        Technical Indicators:
        Identify the technical indicators in the chart and provide any additional insights that can be derived from visual analysis.

        Chart Patterns:
        Identify the chart patterns in the chart and provide any additional insights that can be derived from visual analysis.

        Timeframes:
        Identify the timeframes in the chart and provide any additional insights that can be derived from visual analysis.

        Risk Management:
        Identify the risk management in the chart and provide any additional insights that can be derived from visual analysis.

        Trend Analysis:
        [Trend Analysis]

        Support and Resistance Levels:
        [Support and Resistance Levels]

        Volume Analysis:
        [Volume Analysis]

        Technical Indicators:
        [Technical Indicators]

        Chart Patterns:
        [Chart Patterns]

        Timeframes:
        [Timeframes]

        Risk Management:
        [Risk Management]

        Analyze the chart in the upper given format.if the given image is not related to stock market,cryptocurrency or financial markets, say "The given image is not related to stock market, cryptocurrency or financial markets."


"""

## If submit button is clicked
if submit:
    if uploaded_file is None:
        st.error("Please upload an image.")
    else:
        # Perform analysis here
        with st.spinner('Performing analysis...'):
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_repsonse(input_prompt, image_data, input_text)
        st.subheader("The Response is")
        st.write(response)
