# SQLite3 compatibility for Streamlit Cloud
import sys

def setup_sqlite3_compatibility():
    """
    Set up SQLite3 compatibility for ChromaDB on Streamlit Cloud.
    This replaces the default sqlite3 module with pysqlite3-binary when available.
    """
    try:
        # Try to import pysqlite3-binary and replace sqlite3
        import pysqlite3
        sys.modules['sqlite3'] = pysqlite3
        print("✅ Using pysqlite3-binary for SQLite3 compatibility")
    except ImportError:
        print("ℹ️ Using system sqlite3 (pysqlite3-binary not available)")
        pass 