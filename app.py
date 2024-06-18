import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Google Generative AI
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)

# Define function to get Gemini response
def get_gemini_response(input_prompt, data, query):
    model = genai.GenerativeModel('gemini-pro')
    combined_input = f"{input_prompt}\n\nData:\n{data}\n\nQuestion: {query}"
    response = model.generate_content([combined_input])
    return response.text

# Define function to read file
def read_file(file):
    if file.name.endswith('.csv'):
        return pd.read_csv(file)
    elif file.name.endswith('.xls') or file.name.endswith('.xlsx'):
        return pd.read_excel(file)
    else:
        return None

# Streamlit app configuration
st.set_page_config(page_title="Chatbot for Excel/CSV")
st.header("Chatbot for Excel/CSV")

# User input and file upload
uploaded_file = st.file_uploader("Choose a file...", type=["csv", "xls", "xlsx"])
input_prompt = st.text_input("Input Prompt: ", key="input")

# Button to submit the query
submit = st.button("➤")

# Process the input and file upload
if submit and uploaded_file:
    # Read the uploaded file
    data = read_file(uploaded_file)
    if data is not None:
        data_str = data.to_csv(index=False)  # Convert DataFrame to CSV string
        query = input_prompt
        input_prompt = """
        You are an expert in understanding csv, excel, tabular data, statistics, mathematics and analysis.
        You will have to answer questions based on the data, give detailed answer only if it is mentioned else direct answer.
        """
        response = get_gemini_response(input_prompt, data_str, query)
        st.subheader("🤖 Response:")
        st.write(response)
    else:
        st.error("Unsupported file format.")
