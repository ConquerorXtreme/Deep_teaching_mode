import streamlit as st
import os
from gtts import gTTS
from pydub import AudioSegment

from main import extract_toc_and_parse
from full import process_chapter_content

# Streamlit app setup
st.set_page_config(page_title="Book to Course", layout="wide")
st.title("📚 Book / Slides Course Generator")

mode_selector = st.sidebar.radio("Select Mode", ["Book", "Slides", "Teach Me"])

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

elif mode_selector == "Slides":
    st.header("📽️ Slides Mode")
    st.info("Slides mode functionality will be added here.")

elif mode_selector == "Teach Me":
    st.header("🗣️ Teach Me (Text-to-Speech from Topics)")

    base_output_path = "/home/aryan/deep-spark-mentor-ai/backend/output"
    try:
        all_chapters = sorted([
            ch for ch in os.listdir(base_output_path)
            if os.path.isdir(os.path.join(base_output_path, ch))
        ])
    except FileNotFoundError:
        st.error("Output folder not found.")
        st.stop()

    selected_chapter = st.selectbox("Choose Chapter", all_chapters)

    chapter_path = os.path.join(base_output_path, selected_chapter)
    try:
        topics = sorted([
            f for f in os.listdir(chapter_path)
            if f.endswith(".txt")
        ])
    except FileNotFoundError:
        st.error("Chapter folder not found.")
        st.stop()

    selected_topic = st.selectbox("Choose Topic", topics)

    if st.button("🔊 Generate and Play Audio"):
        file_path = os.path.join(chapter_path, selected_topic)
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                text_content = file.read()

            # Clean text
            text_content = text_content.replace("*", "").replace("`", " ").replace("/", " divide by ")

            # Convert to speech
            audio_path = "part.mp3"
            tts = gTTS(text_content, lang="en", slow=False)
            tts.save(audio_path)

            # Optional: adjust pitch/speed using pydub if needed
            audio = AudioSegment.from_file(audio_path)
            st.audio(audio_path, format="audio/mp3")
            st.success("Audio generated and ready to play!")

        except Exception as e:
            st.error(f"Error: {str(e)}")
