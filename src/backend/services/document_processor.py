import io
import json
import os
from PIL import Image, ImageFilter, ImageEnhance
import pytesseract
from openai import OpenAI
import base64
from ...backend.utils.llm_img_processing import llm_img_processing
from ...backend.utils.ocr_img_processing import ocr_img_processing

from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise Exception("OPENAI_API_KEY environment variable not set.")

def process_document_image(
        client,
        file_bytes,
        processing
):
    """
    Processes a document image to extract the person's name, address, document date. 
    Image processing can be performed in 2 different ways, depending on the processing parameter.
    - processing='ocr':
        1. Extracts text from the image using Optical Character Recognition (OCR) to convert image with text to actual text
        2. LLM to extract the person's name, address, document date.
    - processing='llm':
        1. directly applies multimodal LLM capabilities to read the document and extract the required information

    Returns:
        dict: A dictionary containing:
            - 'extracted_name': The name extracted from the document.
            - 'extracted_address': The address extracted from the document.
            - 'document_date': The document date extracted.
    """
    if processing == 'ocr':
        messages = ocr_img_processing(client, file_bytes)
    elif processing == 'llm':
        messages = llm_img_processing(client, file_bytes)
    else:
        raise Exception("processing parameter must either be 'ocr' or 'llm'. ")

    json_schema = {
        "name": "refined_document_schema",
        "schema": {
            "type": "object",
            "properties": {
                "extracted_first_name": {
                    "description": "The first name extracted from the document",
                    "type": "string"
                },
                "extracted_last_name": {
                    "description": "The last name extracted from the document",
                    "type": "string"
                },
                "extracted_client_street_name": {
                    "description": "The street name extracted from the document",
                    "type": "string"
                },
                "extracted_client_street_number": {
                    "description": "The street number extracted from the document",
                    "type": "string"
                },
                "extracted_client_postal_code": {
                    "description": "The postal code extracted from the document",
                    "type": "string"
                },
                "extracted_client_city": {
                    "description": "The city extracted from the document",
                    "type": "string"
                },
                "extracted_bank_street_name": {
                    "description": "The street name extracted from the document",
                    "type": "string"
                },
                "extracted_bank_street_number": {
                    "description": "The street number extracted from the document",
                    "type": "string"
                },
                "extracted_bank_postal_code": {
                    "description": "The postal code extracted from the document",
                    "type": "string"
                },
                "extracted_bank_city": {
                    "description": "The city extracted from the document",
                    "type": "string"
                },
                "document_date": {
                    "description": "The date of the document",
                    "type": "string"
                }
            },
            "additionalProperties": False
        }
    }
    
    try:
        completion = client.chat.completions.create(
                model='gpt-4o-mini' if processing=='ocr' else 'gpt-4o',
                messages=messages,
                response_format={
                    "type": "json_schema",
                    "json_schema": json_schema
                }
                #temperature=0.0 #low temperature for deterministic output, which is needed here
            )
        response_content = completion.choices[0].message.content

        # Step 6: parse the JSON output from the LLM
        extracted_data = json.loads(response_content)

    except Exception as e:
        raise Exception(f"Error during LLM processing: {e}")
    
    return extracted_data


# Conditional block that only runs when the file is executed directly, not when it is imported as a module
if __name__ == '__main__':
    sample_image_path = r"/Users/julioarend/Documents/Documents/JobHunt/Taktile/data/documents/scan_1.jpg"

    with open(sample_image_path, 'rb') as f:
        file_bytes = f.read()
    client = OpenAI(api_key=openai_api_key)

    result = process_document_image(client, file_bytes, processing='llm')
    print("Extracted Data:")
    print(result)