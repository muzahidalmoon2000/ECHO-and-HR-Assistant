
import easyocr
import numpy as np
import fitz  # PyMuPDF
from PIL import Image
from io import BytesIO
import requests

reader = easyocr.Reader(['en'])  # Initialize once

# OCR for images using EasyOCR
def extract_text_from_image(image_url):
    try:
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content)).convert("RGB")
        img_np = np.array(img)  # Convert to NumPy array
        results = reader.readtext(img_np, detail=0)
        return "\n".join(results)
    except Exception as e:
        print(f"❌ EasyOCR failed: {e}")
        return ""

# Extract text from PDF using OCR (fallback for scanned documents)
def extract_text_from_scanned_pdf(pdf_url):
    try:
        response = requests.get(pdf_url)
        if response.status_code != 200 or "pdf" not in response.headers.get("Content-Type", "").lower():
            print(f"⚠️ Invalid scanned PDF response: {pdf_url}")
            return ""

        pdf_file = fitz.open(stream=response.content, filetype="pdf")
        text = ""
        for page_num in range(pdf_file.page_count):
            page = pdf_file.load_page(page_num)
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            img_bytes = BytesIO()
            img.save(img_bytes, format="PNG")
            img_bytes.seek(0)
            ocr_result = reader.readtext(img_bytes, detail=0)
            text += "\n".join(ocr_result) + "\n"
        return text.strip()
    except Exception as e:
        print(f"❌ EasyOCR PDF fallback failed: {e}")
        return ""

# Text extraction from PDFs (non-scanned)
def extract_text_from_pdf(pdf_url):
    try:
        response = requests.get(pdf_url)
        content_type = response.headers.get("Content-Type", "")
        if response.status_code != 200 or "pdf" not in content_type.lower():
            print(f"⚠️ Invalid PDF response from {pdf_url} — Content-Type: {content_type}")
            return ""

        pdf_file = fitz.open(stream=response.content, filetype="pdf")
        text = ""
        for page_num in range(pdf_file.page_count):
            page = pdf_file.load_page(page_num)
            text += page.get_text()
        return text.strip()
    except Exception as e:
        print(f"❌ PyMuPDF failed to open PDF: {e}")
        return ""
