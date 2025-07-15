def get_chunks(text, chunk_size=20):
    """
    Split text into fixed-size word chunks.
    
    Args:
        text (str): The text to chunk
        chunk_size (int): Number of words per chunk
        
    Returns:
        list: List of text chunks
    """
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = ' '.join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks

