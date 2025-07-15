import streamlit as st
from utils.get_embeddings import get_embeddings
from utils.get_chunks import get_chunks
from utils.handle_db import get_chroma_collection
from utils.sanitize_collection_name import sanitize_collection_name

def handle_file_upload(uploaded_file):
    """
    Process uploaded file and store it in ChromaDB.
    
    Args:
        uploaded_file (dict): Document dictionary containing file info and content
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Extract information from the document dictionary
        collection_name = sanitize_collection_name(uploaded_file['name'])
        content = uploaded_file['content']
        
        # Check if content is valid
        if not content or content.startswith("Error") or content == "No text content found in PDF":
            st.warning(f"Skipping {collection_name} - no valid content to process")
            return False
        
        # Process the content into chunks
        knowledge_chunks = get_chunks(content, chunk_size=50)

        # Get ChromaDB collection (remove file extension from collection name)
        collection = get_chroma_collection(collection_name=collection_name)
        if not collection:
            return False

        # Process chunks and add to ChromaDB
        successful_chunks = 0
        for i, chunk in enumerate(knowledge_chunks):
            embedding = get_embeddings(chunk)
            if embedding:  # Only add if embedding was successful
                collection.add(
                    ids=[f"chunk-{i+1}"],
                    documents=[chunk],    
                    embeddings=[embedding]
                )
                successful_chunks += 1
        
        print(f"Processed {successful_chunks}/{len(knowledge_chunks)} chunks for ChromaDB")
        return successful_chunks > 0
        
    except Exception as e:
        st.error(f"Error processing documents for ChromaDB: {str(e)}")
        return False
