import pdfplumber
import docx

def extract_text_from_pdf(file_bytes):
    text = ""
    with pdfplumber.open(file_bytes) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
    return text

def extract_text_from_docx(file_bytes):
    doc = docx.Document(file_bytes)
    text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
    return text

def parse_cv_file(uploaded_file):

    if uploaded_file is None:
        return None
        
    filename = uploaded_file.name.lower()
    
    if filename.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    elif filename.endswith(".docx"):
        return extract_text_from_docx(uploaded_file)
    elif filename.endswith(".txt"):
        return uploaded_file.getvalue().decode("utf-8")
    else:
        return None