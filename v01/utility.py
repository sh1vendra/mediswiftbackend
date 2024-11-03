import json
from datetime import datetime
from v01.models import Query, Treatment
from groq import Groq
from rest_framework.response import Response
from rest_framework import status
GROQ_API_KEY = "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"
GROQ_MODEL="llama-3.1-70b-versatile"

def create_response(success, message, body=None, status=status.HTTP_200_OK):
    try:
        response_data = {'success': success, 'message': message}
        if body is not None:
            response_data['body'] = body
        return Response(response_data, status=status)
    except Exception as e:
        error_message = f"Error creating response: {str(e)}"
        return Response({'success': False, 'message': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def process_patient_query(query):
    """
    Processes a general query by retrieving all chat history and treatments, comparing them,
    and generating any necessary new treatment data through the Groq API.
    """
    try:
        # Retrieve all existing chat history and treatments
        context = get_all_treatments()
        chat_history = get_all_patient_history()
        
        # Generate a prompt for Groq to check and create treatment data if needed
        response_input = format_treatment_check_input(context, chat_history, query)
        treatment_response = generate_diagnosis_response(response_input)
        
        # If new treatment data is provided, parse it
        if treatment_response and "create_treatment" in treatment_response.lower():
            parsed_treatment_data = parse_treatment_data(treatment_response)
        
        return treatment_response  # Return the original response if no new treatment data
    except Exception as e:
        print(f"Error processing query: {e}")
        return "An error occurred while processing your query. Please try again later."

def get_all_patient_history():
    """
    Fetches all chat history.
    """
    try:
        prev_queries = Query.objects.all()  # Retrieve all queries
        if not prev_queries.exists():
            return "No prior history found."

        return [f"{q.query_text}\n{q.response_text}" for q in prev_queries]
    except Exception as e:
        print(f"Error retrieving chat history: {e}")
        return "An error occurred while retrieving history."

def get_all_treatments():
    """
    Fetches all treatment data from the database.
    """
    try:
        treatments = Treatment.objects.all()  # Retrieve all treatments
        if not treatments.exists():
            return "No treatment data found."

        return [f"{treatment.patient_name}: {treatment.disease}" for treatment in treatments]
    except Exception as e:
        print(f"Error retrieving treatments: {e}")
        return "An error occurred while retrieving treatments."

def format_treatment_check_input(context, chat_history, query):
    """
    Formats the input for Groq to compare chat history and treatment data, and suggest any new treatment.
    """
    return (
        f"Context:\n{context}\n\n"
        f"Chat History:\n{chat_history}\n\n"
        f"Please analyze the chat history and treatment context above. "
        f"If new treatment data is required based on the chat history, please provide it in the following format:\n"
        f"patient_name, date_of_illness, symptoms, disease, diagnosis, medication, frequency, length_of_treatment.\n"
        f"If the treatment data already exists, respond with 'Existing treatment found. No new data needed.'\n\n"
        f"Question: {query}\n\n"
        "Response:"
    )

def parse_treatment_data(treatment_data):
    """
    Parses structured treatment data from the response into a dictionary for saving.
    Adjust parsing as per Groq's output format (e.g., JSON or comma-separated values).
    """
    try:
        # Attempt to parse as JSON
        if treatment_data.strip().startswith("{"):
            parsed_data = json.loads(treatment_data)
        
        # If data is comma-separated, split and map to fields manually
        else:
            fields = treatment_data.split(",")
            if len(fields) != 8:
                raise ValueError("Invalid format for comma-separated data.")
            parsed_data = {
                "patient_name": fields[0].strip(),
                "date_of_illness": datetime.strptime(fields[1].strip(), '%Y-%m-%d').date(),  # Convert to date
                "symptoms": fields[2].strip(),
                "disease": fields[3].strip(),
                "diagnosis": fields[4].strip(),
                "medication": fields[5].strip(),
                "frequency": fields[6].strip(),
                "length_of_treatment": fields[7].strip()
            }
        
        # Validate parsed_data for required fields
        required_fields = ["patient_name", "date_of_illness", "symptoms", "disease", "diagnosis", "medication", "frequency", "length_of_treatment"]
        for field in required_fields:
            if field not in parsed_data or not parsed_data[field]:
                raise ValueError(f"Missing required field: {field}")
        
        return parsed_data
    
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error parsing treatment data: {e}")
        return None

def generate_diagnosis_response(query, model=None):
    """
    Uses the Groq API to generate a medical response based on the provided query.
    """
    try:
        api_key = GROQ_API_KEY
        model = model or GROQ_MODEL 
        if not api_key:
            raise ValueError("API key missing. Set the GROQ_API_KEY environment variable.")

        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": query}],
            model=model
        )
        return chat_completion.choices[0].message.content
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return "There was an issue with your request."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "An error occurred while processing your request."
