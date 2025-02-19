from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
import base64

from src.backend.services.document_processor import process_document_image
from src.backend.utils.comparators import compare_identity
from openai import OpenAI

from dotenv import load_dotenv
import os

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise Exception("OPENAI_API_KEY environment variable not set.")
app = FastAPI(title='KYC Document Processor API')

# Initialize OpenAI client with API key
client = OpenAI(api_key=openai_api_key)

@app.post("/process_document", summary="Process a document and verify identity")
async def process_document(
    file: UploadFile = File(...),
    first_name: str = Form(...),
    last_name: str = Form(...),
    street_name: str = Form(...),
    street_number: str = Form(...),
    postal_code: str = Form(...),
    city: str = Form(...),
):
    """
    Process and verify a KYC (Know Your Customer) document against provided user information.
    
    Args:
        file (UploadFile): The document image file (JPEG or PNG)
        first_name (str): User's provided first name
        last_name (str): User's provided last name
        street_name (str): User's provided street name
        street_number (str): User's provided street number
        postal_code (str): User's provided postal code
        city (str): User's provided city
    
    Returns:
        JSONResponse: A message indicating whether verification was successful
    
    Raises:
        HTTPException: If file type is invalid or document processing fails
    
    Process Flow:
        1. Validates the uploaded file format
        2. Processes the document using OCR and LLM
        3. Compares extracted information with user-provided data
        4. Returns verification result
    """
    # Validate file type: Only JPEG or PNG allowed
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type. Only JPEG and PNG allowed."
        )
    
    # Read the uploaded file into memory
    file_bytes = await file.read()
    
    # Process the document image using OCR and LLM
    # This step extracts text from the image and processes it using OpenAI
    try:
        extracted_data = process_document_image(
            client=client, 
            file_bytes=file_bytes, 
            processing='ocr'
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {e}"
        )
    
    # Compare user-provided information with extracted data
    # This verification step ensures the document matches the user's input
    is_verified = compare_identity(
        # User-provided information
        user_first_name=first_name,
        user_last_name=last_name,
        user_street_name=street_name,
        user_street_number=street_number,
        user_postal_code=postal_code,
        user_city=city,
        
        # Information extracted from the document
        extracted_first_name=extracted_data.get("extracted_first_name"),
        extracted_last_name=extracted_data.get("extracted_last_name"),
        extracted_client_street_name=extracted_data.get("extracted_client_street_name"),
        extracted_client_street_number=extracted_data.get("extracted_client_street_number"),
        extracted_client_postal_code=extracted_data.get("extracted_client_postal_code"),
        extracted_client_city=extracted_data.get("extracted_client_city"),
    )

    # Return appropriate response based on verification result
    response = "Thank you very much. You have been verified successfully." if is_verified else "Verification failed, please try again."
    return JSONResponse(content=response)

# Run the API directly with uvicorn if this python file is executed
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)