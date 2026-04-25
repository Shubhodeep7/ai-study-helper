import streamlit as st
from PyPDF2 import PdfReader
import google.generativeai as genai
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
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ---------------------------
# FILE UPLOAD
# ---------------------------
uploaded_file = st.file_uploader("📂 Upload your PDF", type="pdf")

text = ""

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
    # DASHBOARD
    # ---------------------------
    st.write("---")
    st.header("📊 Performance Dashboard")

    word_count = len(text.split())
    reading_time = math.ceil(word_count / 200)
    file_size = round(uploaded_file.size / 1024, 2)

    col1, col2 = st.columns(2)
    col1.metric("📄 Pages", total_pages)
    col2.metric("📝 Words", word_count)

    col3, col4 = st.columns(2)
    col3.metric("⏱ Reading Time", f"{reading_time} min")
    col4.metric("💾 Size", f"{file_size} KB")

    # ---------------------------
    # AI ANALYSIS
    # ---------------------------
    st.write("---")
    st.subheader("🧠 AI Content Analysis")

    if st.button("Detect Key Topics & Difficulty"):

        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(f"""
Analyze this study material:

1. Key Topics
2. Difficulty Level

Content:
{text[:4000]}
""")

        st.write(response.text)

# ---------------------------
# SUMMARY SECTION
# ---------------------------
st.divider()

if st.button("✨ Generate Summary"):

    if text.strip() == "":
        st.error("Upload a PDF first!")

    else:

        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(f"""
You are an expert teacher.

1. Identify subject
2. Explain clearly
3. Use bullet points

Content:
{text[:3000]}
""")

        st.session_state["summary"] = response.text

        st.success("Summary Generated!")
        st.write(st.session_state["summary"])

# ---------------------------
# AUDIO (FIXED - OUTSIDE BUTTON)
# ---------------------------
if "summary" in st.session_state:

    st.subheader("🎧 Listen to Summary")

    if st.button("Generate Audio"):

        with st.spinner("Creating podcast..."):

            tts = gTTS(st.session_state["summary"], lang="en")

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tts.save(temp_file.name)

            with open(temp_file.name, "rb") as f:
                audio_bytes = f.read()

            st.success("Audio Ready!")
            st.audio(audio_bytes, format="audio/mp3")

            st.download_button(
                label="📥 Download Audio",
                data=audio_bytes,
                file_name="summary_audio.mp3",
                mime="audio/mp3"
            )

# ---------------------------
# IMPORTANT POINTS
# ---------------------------
st.divider()
st.header("⭐ Important Sentences")

if st.button("Extract Important Points"):

    if text.strip() == "":
        st.error("Upload a PDF first")

    else:

        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(f"""
Extract 5–8 important bullet points:

{text[:3000]}
""")

        st.write(response.text)

# ---------------------------
# Q&A SECTION
# ---------------------------
st.divider()
st.header("💬 Ask Questions From PDF")

question = st.text_input("Type your question")

if st.button("Ask Question"):

    if text.strip() == "":
        st.error("Upload a PDF first")

    elif question.strip() == "":
        st.error("Enter a question")

    else:

        model = genai.GenerativeModel("gemini-2.5-flash")

        response = model.generate_content(f"""
Content:
{text[:4000]}

Question:
{question}
""")

        st.write(response.text)

# ---------------------------
# FOOTER
# ---------------------------
st.markdown("""
<hr>
<center>Built for Hackathon 🚀</center>
""", unsafe_allow_html=True)
