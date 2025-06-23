# Import the os module to access environment variables
import os

# Import the requests module to send HTTP requests
import requests

# Define a class called QAEngine for answering questions about celebrities
class QAEngine:
    
    # Constructor method to set up the API details
    def __init__(self):
        # Load the API key from the environment variable named "GROQ_API_KEY"
        self.api_key = os.getenv("GROQ_API_KEY")

        # Set the API endpoint for chat-based communication
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

        # Define the LLM model to be used for answering questions
        self.model = "meta-llama/llama-4-maverick-17b-128e-instruct"

    # Method to ask a question about a specific celebrity
    def ask_about_celebrity(self, name, question):
        # Prepare the HTTP headers with the API key and content type
        headers = {
            "Authorization": f"Bearer {self.api_key}",  # Add the API key
            "Content-Type": "application/json"          # Tell the server we're sending JSON
        }

        # Create a prompt string that includes the celebrity's name and the user's question
        prompt = f"""You are an AI assistant that knows a lot about celebrities. Answer the question about {name} concisely and accurately.

Question: {question}"""

        # Create the full request payload to send to the API
        payload = {
            "model": self.model,                        # Specify the model to use
            "messages": [{"role": "user", "content": prompt}],  # Add the user message
            "temperature": 0.5,                         # Set temperature (balance between creativity and accuracy)
            "max_tokens": 512                           # Limit the length of the response
        }

        # Send a POST request to the API with the headers and payload
        response = requests.post(self.api_url, headers=headers, json=payload)

        # If the API responds successfully
        if response.status_code == 200:
            # Return the content of the model's response
            return response.json()['choices'][0]['message']['content']
        
        # If something went wrong, return a friendly error message
        return "Sorry, I couldn't find the answer."
