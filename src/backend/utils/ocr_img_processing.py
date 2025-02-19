import io
import json
import os
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
from openai import OpenAI
import base64

def ocr_img_processing(client, file_bytes):
    """
    Called to process an image by extracting the text using OCR first, 
    followed by extracting relevant information in JSON format using an LLM.
    """

    # Step 1: Load the image from bytes
    try:
        image = Image.open(io.BytesIO(file_bytes))
        # Preprocess images because they could be of bad quality
        image = image.convert("RGB")
        image = ImageEnhance.Contrast(image).enhance(2)
        image.show()
    except Exception as e:
        raise Exception(f"Error opening image: {e}")
    
    #Step 2: Extract text from the image using OCR (with pytesseract)
    try:
        ocr_text = pytesseract.image_to_string(image)
    except Exception as e:
        raise Exception(f"Error during OCR processing: {e}")

    # Step 3: prepare prompt for LLM and message/JSON schema for the LLM call.
    messages = [
        {
            "role": "developer", 
            "content": (
                "You extract refined details from the provided text that I extracted from bank statements of bank customers from all over the world via OCR. "
                "Please consider that in a bank statement, there usually is the bank's address, as well as the client's address. "
                "Please extract the client's address (usually located next/under personal details/name) and the bank address separately. "
                "Extract the person's first name and last name separately, and extract the components of the address details "
                "street name, street number, postal code, and city. Also extract the date at which the bank statement was created. "
                "Return the result as a JSON object with the following keys: "
                "'extracted_first_name', 'extracted_last_name', 'extracted_client_street_name', 'extracted_client_street_number', "
                "'extracted_client_postal_code', 'extracted_client_city', 'extracted_bank_street_name', 'extracted_bank_street_number', "
                "'extracted_bank_postal_code', 'extracted_bank_city', and 'document_date'. "
                "If a detail is not found, return its value as an empty string for each key that you can't find a value for."
            )
        },
        {
            "role": "user", 
            "content": f"Extract the details from the text: '''{ocr_text}'''"
        }
    ]

    return messages