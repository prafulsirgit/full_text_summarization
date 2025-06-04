from PIL import Image
import pdfplumber
import pytesseract

def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = "".join(page.extract_text() or "" for page in pdf.pages)
    return text

def extract_text_from_image(file_path):
    image = Image.open(file_path)
    text = pytesseract.image_to_string(image)
    return text