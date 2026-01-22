from pdf2image import convert_from_bytes
from PIL import Image
import io

def process_file(file_bytes: bytes, content_type: str) -> Image.Image:
    """
    Converts input bytes to a PIL Image. 
    If PDF, converts the first page to an image.
    """
    try:
        if "pdf" in content_type:
            # Convert PDF to list of images, take the first one
            images = convert_from_bytes(file_bytes)
            if not images:
                raise ValueError("PDF is empty")
            return images[0]
            
        elif "image" in content_type:
            # Standard image handling
            return Image.open(io.BytesIO(file_bytes))
        
        else:
            raise ValueError("Invalid file type. Upload PDF, JPG, or PNG.")
            
    except Exception as e:
        raise ValueError(f"File processing error: {str(e)}")