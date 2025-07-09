import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import io

def show():
    st.title("PDF to Word Converter")
    st.write("Upload your PDF here:")
    uploaded_file = st.file_uploader(" ", type=["pdf"])

    if uploaded_file is not None:
        pdf = PdfReader(uploaded_file)
        st.write("PDF successfully uploaded!")

        st.write(f"Number of pages: {len(pdf.pages)}")

        doc = Document()

        for page_num in range(len(pdf.pages)):
            page = pdf.pages[page_num]
            text = page.extract_text()
            doc.add_paragraph(text)

        word_io = io.BytesIO()
        doc.save(word_io)
        word_io.seek(0)

        st.download_button(
            label="Download Word File",
            data=word_io,
            file_name="converted.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
