def truncate_filename(filename, max_length=35):
    """
    Truncate long filenames for display.
    
    Args:
        filename (str): Original filename
        max_length (int): Maximum length to display
        
    Returns:
        str: Truncated filename
    """
    if len(filename) > max_length:
        return filename[:max_length-3] + "..."
    return filename
