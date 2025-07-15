# Setup SQLite3 compatibility for Streamlit Cloud deployment
from utils.db_compatibility import setup_sqlite3_compatibility
setup_sqlite3_compatibility()

import streamlit as st
import PyPDF2
import io
import os
import time
import chromadb
from chromadb.config import Settings
from openai import OpenAI

# Import custom functions
from utils.handle_file_upload import handle_file_upload
from utils.handle_result import handle_result
from utils.formate_file_size import format_file_size
from utils.truncate_filename import truncate_filename
from utils.handle_db import clear_chroma_db
from utils.process_pdf_content import process_pdf_content
from utils.sanitize_collection_name import sanitize_collection_name

# PDF-only document analyzer - no image support

# ---------------------------
# Streamlit Page Config
# ---------------------------
st.set_page_config(
    page_title="Notebook AI - Document Analyzer", 
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------
# Custom CSS for Layout and Styling
# ---------------------------
st.markdown("""
<style>
    /* Sidebar width adjustment */
    .css-1d391kg {
        width: 33.33% !important;
        min-width: 400px !important;
    }
    
    /* Main content area */
    .css-18e3th9 {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
    
    /* Sources panel styling */
    .sources-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        padding: 0.5rem 0;
        border-bottom: 1px solid #333;
    }
    
    .sources-title {
        font-size: 1.2rem;
        font-weight: 600;
        color: #fff;
    }
    
    .add-button, .discover-button {
        background: #262730;
        border: 1px solid #444;
        border-radius: 6px;
        padding: 0.5rem 1rem;
        color: #fff;
        cursor: pointer;
        font-size: 0.9rem;
        margin: 0 0.25rem;
    }
    
    .add-button:hover, .discover-button:hover {
        background: #333;
    }
    
    /* Document list styling */
    .document-item {
        display: flex;
        align-items: center;
        padding: 0.75rem;
        margin: 0.5rem 0;
        background: #1e1e1e;
        border-radius: 8px;
        border: 1px solid #333;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .document-item:hover {
        background: #252525;
        border-color: #555;
    }
    
    .document-item.selected {
        background: #2563eb;
        border-color: #3b82f6;
    }
    
    .document-item.selected:hover {
        background: #1d4ed8;
        border-color: #2563eb;
    }
    
    .document-icon {
        margin-right: 0.75rem;
        font-size: 1.2rem;
    }
    
    .document-info {
        flex: 1;
        min-width: 0;
    }
    
    .document-name {
        font-weight: 500;
        color: #fff;
        font-size: 0.9rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    
    .document-type {
        font-size: 0.8rem;
        color: #888;
        margin-top: 0.25rem;
    }
    
    .document-checkbox {
        margin-left: 0.5rem;
    }
    
    /* Select all section */
    .select-all-section {
        padding: 0.75rem;
        background: #262730;
        border-radius: 6px;
        margin: 1rem 0;
        border: 1px solid #333;
    }
    
    /* Preview card styling */
    .preview-card {
        background: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    /* File info badges */
    .file-info {
        display: inline-block;
        background: #e3f2fd;
        color: #1976d2;
        padding: 0.25rem 0.5rem;
        border-radius: 20px;
        font-size: 0.8rem;
        margin: 0.25rem 0;
    }
    
    /* PDF preview styling */
    .pdf-preview {
        background: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 6px;
        padding: 0.75rem;
        font-family: 'Courier New', monospace;
        font-size: 0.85rem;
        max-height: 200px;
        overflow-y: auto;
    }
    
    /* Image container styling */
    .image-container {
        border-radius: 8px;
        overflow: hidden;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    /* Image preview in cards */
    .preview-card img {
        border-radius: 6px;
        margin: 0.5rem 0;
    }
    
    /* PDF Content Text Area Styling for Dark Theme */
    .stTextArea > div > div > textarea {
        background-color: #1e1e1e !important;
        color: #ffffff !important;
        border: 1px solid #444 !important;
        border-radius: 8px !important;
        font-family: 'Courier New', monospace !important;
        font-size: 14px !important;
        line-height: 1.6 !important;
        padding: 15px !important;
    }
    
    /* Ensure text area is readable in dark theme */
    .stTextArea > div > div > textarea:disabled {
        background-color: #2d2d2d !important;
        color: #f0f0f0 !important;
        border: 1px solid #555 !important;
        opacity: 1 !important;
    }
    
    /* PDF content text area specific styling */
    div[data-testid="stTextArea"] textarea {
        background-color: #2d2d2d !important;
        color: #f0f0f0 !important;
        border: 1px solid #555 !important;
        border-radius: 8px !important;
    }
    
    /* Light theme fallback */
    @media (prefers-color-scheme: light) {
        .stTextArea > div > div > textarea {
            background-color: #ffffff !important;
            color: #000000 !important;
            border: 1px solid #ddd !important;
        }
        
        .stTextArea > div > div > textarea:disabled {
            background-color: #f8f9fa !important;
            color: #212529 !important;
            border: 1px solid #ddd !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for uploaded files (temporary storage - cleared on refresh)
if 'uploaded_documents' not in st.session_state:
    st.session_state.uploaded_documents = []  # Array to store uploaded files temporarily
if 'selected_doc_indices' not in st.session_state:
    st.session_state.selected_doc_indices = []  # Array to store indices of selected documents (max 2)
if 'session_id' not in st.session_state:
    st.session_state.session_id = int(time.time())

# ---------------------------
# Upload Dialog Function
# ---------------------------
@st.dialog("Upload Document")
def upload_dialog():    
    # File type info
    st.info("📄 PDF documents only - upload your PDF files for analysis")
    
    # Enhanced file uploader with proper drag and drop styling
    st.markdown("""
    <style>
        .stFileUploader > div > div > div > div {
            border: 2px dashed #555 !important;
            border-radius: 8px !important;
            padding: 2rem !important;
            text-align: center !important;
            background: #262730 !important;
            margin: 1rem 0 !important;
            min-height: 150px !important;
        }
        
        .stFileUploader > div > div > div > div:hover {
            border-color: #777 !important;
            background: #2a2b36 !important;
        }
        
        .stFileUploader > div > div > div > div > button {
            background: transparent !important;
            border: none !important;
            color: #ccc !important;
            font-size: 1rem !important;
        }
        
        .stFileUploader > div > div > div > div > button:before {
            content: "📄 Drag and drop PDF file here or click to browse" !important;
            display: block !important;
            font-size: 1.1rem !important;
            margin-bottom: 0.5rem !important;
        }
        
        .stFileUploader > div > div > div > div > small {
            color: #888 !important;
            font-size: 0.9rem !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # File uploader with drag and drop functionality
    uploaded_file = st.file_uploader(
        "Upload",
        type=["pdf"],
        accept_multiple_files=False,
        key="dialog_file_uploader",
        help="Drag your PDF file directly onto this area or click to browse your files"
    )
    
    # Process uploaded file
    if uploaded_file:
        # Check if file already exists
        if not any(doc['name'] == uploaded_file.name for doc in st.session_state.uploaded_documents):
            # Process PDF using utility function
            with st.spinner("Processing PDF..."):
                content = process_pdf_content(uploaded_file)
                
                if uploaded_file.type == "application/pdf":
                    if content and not content.startswith("Error") and content != "No text content found in PDF":
                        try:
                            pdf_reader = PyPDF2.PdfReader(uploaded_file)
                            word_count = len(content.split())
                            st.success(f"✅ PDF processed successfully - {len(pdf_reader.pages)} pages, {word_count} words")
                        except:
                            st.success("✅ PDF processed successfully")
                    elif content == "No text content found in PDF":
                        st.warning("⚠️ No text content found in PDF")
                    else:
                        st.error(f"❌ PDF processing failed: {content}")
                else:
                    st.error("❌ Only PDF files are supported")
            
            # Store document info in temporary array
            doc_info = {
                'name': uploaded_file.name,
                'type': uploaded_file.type,
                'size': uploaded_file.size,
                'content': content,
                'file_obj': uploaded_file,
                'upload_time': time.time()  # Track when uploaded
            }
            st.session_state.uploaded_documents.append(doc_info)  # Add to archived array
            
            # Auto-select new document (max 2 selections)
            new_doc_index = len(st.session_state.uploaded_documents) - 1

            if len(st.session_state.selected_doc_indices) < 2:
                st.session_state.selected_doc_indices.append(new_doc_index)
                with st.spinner("Processing PDF content..."):
                    handle_file_upload(st.session_state.uploaded_documents[new_doc_index])
            else:
                # Replace oldest selection with new document
                with st.spinner("Processing PDF content..."):
                    handle_file_upload(st.session_state.uploaded_documents[new_doc_index])

            st.success(f"✅ Added PDF document: {uploaded_file.name}")
            st.info("📁 Document stored in temporary archive (will be cleared on page refresh)")

        else:
            st.warning(f"File '{uploaded_file.name}' is already uploaded.")
    
    # Action buttons
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("Cancel", use_container_width=True):
            st.rerun()
    with col2:
        if st.button("Upload", type="primary", use_container_width=True, disabled=not uploaded_file):
            if uploaded_file:
                st.rerun()

# ---------------------------
# SIDEBAR - SOURCES PANEL
# ---------------------------
with st.sidebar:
    # Sources header with document count
    doc_count = len(st.session_state.uploaded_documents)
    selected_count = len(st.session_state.selected_doc_indices)
    selection_text = f" • {selected_count} selected" if selected_count > 0 else ""
    st.markdown(f"""
    <div class="sources-header">
        <span class="sources-title">Sources ({doc_count}{selection_text})</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Show temporary storage info if documents exist
    if doc_count > 0:
        st.caption("⏰ Files stored temporarily - cleared on refresh")
    
    # Add button - opens dialog
    if st.button("➕ Add", key="add_btn", use_container_width=True):
        upload_dialog()
    
    # Document list (multi-selection, max 2)
    if st.session_state.uploaded_documents:
        st.markdown("---")
        
        # Show selection info
        selected_count = len(st.session_state.selected_doc_indices)
        if selected_count > 0:
            st.caption(f"📋 {selected_count}/2 documents selected")
        else:
            st.caption("📋 Select up to 2 documents")
        
        for i, doc in enumerate(st.session_state.uploaded_documents):
            # PDF icon only
            icon = "📄"
            
            # Check if this document is selected
            is_selected = i in st.session_state.selected_doc_indices
            
            # Truncate long filenames
            display_name = truncate_filename(doc['name'])
            
            # Create clickable document item
            if st.button(
                f"{icon} {display_name}",
                key=f"doc_button_{i}",
                use_container_width=True,
                type="primary" if is_selected else "secondary"
            ):
                # Toggle selection with max 2 documents
                if i in st.session_state.selected_doc_indices:
                    # Deselect if already selected
                    st.session_state.selected_doc_indices.remove(i)
                    # Clear ChromaDB if no documents selected
                    if len(st.session_state.selected_doc_indices) == 0:
                        clear_chroma_db()
                        # Rebuild ChromaDB with remaining selected documents
                else:
                    # Select document (max 2)
                    if len(st.session_state.selected_doc_indices) < 2:
                        st.session_state.selected_doc_indices.append(i)
                    else:
                        # Replace oldest selection
                        st.session_state.selected_doc_indices.pop(0)
                        st.session_state.selected_doc_indices.append(i)
                        # Clear and rebuild ChromaDB with new selections
                st.rerun()
    
    # Clear All button at bottom of sidebar
    if st.session_state.uploaded_documents:
        st.markdown("---")  # Add separator
        if st.button("🗑️ Clear All", type="secondary", use_container_width=True):
            st.session_state.uploaded_documents = []  # Clear the archived array
            st.session_state.selected_doc_indices = []  # Reset selections
            clear_chroma_db()  # Clear ChromaDB when clearing all documents
            st.rerun()

# ---------------------------
# MAIN CONTENT AREA
# ---------------------------

# Main title
st.title("📚 Notebook AI")

# Show selected document info and array status
total_docs = len(st.session_state.uploaded_documents)
has_selection = len(st.session_state.selected_doc_indices) > 0
selected_count = len(st.session_state.selected_doc_indices)

# ---------------------------
# Side by Side Layout: Document Preview and Questions
# ---------------------------
if st.session_state.uploaded_documents and has_selection:
    # Create two columns for side-by-side layout
    preview_col, question_col = st.columns([1, 1])
    
    # Get selected documents
    selected_docs = [st.session_state.uploaded_documents[i] for i in st.session_state.selected_doc_indices]
    
    # Left Column - Document Preview
    with preview_col:
        st.header(f"👁️ PDF Preview ({selected_count} selected)")
        
        # Display each selected document
        for idx, selected_doc in enumerate(selected_docs):
            # Add separator between documents
            if idx > 0:
                st.markdown("---")
            
            # File metadata
            size_text = format_file_size(selected_doc['size'])
            
            # Document header            
            # PDF Preview
            try:
                pdf_reader = PyPDF2.PdfReader(selected_doc['file_obj'])
                page_count = len(pdf_reader.pages)
                
                st.markdown(f"""
                <div class="file-info">📄 PDF • {page_count} page(s) • {size_text}</div>
                """, unsafe_allow_html=True)
                
                if selected_doc['content'] and selected_doc['content'].strip() and not selected_doc['content'].startswith("Error"):
                    word_count = len(selected_doc['content'].split())
                    st.success(f"✅ Text extracted: {word_count} words")
                    
                    # Display content in a text area (smaller height for multiple docs)
                    content_height = 400 if selected_count == 1 else 200
                    st.text_area(
                        f"📖 Content Preview - Document {idx + 1}",
                        selected_doc['content'],
                        height=content_height,
                        key=f"pdf_content_preview_{idx}",
                        help="Full PDF text content",
                        disabled=True
                    )
                else:
                    st.warning("⚠️ No text content available in this PDF")
                    
            except Exception as e:
                st.error(f"❌ PDF preview error: {str(e)}")
    
    # Right Column - Questions Section
    with question_col:
        st.header("❓ Ask Questions")

        

             # Custom question input
        question = st.text_input(
            "Ask your own question:",
            placeholder="e.g., What is this document about?",
            key="custom_question"
        )

        # Quick question buttons  
        st.markdown("---")
        st.subheader("💡 Quick Questions")
        
        col1, col2, col3 = st.columns(3)
        
        # Initialize session state for button responses
        if 'button_response' not in st.session_state:
            st.session_state.button_response = None
        
        with col1:
            if st.button("📝 Summarize", use_container_width=True, key="summarize_btn"):
                with st.spinner("🤖 Getting AI response..."):
                    response = handle_result("Provide a brief summary of this document.", st.session_state.selected_doc_indices, st.session_state.uploaded_documents)
                    st.session_state.button_response = response if response else "⚠️ Unable to get AI response. Please check your API key and try again."
         
        
        with col2:
            if st.button("🔍 Key Points", use_container_width=True, key="keypoints_btn"):
                with st.spinner("🤖 Getting AI response..."):
                    response = handle_result("What are the main key points in this document?", st.session_state.selected_doc_indices, st.session_state.uploaded_documents)
                    st.session_state.button_response = response if response else "⚠️ Unable to get AI response. Please check your API key and try again."

        with col3:
            if st.button("📊 Details", use_container_width=True, key="details_btn"):
                with st.spinner("🤖 Getting AI response..."):
                    response = handle_result("What are the most important details I should know?", st.session_state.selected_doc_indices, st.session_state.uploaded_documents)
                    st.session_state.button_response = response if response else "⚠️ Unable to get AI response. Please check your API key and try again."
        
        # Display button response if available
        if st.session_state.button_response:
            st.markdown("### 🤖 AI Response:")
            st.write(st.session_state.button_response)
            
            # Clear response button
            if st.button("🗑️ Clear Response", type="secondary", key="clear_response_btn"):
                st.session_state.button_response = None
                st.rerun()
        
        # Show AI response if there's a question
        if question and question.strip():
            with st.spinner("🤖 Getting AI response..."):
                response_text = handle_result(question, st.session_state.selected_doc_indices, st.session_state.uploaded_documents)
                if response_text:
                    st.markdown("### 🤖 AI Response:")
                    st.write(response_text)
                else:
                    st.warning("⚠️ Unable to get AI response. Please check your API key and try again.")
        
    
elif st.session_state.uploaded_documents:
    st.info("👆 Please select up to 2 PDF documents from the sidebar to start asking questions")
else:
    st.info("👆 Click '➕ Add' in the sidebar to upload your first PDF document")

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")








