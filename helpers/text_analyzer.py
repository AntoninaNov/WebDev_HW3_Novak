# helpers/text_analyzer.py
import re

def analyze_text(file_content, search_string):
    """
    Analyzes the text file content and returns metadata.
    """
    text_length = len(file_content)
    alphanumeric_count = len(re.findall(r'\w', file_content))
    occurrences = file_content.lower().count(search_string.lower())

    # Construct and return the response data
    response_data = {
        'length': text_length,
        'alphanumeric_count': alphanumeric_count,
        'occurrences': occurrences
    }
    return response_data
