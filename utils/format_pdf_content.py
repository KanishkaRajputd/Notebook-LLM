def format_pdf_content(raw_content):
    """
    Format raw PDF content for better display.
    
    Args:
        raw_content (str): Raw text content from PDF
        
    Returns:
        str: Formatted text content
    """
    if not raw_content or raw_content.startswith("Error"):
        return raw_content
    
    # Clean up the text
    lines = raw_content.split('\n')
    formatted_lines = []
    
    for line in lines:
        # Remove extra whitespace
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Add the line to formatted content
        formatted_lines.append(line)
    
    # Join lines with proper spacing
    formatted_content = '\n'.join(formatted_lines)
    
    # Clean up multiple consecutive newlines
    while '\n\n\n' in formatted_content:
        formatted_content = formatted_content.replace('\n\n\n', '\n\n')
    
    return formatted_content


def get_content_preview(content, max_lines=50):
    """
    Get a preview of the content with limited lines.
    
    Args:
        content (str): Full content
        max_lines (int): Maximum number of lines to show
        
    Returns:
        str: Preview content
    """
    if not content:
        return ""
    
    lines = content.split('\n')
    if len(lines) <= max_lines:
        return content
    
    preview_lines = lines[:max_lines]
    preview = '\n'.join(preview_lines)
    preview += f"\n\n... (showing first {max_lines} lines of {len(lines)} total lines)"
    
    return preview 