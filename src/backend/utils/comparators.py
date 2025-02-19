
import json
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise Exception("OPENAI_API_KEY environment variable not set.")

def compare_identity(
    # User-provided data:
    user_first_name: str,
    user_last_name: str,
    user_street_name: str,
    user_street_number: str,
    user_postal_code: str,
    user_city: str,
    # Extracted data from the bank statement:
    extracted_first_name: str,
    extracted_last_name: str,
    extracted_client_street_name: str,
    extracted_client_street_number: str,
    extracted_client_postal_code: str,
    extracted_client_city: str,
) -> bool:
    """
    Uses OpenAI's API to compare user-provided identity and address details with the extracted details.
    The prompt instructs the model to consider common abbreviations (e.g., "St" vs. "Street") as equivalent.
    
    Returns:
        bool: True if the model determines that the data match (i.e. identity is verified), otherwise False.
    """
    # Organize the data into dictionaries
    user_data = {
        "first_name": user_first_name,
        "last_name": user_last_name,
        "street_name": user_street_name,
        "street_number": user_street_number,
        "postal_code": user_postal_code,
        "city": user_city,
    }
    extracted_data = {
        "first_name": extracted_first_name,
        "last_name": extracted_last_name,
        "street_name": extracted_client_street_name,
        "street_number": extracted_client_street_number,
        "postal_code": extracted_client_postal_code,
        "city": extracted_client_city,
    }

    # Prepare the messages for the chat completion
    messages = [
        {
            "role": "developer",
            "content": (
                "You are a highly accurate identity verification assistant. "
                "Compare two sets of personal data (user-provided and extracted from a bank statement) and determine if they refer to the same identity. "
                "Consider that abbreviations such as 'St' and 'Street', 'Ave' and 'Avenue', 'Ct' and 'Court' are equivalent. "
                "Also consider that either city or postal code need to be the same, as they are equivalent information. This accounts for manual typos. "
                "Return your answer as a JSON object with a single boolean field 'is_verified', which is true if the data match and false otherwise."
            )
        },
        {
            "role": "user",
            "content": f"User Data: {json.dumps(user_data)}\n\nExtracted Data: {json.dumps(extracted_data)}"
        }
    ]

    # Define the expected JSON schema for the response
    json_schema = {
        "name": "comparison_schema",
        "schema": {
            "type": "object",
            "properties": {
                "is_verified": {
                    "type": "boolean",
                    "description": "True if the user data and extracted data match considering common abbreviations; false otherwise."
                }
            },
            "required": ["is_verified"],
            "additionalProperties": False
        }
    }

    # Ensure that the OpenAI API key is set
    # openai_api_key = os.getenv("OPENAI_API_KEY")
    # if not openai_api_key:
    #     raise Exception("OPENAI_API_KEY environment variable not set.")
    # openai.api_key = openai_api_key

    client = OpenAI(api_key=openai_api_key)

    try:
        # Call the OpenAI ChatCompletion API with the JSON schema response format.
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  # Adjust the model name as needed
            messages=messages,
            temperature=0.0,  # Low temperature for deterministic output
            response_format={
                "type": "json_schema",
                "json_schema": json_schema
            }
        )
        response_content = completion.choices[0].message.content
        result = json.loads(response_content)
        return result.get("is_verified", False)
    except Exception as e:
        raise Exception(f"Error during identity comparison: {e}")

if __name__ == '__main__':
    # Example test case
    is_verified = compare_identity(
        user_first_name='John',
        user_last_name='Smith',
        user_street_name='Coventry Avenue',
        user_street_number='2450',
        user_postal_code='78521',
        user_city='Brownsville',
        extracted_first_name='John',
        extracted_last_name='Smith',
        extracted_client_street_name='Coventry Av',
        extracted_client_street_number='2450',
        extracted_client_postal_code='78521',
        extracted_client_city='Brownsville',
    )
    print(is_verified)
