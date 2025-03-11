import os
import groq
from typing import Optional
from dotenv import load_dotenv

def setup_groq_client() -> Optional[groq.Client]:
    """Set up and return Groq client with API key."""
    # Load environment variables from .env file
    load_dotenv()
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("\nError: GROQ_API_KEY not found in environment variables")
        return None
    return groq.Client(api_key=api_key)

def get_disease_from_symptoms(symptoms: str) -> Optional[str]:
    """
    Queries Groq API to analyze symptoms and return the most likely disease with a description.
    """
    client = setup_groq_client()
    if not client:
        return None

    if not symptoms.strip():
        print("Error: No symptoms provided")
        return None

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system", 
                    "content": "You are a medical AI assistant that identifies potential conditions based on symptoms. Always include disclaimers about seeking professional medical advice."
                },
                {
                    "role": "user", 
                    "content": f"Given the symptoms: {symptoms}, determine the most likely conditions. Provide the names of possible conditions and brief descriptions."
                }
            ],
            model="mixtral-8x7b-32768",
            temperature=0.5,
            max_tokens=500,
        )
        
        return chat_completion.choices[0].message.content

    except Exception as e:
        print(f"Error during API call: {str(e)}")
        return None

def main():
    print("Welcome to the Symptom Analyzer!")
    print("Please enter your symptoms (e.g., fever, cough, fatigue):")
    
    try:
        symptoms = input().strip()
        if not symptoms:
            print("No symptoms entered. Please try again.")
            return

        print("\nAnalyzing symptoms...")
        result = get_disease_from_symptoms(symptoms)
        
        if result:
            print("\nAnalysis Result:")
            print(result)
            print("\nDisclaimer: This is for informational purposes only. Always consult a healthcare professional for medical advice.")
        else:
            print("\nCould not analyze symptoms at this time. Please check if your API key is correct.")

    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")

if __name__ == '__main__':
    main()
