import PyPDF2
import re

def process_pdf_content(uploaded_file):
    """
    Extract text content from uploaded PDF file with better formatting.
    
    Args:
        uploaded_file: Streamlit uploaded file object
        
    Returns:
        str: Extracted text content
    """
    content = ""
    
    if uploaded_file.type == "application/pdf":
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            for page_num, page in enumerate(pdf_reader.pages):
                try:
                    text = page.extract_text()
                    if text:
                        # Clean up the extracted text
                        cleaned_text = _clean_pdf_text(text)
                        content += cleaned_text + ""
                except Exception as e:
                    print(f"Error extracting text from page {page_num + 1}: {str(e)}")
                    continue
            
            if not content.strip():
                content = "No text content found in PDF"
            else:
                # Final cleanup
                content = _final_text_cleanup(content)
                
        except Exception as e:
            if "Odd-length string" in str(e):
                content = f"Error reading PDF: {str(e)}\n\nThis PDF contains formatting issues that prevent proper text extraction. Please try converting the PDF to a different format or use a different PDF reader."
            else:
                content = f"Error reading PDF: {str(e)}"
    else:
        content = "Invalid file type - only PDF files are supported"
    
    return content


def _clean_pdf_text(text):
    """Clean and format text extracted from PDF."""
    if not text:
        return ""
    
    # Remove extra whitespace and normalize line breaks
    text = re.sub(r'\s+', ' ', text)
    
    # Fix common PDF extraction issues
    text = text.replace('\n\n', '')
    
    # Remove multiple spaces
    text = re.sub(r' +', ' ', text)
    
    # Try to recreate paragraphs by looking for sentence endings
    text = re.sub(r'(\w+[.!?])\s+([A-Z])', r'\1\n\n\2', text)
    
    # Fix numbered lists
    text = re.sub(r'(\d+\.\s+)', r'\n\1', text)
    
    return text.strip()


def _final_text_cleanup(content):
    """Final cleanup of the entire document content."""
    # Remove excessive blank lines
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Ensure proper spacing around numbered items
    content = re.sub(r'\n(\d+\.)', r'\n\n\1', content)
    
    # Clean up any remaining multiple spaces (but preserve single spaces)
    content = re.sub(r' +', ' ', content)
    
    return content.strip()
