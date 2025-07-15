# Setup SQLite3 compatibility for Streamlit Cloud deployment
from utils.db_compatibility import setup_sqlite3_compatibility
setup_sqlite3_compatibility()

import streamlit as st
import chromadb
from chromadb.config import Settings
import os


def clear_chroma_db(collection_name=None):
    """
    Clear all documents from ChromaDB collection(s).
    
    Args:
        collection_name (str, optional): Name of specific collection to clear.
                                       If None, clears all collections.
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        persist_directory = "./chrome_store"
        
        # Try to create the directory if it doesn't exist
        try:
            os.makedirs(persist_directory, exist_ok=True)
        except:
            pass
        
        # Use more compatible ChromaDB configuration
        try:
            chroma_client = chromadb.PersistentClient(path=persist_directory)
        except Exception as e:
            # Fallback to in-memory client if persistent storage fails
            print(f"Warning: Persistent storage failed, using in-memory client: {e}")
            chroma_client = chromadb.Client()
        
        if collection_name:
            # Clear specific collection
            try:
                collection = chroma_client.get_collection(name=collection_name)
                all_items = collection.get()
                if all_items['ids']:
                    collection.delete(ids=all_items['ids'])
                    print(f"🗑️ Cleared ChromaDB collection '{collection_name}'")
                else:
                    print(f"📭 ChromaDB collection '{collection_name}' was already empty")
                return True
            except Exception as e:
                print(f"Collection '{collection_name}' not found or already cleared")
                return True
        else:
            # Clear all collections
            try:
                collections = chroma_client.list_collections()
                if collections:
                    for collection in collections:
                        chroma_client.delete_collection(name=collection.name)
                        print(f"🗑️ Deleted ChromaDB collection '{collection.name}'")
                else:
                    print("📭 No ChromaDB collections found")
                return True
            except Exception as e:
                print(f"Error clearing all collections: {str(e)}")
                return False
        
    except Exception as e:
        st.error(f"Error clearing ChromaDB: {str(e)}")
        return False


def get_chroma_collection(collection_name, persist_directory="./chrome_store"):
    """
    Get or create a ChromaDB collection.
    
    Args:
        collection_name (str): Name of the collection
        persist_directory (str): Directory to persist ChromaDB data
        
    Returns:
        Collection or None: ChromaDB collection or None if error
    """
    print(f"Collection name: {collection_name}")
    try:
        # Try to create the directory if it doesn't exist
        try:
            os.makedirs(persist_directory, exist_ok=True)
        except:
            pass
        
        # Use more compatible ChromaDB configuration
        try:
            chroma_client = chromadb.PersistentClient(path=persist_directory)
        except Exception as e:
            # Fallback to in-memory client if persistent storage fails
            print(f"Warning: Persistent storage failed, using in-memory client: {e}")
            chroma_client = chromadb.Client()
        
        collection = chroma_client.get_or_create_collection(name=collection_name)
        return collection
    except Exception as e:
        st.error(f"Error accessing ChromaDB collection: {str(e)}")
        return None
