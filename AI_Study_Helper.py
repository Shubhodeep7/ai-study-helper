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

# Configure AI (DO THIS ONCE)
genai.configure(api_key="AIzaSyA5gGVZ8MGbhEcyVfVqeHc6HWHivorkq28")

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

# Button
if st.button("✨ Generate Summary"):
    if text.strip() == "":
        st.error("No text found in PDF!")
    else:
        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            "Summarize this text:\n" + text[:6000]
        )

        st.write("### Summary")
        st.write(response.text)
