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
# CUSTOM UI STYLING
# ---------------------------

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

h1 {
    text-align: center;
    color: #1f77b4;
}

.stButton > button {
    background-color: #1f77b4;
    color: white;
    border-radius: 10px;
    padding: 10px 20px;
    font-size: 16px;
}

.stTextInput > div > div > input {
    border-radius: 10px;
}

.block-container {
    padding-top: 2rem;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------

st.markdown("""
<h1>📚 AI Study Assistant</h1>
<p style='text-align:center; font-size:18px;'>
Upload your notes, summarize instantly, and ask questions using AI
</p>
""", unsafe_allow_html=True)

# ---------------------------
# SIDEBAR
# ---------------------------

st.sidebar.title("🚀 AI Study Helper")

st.sidebar.markdown("""
### Features

- 📄 PDF Summary  
- 💬 Chat With Notes  
- 📥 Download Results  
- 🧠 Study Smarter
""")

st.sidebar.success("Hackathon Ready")

# Configure AI
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ---------------------------
# FILE UPLOAD
# ---------------------------

col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader(
        "📂 Upload your PDF",
        type="pdf"
    )

with col2:
    st.info("Supported format:\nPDF")

text = ""

# Extract text
if uploaded_file is not None:

    reader = PdfReader(uploaded_file)

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text

    st.success("✅ PDF uploaded successfully!")

st.divider()

# ---------------------------
# SUMMARY SECTION
# ---------------------------

st.markdown("## ✨ Generate Summary")

if st.button("Generate Summary"):

    if text.strip() == "":
        st.error("No text found in PDF!")

    else:
        try:
            with st.spinner("Analyzing document..."):

                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                prompt = f"""
                You are an expert teacher.

                From the following PDF content:

                1. Identify the SUBJECT of the document in one line.
                2. Explain the content in simple language.
                3. Focus on understanding, not definitions.
                4. Give practical explanation and key ideas.
                5. Use bullet points.

                Format exactly like this:

                Subject:
                <subject name>

                Explanation Summary:
                - point
                - point
                - point

                Content:
                {text[:3000]}
                """

                response = model.generate_content(prompt)

                result = response.text

                st.success("Analysis Complete!")

                st.write(result)

                # DOWNLOAD BUTTON

                st.download_button(
                    label="📥 Download Summary",
                    data=result,
                    file_name="summary.txt",
                    mime="text/plain"
                )

        except Exception as e:

            st.error("Error generating summary")

            st.write(str(e))

st.divider()

# ---------------------------
# CHAT SECTION
# ---------------------------

st.markdown("## 💬 Chat With Your PDF")

question = st.text_input(
    "Ask a question from your notes"
)

if st.button("Ask Question"):

    if text.strip() == "":
        st.error("Please upload a PDF first")

    elif question.strip() == "":
        st.error("Please enter a question")

    else:
        try:
            with st.spinner("Thinking..."):

                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                prompt = f"""
                Use the following PDF content to answer the question.

                PDF Content:
                {text[:4000]}

                Question:
                {question}

                Give a clear and simple answer.
                """

                response = model.generate_content(
                    prompt
                )

                answer = response.text

                st.success("Answer Generated!")

                st.write(answer)

                # DOWNLOAD ANSWER BUTTON

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
Built with ❤️ using Python, Streamlit, and AI
</center>
""", unsafe_allow_html=True)
