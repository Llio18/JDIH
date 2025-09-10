import os
from pdf2image import convert_from_path
import pytesseract
import PyPDF2

def extract_text_smart_hybrid(pdf_path):
    """
    Mengekstrak teks pada halaman pdf dengan Ocr jika PyPDF2 gagal mengambil teks.
    """
    if not os.path.exists(pdf_path):
        print(f"Error: File tidak ditemukan di path '{pdf_path}'")
        return ""

    print(f"Memulai ekstraksi cerdas dari: {pdf_path}")
    
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_path)
        total_pages = len(pdf_reader.pages)
        images = convert_from_path(pdf_path)
        
        final_text_per_page = []

        for page_num in range(total_pages):
            page = pdf_reader.pages[page_num]
            text_from_pypdf2 = page.extract_text()

            if text_from_pypdf2 and len(text_from_pypdf2.strip()) > 50:
                final_text_per_page.append(text_from_pypdf2)
                print(f"✅ Halaman {page_num + 1}: Sukses dengan PyPDF2.")
            else:
                print(f"⚠️ Halaman {page_num + 1}: PyPDF2 gagal, menjalankan OCR...")
                page_text_ocr = pytesseract.image_to_string(images[page_num], lang='ind+eng')
                final_text_per_page.append(page_text_ocr)

        return "\n\n--- Halaman Berikutnya ---\n\n".join(final_text_per_page)

    except Exception as e:
        print(f"Terjadi error saat pemrosesan: {e}")
        return ""