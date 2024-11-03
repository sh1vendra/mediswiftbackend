import json
from datetime import datetime
from v01.models import Query, Treatment
from groq import Groq
from rest_framework.response import Response
from rest_framework import status

GROQ_API_KEY = "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"
GROQ_MODEL = "llama-3.1-70b-versatile"

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
    Processes the patient's query by retrieving history and treatments, then generates a personalized response.
    """
    try:
        # Retrieve all chat history and treatments
        context = get_all_treatments()
        chat_history = get_all_patient_history()
        
        # Format the input for the Groq model with a more conversational tone
        response_input = format_treatment_check_input(context, chat_history, query)
        treatment_response = generate_diagnosis_response(response_input)
        
        return treatment_response  # Return the original response if no new treatment data
    except Exception as e:
        print(f"Error processing query: {e}")
        return "I encountered an error while trying to understand your concerns. Could you please try again?"

def get_all_patient_history():
    """
    Retrieves all chat history for context.
    """
    try:
        prev_queries = Query.objects.all()
        if not prev_queries.exists():
            return "No prior history."

        return [f"{q.query_text}\n{q.response_text}" for q in prev_queries]
    except Exception as e:
        print(f"Error retrieving chat history: {e}")
        return "Sorry, I encountered an error while retrieving your history."

def get_all_treatments():
    """
    Retrieves all past treatments, if any.
    """
    try:
        treatments = Treatment.objects.all()
        if not treatments.exists():
            return "No prior treatments."

        return [f"{treatment.patient_name}: {treatment.disease}" for treatment in treatments]
    except Exception as e:
        print(f"Error retrieving treatments: {e}")
        return "Sorry, I encountered an error while retrieving treatment data."

def format_treatment_check_input(context, chat_history, query):
    """
    Prepares a conversational prompt for Groq.
    """
    return (
        f"Here’s what we know from previous conversations:\n{context}\n\n"
        f"And here’s the recent chat history:\n{chat_history}\n\n"
        f"Patient message: {query}\n\n"
        "Respond kindly and empathetically to understand the patient’s needs. "
        "If the patient is unclear, ask simple, friendly questions to gather the information needed."
        "Example: ‘How can I assist you today?’ or ‘Could you describe how you’re feeling?’"
    )

def parse_treatment_data(treatment_data):
    """
    Parses structured treatment data from the response.
    """
    try:
        if treatment_data.strip().startswith("{"):
            parsed_data = json.loads(treatment_data)
        else:
            fields = treatment_data.split(",")
            if len(fields) != 8:
                raise ValueError("Invalid format for data.")
            parsed_data = {
                "patient_name": fields[0].strip(),
                "date_of_illness": datetime.strptime(fields[1].strip(), '%Y-%m-%d').date(),
                "symptoms": fields[2].strip(),
                "disease": fields[3].strip(),
                "diagnosis": fields[4].strip(),
                "medication": fields[5].strip(),
                "frequency": fields[6].strip(),
                "length_of_treatment": fields[7].strip()
            }
        
        required_fields = ["patient_name", "date_of_illness", "symptoms", "disease", "diagnosis", "medication", "frequency", "length_of_treatment"]
        for field in required_fields:
            if field not in parsed_data or not parsed_data[field]:
                raise ValueError(f"Missing field: {field}")
        
        return parsed_data
    
    except (json.JSONDecodeError, ValueError) as e:
        print(f"Error parsing treatment data: {e}")
        return None

def generate_diagnosis_response(query, model=None):
    """
    Uses the Groq API to generate a friendly, conversational response.
    """
    try:
        api_key = GROQ_API_KEY
        model = model or GROQ_MODEL
        if not api_key:
            raise ValueError("API key missing.")

        client = Groq(api_key=api_key)
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": query}],
            model=model
        )
        return chat_completion.choices[0].message.content
    except ValueError as ve:
        print(f"ValueError: {ve}")
        return "Sorry, there was an issue with your request."
    except Exception as e:
        print(f"An error occurred: {e}")
        return "I encountered an error processing your request."