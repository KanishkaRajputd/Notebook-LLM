
def format_file_size(size_bytes):
    """
    Format file size in bytes to human readable format.
    
    Args:
        size_bytes (int): File size in bytes
        
    Returns:
        str: Formatted file size string
    """
    file_size_mb = size_bytes / (1024 * 1024)
    if file_size_mb < 1:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{file_size_mb:.1f} MB"
