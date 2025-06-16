import base64
from io import BytesIO
from pdf2image import convert_from_bytes
from PIL import Image

def convert_pdf_to_base64_images(pdf_content: bytes) -> list:
    """
    Convert PDF content to a list of base64 encoded images
    """
    try:
        # Convert PDF pages to images
        images = convert_from_bytes(pdf_content)
        base64_images = []
        
        # Convert each page to base64
        for i, image in enumerate(images):
            # Convert PIL image to base64
            img_byte_arr = BytesIO()
            image.save(img_byte_arr, format='JPEG')
            img_byte_arr = img_byte_arr.getvalue()
            base64_string = base64.b64encode(img_byte_arr).decode()
            base64_images.append({
                'page': i + 1,
                'image': base64_string
            })
            
        return base64_images
    except Exception as e:
        raise Exception(f"Error converting PDF to images: {str(e)}")