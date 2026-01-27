from pdfminer.high_level import extract_text
import io

def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extracts text explicitly from a PDF file using pdfminer.six.
    This simulates 'pdftotext -layout' behavior.
    """
    try:
        # Create a BytesIO object from the file content
        file_stream = io.BytesIO(file_bytes)
        
        # Extract text
        text = extract_text(file_stream)
        return text
    except Exception as e:
        raise Exception(f"PDF Text Extraction failed: {str(e)}")
