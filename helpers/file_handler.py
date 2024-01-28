# helpers/file_handler.py
import os

def serve_image(image_path):
    """
    Serves an image file located at the given path.
    """
    if os.path.exists(image_path) and os.path.isfile(image_path):
        _, ext = os.path.splitext(image_path)
        # Determine the content type based on the file extension
        content_type = 'image/jpeg' if ext in ['.jpg', '.jpeg'] else 'image/png'
        with open(image_path, 'rb') as file:
            file_content = file.read()
        return file_content, content_type
    else:
        raise FileNotFoundError("Image not found")
