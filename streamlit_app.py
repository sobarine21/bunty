import streamlit as st
from PyPDF2 import PdfReader
import tempfile
import os
import zipfile
import io

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def main():
    st.title("PDF to Text Bulk Converter")
    st.write(
        "Upload one or more PDF files, convert them to text, and download all results as a zip archive."
    )

    # Bulk PDF upload
    uploaded_files = st.file_uploader(
        "Upload PDF files", type=["pdf"], accept_multiple_files=True
    )

    if uploaded_files:
        process_btn = st.button("Convert and Download Zip")
        if process_btn:
            text_files = []
            with tempfile.TemporaryDirectory() as tmpdir:
                for uploaded_file in uploaded_files:
                    # Save uploaded file to a temp file for PyPDF2
                    tmp_pdf_path = os.path.join(tmpdir, uploaded_file.name)
                    with open(tmp_pdf_path, "wb") as f:
                        f.write(uploaded_file.read())
                    # Extract text
                    with open(tmp_pdf_path, "rb") as f:
                        text = extract_text_from_pdf(f)
                    # Save as .txt
                    txt_filename = os.path.splitext(uploaded_file.name)[0] + ".txt"
                    txt_path = os.path.join(tmpdir, txt_filename)
                    with open(txt_path, "w", encoding="utf-8") as txt_file:
                        txt_file.write(text)
                    text_files.append((txt_filename, txt_path))

                # Create zip archive in memory
                zip_buffer = io.BytesIO()
                with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
                    for txt_filename, txt_path in text_files:
                        zf.write(txt_path, arcname=txt_filename)
                zip_buffer.seek(0)

                # Download button for zip
                st.success("Conversion complete!")
                st.download_button(
                    label="Download All as Zip",
                    data=zip_buffer,
                    file_name="pdfs_converted_to_text.zip",
                    mime="application/zip"
                )

if __name__ == "__main__":
    main()
