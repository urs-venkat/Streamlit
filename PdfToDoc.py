import streamlit as st
from PyPDF2 import PdfReader
from docx import Document
import io
import os # <--- This import is necessary for os.path.splitext

def show():
    # Wrap the entire content in the glass-container for consistent styling
    st.markdown('<div class="glass-container">', unsafe_allow_html=True)

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

                # Iterate through pages and extract text
                for page_num, page in enumerate(pdf.pages):
                    text = page.extract_text()
                    if text: # Only add paragraph if text is extracted
                        doc.add_paragraph(text)
                    # Add a page break in the Word document for each PDF page
                    # This helps maintain some structure, but note that direct PDF layout
                    # conversion to DOCX is a complex problem and usually requires more advanced libraries.
                    if page_num < len(pdf.pages) - 1: # Don't add a page break after the last page
                        doc.add_page_break()

                word_io = io.BytesIO()
                doc.save(word_io)
                word_io.seek(0) # Rewind the buffer to the beginning

            st.subheader("2. Download Your Word Document")
            st.info(f"Your PDF with {len(pdf.pages)} pages has been converted successfully. Download it below:")

            st.download_button(
                label="📥 Download Word File",
                data=word_io,
                # Generates a file name like "my_document_converted.docx"
                file_name=f"{os.path.splitext(uploaded_file.name)[0]}_converted.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"An error occurred during conversion: {e}")
            st.warning("Please note: Complex PDFs (e.g., scanned documents, heavily formatted layouts) may not convert perfectly using this method as it primarily extracts text.")
    else:
        st.info("Please upload a PDF file to begin the conversion process.")

    st.markdown('</div>', unsafe_allow_html=True) # Close the glass-container div