import pypdf
import sys

try:
    reader = pypdf.PdfReader("Sujet/projet_final_UCO.pdf")
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    print(text)
except Exception as e:
    print(f"Error reading PDF: {e}")
