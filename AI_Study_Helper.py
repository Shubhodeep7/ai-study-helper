import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai

# Page setup
st.set_page_config(page_title="AI Study Helper", layout="centered")
st.title("📚 AI Study Helper")
st.subheader("Upload your PDF and get instant summary")

# Sidebar
st.sidebar.title("Options")
st.sidebar.write("Built for Hackathon 🚀")

# Configure AI
import os

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# File upload
uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

text = ""

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text

    st.success("PDF uploaded successfully!")

# Generate Summary Button
if st.button("✨ Generate Summary"):

    if text.strip() == "":
        st.error("No text found in PDF!")

    else:
        try:
            model = genai.GenerativeModel("gemini-2.5-flash")

            response = model.generate_content(
                "Summarize this text in simple points:\n" + text[:3000]
            )

            summary = response.text

            st.write("### Summary")
            st.write(summary)

        except Exception as e:
            st.error("Error generating summary")
            st.write(str(e))
