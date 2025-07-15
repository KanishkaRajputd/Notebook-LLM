import streamlit as st
from openai import OpenAI

def get_openai_client():
    """
    Get OpenAI client with API key from secrets.
    
    Returns:
        OpenAI: OpenAI client instance
    """
    try:
        api_key = st.secrets["OpenAI_KEY"]
        return OpenAI(api_key=api_key)
    except Exception as e:
        st.error(f"Error initializing OpenAI client: {str(e)}")
        return None