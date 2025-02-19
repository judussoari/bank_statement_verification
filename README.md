# Mini KYC App

This is a simple KYC (Know Your Customer) application that verifies a user's identity by comparing their details with information extracted from a bank statement image. The app uses FastAPI for the backend API, Tesseract for OCR, and the OpenAI API for fuzzy matching. A basic HTML frontend allows users to enter their details and upload an image.

## Features

- **REST API:** Built with FastAPI.
- **OCR Processing:** Uses Tesseract to extract text from images.
- **Fuzzy Matching:** Compares user details with extracted data using the OpenAI API (handles common abbreviations like "St" vs. "Street").
- **Simple Frontend:** A basic web form built with FastAPI and Jinja2.
- **Dockerized:** Easily run the application with Docker Compose.