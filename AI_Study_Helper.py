import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import os

# Page setup
st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚",
    layout="centered"
)

# ---------------------------
# UI STYLING
# ---------------------------

st.markdown("""
<style>
.stButton > button {
    background-color: #1f77b4;
    color: white;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 AI Study Assistant")
st.subheader("Upload your notes, summarize, and interact using AI")

# Sidebar
st.sidebar.title("🚀 Features")
st.sidebar.markdown("""
- PDF Summary  
- Chat with Notes  
- Important Sentences  
- Voice Questions  
- Download Results
""")

# Configure AI
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ---------------------------
# FILE UPLOAD
# ---------------------------

uploaded_file = st.file_uploader(
    "📂 Upload your PDF",
    type="pdf"
)

text = ""

# ---------------------------
# EXTRACT TEXT + PROGRESS BAR
# ---------------------------

if uploaded_file is not None:

    reader = PdfReader(uploaded_file)

    progress = st.progress(0)

    total_pages = len(reader.pages)

    for i, page in enumerate(reader.pages):

        page_text = page.extract_text()

        if page_text:
            text += page_text

        progress.progress((i + 1) / total_pages)

    st.success("✅ PDF uploaded successfully!")

    # ---------------------------
    # SHOW PDF DETAILS
    # ---------------------------

    word_count = len(text.split())

    st.info(f"""
📄 File Name: {uploaded_file.name}  
📑 Pages: {total_pages}  
📝 Words: {word_count}
""")

st.divider()

# ---------------------------
# GENERATE SUMMARY
# ---------------------------

if st.button("✨ Generate Summary"):

    if text.strip() == "":
        st.error("No text found in PDF!")

    else:
        try:
            with st.spinner("Generating summary..."):

                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                response = model.generate_content(
                    f"""
You are an expert teacher.

1. Identify the SUBJECT
2. Explain the content clearly
3. Use simple bullet points

Content:
{text[:3000]}
"""
                )

                summary = response.text

                st.success("Summary Generated!")

                st.write(summary)

                st.download_button(
                    label="📥 Download Summary",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain"
                )

        except Exception as e:

            st.error("Error generating summary")

            st.write(str(e))

st.divider()

# ---------------------------
# IMPORTANT SENTENCES
# ---------------------------

st.header("⭐ Important Sentences")

if st.button("Extract Important Points"):

    if text.strip() == "":
        st.error("Upload a PDF first")

    else:
        try:
            with st.spinner("Finding key points..."):

                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                response = model.generate_content(
                    f"""
Extract the most important sentences
from this text.

Return 5–8 key points only.

Content:
{text[:3000]}
"""
                )

                important_points = response.text

                st.success("Important points extracted!")

                st.write(important_points)

        except Exception as e:

            st.error("Error extracting points")

            st.write(str(e))

st.divider()

# ---------------------------
# CHAT SECTION
# ---------------------------

st.header("💬 Ask Questions From Your PDF")

question = st.text_input(
    "Type your question"
)

# ---------------------------
# VOICE INPUT
# ---------------------------

st.subheader("🎤 Or ask using voice")

audio = st.audio_input("Record your question")

if audio is not None:

    st.success("Voice recorded!")

    question = "Transcribed voice question"

    st.write("Using voice input...")

# ---------------------------
# ASK QUESTION
# ---------------------------

if st.button("Ask Question"):

    if text.strip() == "":
        st.error("Upload a PDF first")

    elif question.strip() == "":
        st.error("Enter a question")

    else:
        try:
            with st.spinner("Thinking..."):

                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                prompt = f"""
Use the following PDF content to answer.

Content:
{text[:4000]}

Question:
{question}

Give a clear answer.
"""

                response = model.generate_content(
                    prompt
                )

                answer = response.text

                st.success("Answer Generated!")

                st.write(answer)

                st.download_button(
                    label="📥 Download Answer",
                    data=answer,
                    file_name="answer.txt",
                    mime="text/plain"
                )

        except Exception as e:

            st.error("Error generating answer")

            st.write(str(e))

# ---------------------------
# FOOTER
# ---------------------------

st.markdown("""
<hr>
<center>
</center>
""", unsafe_allow_html=True)
