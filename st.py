import streamlit as st
import requests
from main import extract_toc_and_parse
from full import process_chapter_content

st.set_page_config(page_title="Book to Course", layout="wide")
st.title("📚 Book / Slides Course Generator")

API_URL = "http://localhost:8000"  # FastAPI must run separately

mode_selector = st.sidebar.radio("Select Mode", ["Book", "Slides"])

if mode_selector == "Book":
    st.header("📘 Book Mode")
    uploaded_pdf = st.file_uploader("Upload Book PDF", type=["pdf"])
    if uploaded_pdf:
        with open("upload.pdf", "wb") as f:
            f.write(uploaded_pdf.getbuffer())
        uploaded_pdf = "upload.pdf"

    if uploaded_pdf:
        toc_start = st.number_input("Start of Contents Page (PDF Page Number)", min_value=1, step=1)
        toc_end = st.number_input("End of Contents Page (PDF Page Number)", min_value=toc_start, step=1)
        book_page_1_pdf_page = st.number_input("PDF Page Number that corresponds to 'Book Page 1'", min_value=1, step=1)

        if st.button("Extract Chapters"):
            with st.spinner("Extracting chapters..."):
                chapters = extract_toc_and_parse(uploaded_pdf, toc_start, toc_end)
                st.session_state.chapters = chapters
                st.success("Chapters Extracted!")

    if "chapters" in st.session_state:
        st.header("📑 Chapters")

        with st.expander("🔧 Set Preferences"):
            learning_mode = st.selectbox("Learning Mode", ["deep dive", "last minute exam"])
            previous_knowledge = st.text_input("Your Previous Knowledge")
            education_level = st.selectbox("Your Education Level", ["10th pass", "12th studying", "Graduate", "Postgraduate"])
            language = st.selectbox("Preferred Language", ["english", "hindi", "hinglish"])

        for idx, chapter in enumerate(st.session_state.chapters):
            with st.container():
                st.subheader(f"📖 {chapter[0]}")
                st.json(chapter[1], expanded=False)
                if st.button(f"Generate Course for Chapter {idx + 1}", key=f"gen_{idx}"):
                    process_chapter_content(
                        chapter_data=chapter,
                        pdf_page_for_book_page_1=book_page_1_pdf_page,
                        full_pdf_path=uploaded_pdf,
                        mode=learning_mode,
                        previous_knowledge=previous_knowledge,
                        education_level=education_level,
                        language=language
                    )

if mode_selector == "Slides":
    st.header("📽️ Slides Mode")
    st.info("Slides mode functionality will be added here.")

# Optionally: Fetch files and play audio
st.markdown("## 🔈 Listen to a Chapter")
if st.button("📂 Load Available Files"):
    resp = requests.get(f"{API_URL}/pdf-files")
    if resp.status_code == 200:
        files = resp.json().get("pdf_files", [])
        file_choice = st.selectbox("Choose a File", files)
        if st.button("🎤 Play Audio for Selected File"):
            audio_resp = requests.post(f"{API_URL}/start-teaching", json={"file_name": file_choice})
            if audio_resp.status_code == 200:
                with open("audio.mp3", "wb") as f:
                    f.write(audio_resp.content)
                st.audio("audio.mp3")
            else:
                st.error("Could not generate audio.")
