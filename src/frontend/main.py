from fastapi import FastAPI, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="/app/src/frontend/templates")

# API endpoint for the backend service
API_URL = "http://backend:8000/process_document"

@app.get('/', response_class=HTMLResponse)
async def index(request: Request):
    """
    Display the main form page for user input.
    
    Args:
        request (Request): The incoming FastAPI request object
    
    Returns:
        TemplateResponse: Renders the index.html template
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/submit", response_class=HTMLResponse)
async def submit(
    request: Request,
    user_first_name: str = Form(...),
    user_last_name: str = Form(...),
    user_street_name: str = Form(...),
    user_street_number: str = Form(...),
    user_postal_code: str = Form(...),
    user_city: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Process the form submission and handle file upload.
    
    Args:
        request (Request): The incoming FastAPI request object
        user_first_name (str): User's first name
        user_last_name (str): User's last name
        user_street_name (str): Street name of user's address
        user_street_number (str): Street number of user's address
        user_postal_code (str): Postal code of user's address
        user_city (str): City of user's address
        file (UploadFile): The uploaded file to be processed
    
    Returns:
        TemplateResponse: Renders the result.html template with processed data
    
    Note:
        The function performs the following steps:
        1. Reads the uploaded file
        2. Sends the file and user data to the backend API
        3. Returns the processed results to the user
    """
    # Read the contents of the uploaded file
    file_bytes = await file.read()

    # Make a POST request to the backend API
    async with httpx.AsyncClient() as client:
        # Send both the file and form data to the backend for processing
        response = await client.post(
            API_URL,
            files={'file': (file.filename, file_bytes, file.content_type)},
            data={
                # User personal information
                "first_name": user_first_name,
                "last_name": user_last_name,
                # User address information
                "street_name": user_street_name,
                "street_number": user_street_number,
                "postal_code": user_postal_code,
                "city": user_city,
            }
        )

    # Parse the JSON response from the backend
    result = response.json()

    # Render the result page with the processed data
    return templates.TemplateResponse("result.html", {"request": request, "result": result})

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=9000, reload=True)