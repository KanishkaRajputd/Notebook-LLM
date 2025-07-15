import streamlit as st
from openai import OpenAI
from utils.get_api_client import get_openai_client

def get_embeddings(text):
    """
    Create embeddings for given text using OpenAI API.
    
    Args:
        text (str): Text to create embeddings for
        
    Returns:
        list or None: Embedding vector or None if error
    """
    try:
        client = get_openai_client()
        response = client.embeddings.create(
            input=text,
            model="text-embedding-3-small"
        )
        return response.data[0].embedding
    except Exception as e:
        st.error(f"Error creating embeddings: {str(e)}")
        return None
