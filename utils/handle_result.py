import streamlit as st
from utils.get_embeddings import get_embeddings
from utils.handle_db import get_chroma_collection
from utils.get_api_client import get_openai_client
from utils.sanitize_collection_name import sanitize_collection_name


def handle_result(question, selected_doc_indices, uploaded_documents, n_results=2):
    """
    Query the knowledge base with a question and get AI response.
    
    Args:
        question (str): The question to ask
        selected_doc_indices (list): List of selected document indices
        uploaded_documents (list): List of uploaded documents
        n_results (int): Number of results to retrieve
        
    Returns:
        str or None: AI response or None if error
    """
    try:
        print(question, 'question', selected_doc_indices, 'selected_doc_indices', uploaded_documents, 'uploaded_documents')
        # Get embeddings for the question
        query_embedding = get_embeddings(question)
        if not query_embedding:
            return None
            
        # Get ChromaDB collection and query results
        all_documents = []
        
        for index in selected_doc_indices:  
            collection_name = sanitize_collection_name(uploaded_documents[index]['name'])
            collection = get_chroma_collection(collection_name)
            
            if not collection:
                continue
                
            # Query the collection
            collection_results = collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            # Add the documents from this collection to our results
            if collection_results and 'documents' in collection_results:
                for doc_list in collection_results['documents']:
                    all_documents.extend(doc_list)
        
        # Get OpenAI client
        print(all_documents, 'all_documents')
        client = get_openai_client()
        if not client or not all_documents:
            return None
            
        # Combine all documents into context
        context = "\n\n".join(all_documents)  # Limit to top 10 most relevant chunks
            
        # Generate response using retrieved context
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{
                "role": "user",
                "content": f"You are a helpful and high level document assistant. Given the following context from documents: {context} and the question: {question}, provide a comprehensive and helpful answer. Keep a human touch in your response."
            }]
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        st.error(f"Error querying knowledge base: {str(e)}")
        return None
