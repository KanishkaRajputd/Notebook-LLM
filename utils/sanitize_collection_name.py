import re
import hashlib

def sanitize_collection_name(filename):
    """
    Sanitize filename to create a valid ChromaDB collection name.
    
    ChromaDB collection names must:
    - Be 3-512 characters long
    - Contain only [a-zA-Z0-9._-]
    - Start and end with [a-zA-Z0-9]
    
    Args:
        filename (str): Original filename
        
    Returns:
        str: Sanitized collection name
    """
    # Remove file extension
    name_without_ext = filename.rsplit('.', 1)[0] if '.' in filename else filename
    
    # Replace spaces and invalid characters with underscores
    sanitized = re.sub(r'[^a-zA-Z0-9._-]', '_', name_without_ext)
    
    # Remove consecutive underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    
    # Remove leading/trailing underscores and dots/hyphens
    sanitized = re.sub(r'^[._-]+|[._-]+$', '', sanitized)
    
    # Ensure it starts and ends with alphanumeric
    if sanitized and not sanitized[0].isalnum():
        sanitized = 'doc_' + sanitized
    if sanitized and not sanitized[-1].isalnum():
        sanitized = sanitized + '_doc'
    
    # If empty or too short, create a hash-based name
    if not sanitized or len(sanitized) < 3:
        hash_suffix = hashlib.md5(filename.encode()).hexdigest()[:8]
        sanitized = f"doc_{hash_suffix}"
    
    # Ensure it's not too long (max 512 chars)
    if len(sanitized) > 512:
        hash_suffix = hashlib.md5(filename.encode()).hexdigest()[:8]
        sanitized = sanitized[:500] + '_' + hash_suffix
    
    return sanitized 