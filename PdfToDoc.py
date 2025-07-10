import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import io

def show():
    st.markdown("<h1 style='text-align: center;'>📄 PDF to DOC Converter</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Easily convert your PDF files into editable Word documents.</p>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.subheader("1. Upload Your PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"], label_visibility="collapsed")

    if uploaded_file is not None:
        st.success(f"✅ Successfully uploaded `{uploaded_file.name}`.")
        
        try:
            with st.spinner("⏳ Processing PDF..."):
                pdf = PdfReader(uploaded_file)
                doc = Document()
                
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text:
                        doc.add_paragraph(text)
                    doc.add_page_break()

                word_io = io.BytesIO()
                doc.save(word_io)
                word_io.seek(0)

            st.subheader("2. Download Your Word Document")
            st.info(f"Your PDF with {len(pdf.pages)} pages has been converted successfully.")
            
            st.download_button(
                label="📥 Download Word File",
                data=word_io,
                file_name=f"{os.path.splitext(uploaded_file.name)[0]}_converted.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"An error occurred during conversion: {e}")
    else:
        st.info("Please upload a PDF file to begin the conversion process.")
