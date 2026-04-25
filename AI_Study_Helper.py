import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
import os
import math
from gtts import gTTS
import tempfile

# ---------------------------
# PAGE SETUP
# ---------------------------

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
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.title("📚 AI Study Assistant")
st.subheader("Upload your notes, summarize, and interact using AI")

# ---------------------------
# SIDEBAR
# ---------------------------

st.sidebar.title("🚀 Features")

st.sidebar.markdown("""
- Performance Dashboard  
- AI Content Analysis  
- PDF Summary  
- Listen to Summary (Podcast)  
- Important Sentences  
- Chat with Notes  
- Voice Questions  
- Download Results  
""")

# ---------------------------
# CONFIGURE AI
# ---------------------------

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

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
    # PERFORMANCE DASHBOARD
    # ---------------------------

    st.write("---")
    st.header("📊 Performance Dashboard")

    word_count = len(text.split())

    reading_time = math.ceil(
        word_count / 200
    )

    file_size = round(
        uploaded_file.size / 1024,
        2
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "📄 Number of Pages",
        total_pages
    )

    col2.metric(
        "📝 Word Count",
        word_count
    )

    col3, col4 = st.columns(2)

    col3.metric(
        "⏱ Reading Time",
        f"{reading_time} minutes"
    )

    col4.metric(
        "💾 File Size",
        f"{file_size} KB"
    )

    # ---------------------------
    # AI CONTENT ANALYSIS
    # ---------------------------

    st.write("---")
    st.subheader("🧠 AI Content Analysis")

    if st.button(
        "Detect Key Topics & Difficulty"
    ):

        try:

            with st.spinner(
                "Analyzing content..."
            ):

                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                prompt = f"""
Analyze the following study material.

Return:

1. Key Topics
2. Difficulty Level

Content:
{text[:4000]}
"""

                response = model.generate_content(
                    prompt
                )

                st.success(
                    "Analysis Complete!"
                )

                st.write(
                    response.text
                )

        except Exception as e:

            st.error(
                "Error analyzing content"
            )

            st.write(str(e))

st.divider()

# ---------------------------
# GENERATE SUMMARY
# ---------------------------

if st.button(
    "✨ Generate Summary"
):

    if text.strip() == "":

        st.error(
            "No text found in PDF!"
        )

    else:

        try:

            with st.spinner(
                "Generating summary..."
            ):

                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                response = model.generate_content(
                    f"""
You are an expert teacher.

1. Identify the SUBJECT
2. Explain clearly
3. Use bullet points

Content:
{text[:3000]}
"""
                )

                summary = response.text

                st.success(
                    "Summary Generated!"
                )

                st.write(summary)

                # ---------------------------
                # AUDIO SUMMARY
                # ---------------------------

                st.subheader(
                    "🎧 Listen to Summary"
                )

                if st.button(
                    "Generate Audio"
                ):

                    with st.spinner(
                        "Creating podcast..."
                    ):

                        tts = gTTS(
                            text=summary,
                            lang="en"
                        )

                        temp_file = tempfile.NamedTemporaryFile(
                            delete=False,
                            suffix=".mp3"
                        )

                        tts.save(
                            temp_file.name
                        )

                        st.success(
                            "Audio Ready!"
                        )

                        st.audio(
                            temp_file.name
                        )

                        with open(
                            temp_file.name,
                            "rb"
                        ) as audio_file:

                            st.download_button(
                                label="Download Audio",
                                data=audio_file,
                                file_name="summary_audio.mp3",
                                mime="audio/mp3"
                            )

                # ---------------------------
                # DOWNLOAD SUMMARY
                # ---------------------------

                st.download_button(
                    label="📥 Download Summary",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain"
                )

        except Exception as e:

            st.error(
                "Error generating summary"
            )

            st.write(str(e))

st.divider()

# ---------------------------
# IMPORTANT SENTENCES
# ---------------------------

st.header(
    "⭐ Important Sentences"
)

if st.button(
    "Extract Important Points"
):

    if text.strip() == "":

        st.error(
            "Upload a PDF first"
        )

    else:

        try:

            with st.spinner(
                "Finding key points..."
            ):

                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                response = model.generate_content(
                    f"""
Extract the most important sentences.

Return 5–8 bullet points.

Content:
{text[:3000]}
"""
                )

                st.success(
                    "Important points extracted!"
                )

                st.write(
                    response.text
                )

        except Exception as e:

            st.error(
                "Error extracting points"
            )

            st.write(str(e))

st.divider()

# ---------------------------
# CHAT SECTION
# ---------------------------

st.header(
    "💬 Ask Questions From Your PDF"
)

question = st.text_input(
    "Type your question"
)

st.subheader(
    "🎤 Or ask using voice"
)

audio = st.audio_input(
    "Record your question"
)

if audio is not None:

    st.success(
        "Voice recorded!"
    )

    question = "Voice question received"

# ---------------------------
# ASK QUESTION
# ---------------------------

if st.button(
    "Ask Question"
):

    if text.strip() == "":

        st.error(
            "Upload a PDF first"
        )

    elif question.strip() == "":

        st.error(
            "Enter a question"
        )

    else:

        try:

            with st.spinner(
                "Thinking..."
            ):

                model = genai.GenerativeModel(
                    "gemini-2.5-flash"
                )

                prompt = f"""
Content:
{text[:4000]}

Question:
{question}
"""

                response = model.generate_content(
                    prompt
                )

                answer = response.text

                st.success(
                    "Answer Generated!"
                )

                st.write(answer)

                st.download_button(
                    label="📥 Download Answer",
                    data=answer,
                    file_name="answer.txt",
                    mime="text/plain"
                )

        except Exception as e:

            st.error(
                "Error generating answer"
            )

            st.write(str(e))

# ---------------------------
# FOOTER
# ---------------------------

st.markdown(
    """
<hr>
<center>
Built for Hackathon 🚀
</center>
""",
    unsafe_allow_html=True
)
