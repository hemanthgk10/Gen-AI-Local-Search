import PyPDF2
import docx
import pptx
import os

class DocumentPreprocessor:
    @staticmethod
    def extract_text_from_pdf(file_path):
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            return " ".join([page.extract_text() for page in reader.pages])

    @staticmethod
    def extract_text_from_docx(file_path):
        doc = docx.Document(file_path)
        return " ".join([para.text for para in doc.paragraphs])

    @staticmethod
    def extract_text_from_pptx(file_path):
        ppt = pptx.Presentation(file_path)
        return " ".join([shape.text for slide in ppt.slides for shape in slide.shapes if shape.has_text_frame])

    @staticmethod
    def preprocess_directory(directory_path):
        text_data = []
        for root, _, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                if file.endswith(".pdf"):
                    text_data.append(DocumentPreprocessor.extract_text_from_pdf(file_path))
                elif file.endswith(".docx"):
                    text_data.append(DocumentPreprocessor.extract_text_from_docx(file_path))
                elif file.endswith(".pptx"):
                    text_data.append(DocumentPreprocessor.extract_text_from_pptx(file_path))
        return text_data
