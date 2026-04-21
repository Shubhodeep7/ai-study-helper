import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import os

# Page setup
st.set_page_config(page_title="AI Study Helper", layout="centered")

st.title("📚 AI Study Helper")
st.subheader("Upload your PDF and interact with it using AI")

# Sidebar
st.sidebar.title("Options")
st.sidebar.write("Built for Hackathon 🚀")

# Configure AI
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# File upload
uploaded_file = st.file_uploader("Upload your PDF", type="pdf")

text = ""

# Extract text from PDF
if uploaded_file is not None:

    reader = PdfReader(uploaded_file)

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text

    st.success("PDF uploaded successfully!")

# ---------------------------
# SUMMARY FEATURE
# ---------------------------

if st.button("✨ Generate Summary"):

    if text.strip() == "":
        st.error("No text found in PDF!")

    else:
        try:
            with st.spinner("Generating summary..."):

                model = genai.GenerativeModel("gemini-2.5-flash")

                response = model.generate_content(
                    "Summarize this text in simple bullet points:\n"
                    + text[:3000]
                )

                summary = response.text

                st.write("### Summary")
                st.write(summary)

        except Exception as e:
            st.error("Error generating summary")
            st.write(str(e))

# ---------------------------
# CHAT WITH PDF FEATURE
# ---------------------------

st.write("---")

st.header("💬 Ask Questions From Your PDF")

question = st.text_input("Enter your question")

if st.button("Ask Question"):

    if text.strip() == "":
        st.error("Please upload a PDF first")

    elif question.strip() == "":
        st.error("Please enter a question")

    else:
        try:
            with st.spinner("Thinking..."):

                model = genai.GenerativeModel("gemini-2.5-flash")

                prompt = f"""
                Use the following PDF content to answer the question.

                PDF Content:
                {text[:4000]}

                Question:
                {question}

                Give a clear and simple answer.
                """

                response = model.generate_content(prompt)

                answer = response.text

                st.write("### Answer")
                st.write(answer)

        except Exception as e:
            st.error("Error generating answer")
            st.write(str(e))
            st.write(str(e))
