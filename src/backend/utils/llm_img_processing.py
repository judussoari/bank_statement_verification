import io
import json
import os
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
from openai import OpenAI
import base64

def llm_img_processing(client, file_bytes):
    """
    Called to process an image by directly taking an image as an input and passing it to a multimodal llm, 
    followed by extracting relevant information in JSON format using an LLM.
    """

    try: 
        image = Image.open(io.BytesIO(file_bytes))
        image = image.convert("RGB")
        image = image.filter(ImageFilter.SHARPEN)
        image = ImageEnhance.Contrast(image).enhance(7)
        image.show()

        # Convert image to JPEG bytes
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        file_bytes = base64.b64encode(buffer.getvalue()).decode("utf-8")
    except Exception as e:
        raise Exception(f"Error opening image: {e}")

    messages = [
        {
            "role": "user", 
            "content": [
                {
                    "type": 'text',
                    'text': "You extract refined details from the provided image rom bank statements of bank customers from all over the world. "
                "Please consider that in a bank statement, there usually is the bank's address, as well as the client's address. "
                "Please extract the client's address (usually located next/under personal details/name) and the bank address separately. "
                "Extract the person's first name and last name separately, and extract the components of the address details "
                "street name, street number, postal code, and city. Also extract the date at which the bank statement was created. "
                "Return the result as a JSON object with the following keys: "
                "'extracted_first_name', 'extracted_last_name', 'extracted_client_street_name', 'extracted_client_street_number', "
                "'extracted_client_postal_code', 'extracted_client_city', 'extracted_bank_street_name', 'extracted_bank_street_number', "
                "'extracted_bank_postal_code', 'extracted_bank_city', and 'document_date'. "
                "If a detail is not found, return its value as an empty string for each key that you can't find a value for."
                },
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{file_bytes}"}
                },
            ]
        },
    ]

    return messages
