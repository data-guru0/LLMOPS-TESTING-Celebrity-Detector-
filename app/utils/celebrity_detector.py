# Import the os module to access environment variables
import os

# Import base64 to encode image data for API requests
import base64

# Import requests to send HTTP requests to the API
import requests

# Define a class to handle celebrity detection using a language model
class CelebrityDetector:
    
    # Constructor method to initialize API settings
    def __init__(self):
        # Get the Groq API key from environment variables
        self.api_key = os.getenv("GROQ_API_KEY")

        # Set the API URL endpoint for making chat completions
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

        # Choose the specific model to use (LLaMA 4 instruct version)
        self.model = "meta-llama/llama-4-maverick-17b-128e-instruct"

    # Method to identify the celebrity from an image
    def identify(self, image_bytes):
        # Convert the image bytes into a base64-encoded string (so it can be sent as text)
        encoded_image = base64.b64encode(image_bytes).decode()

        # Prepare the headers with API key and content type
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Create the input prompt and image for the model
        prompt = {
            "model": self.model,
            "messages": [
                {
                    "role": "user",  # The message is coming from the user
                    "content": [
                        {
                            "type": "text",
                            "text": """You are a celebrity recognition expert AI. 
Identify the person in the image. If known, respond in this format:

- **Full Name**: 
- **Profession**:
- **Nationality**:
- **Famous For**:
- **Top Achievements**:

If unknown, return "Unknown".
"""
                        },
                        {
                            "type": "image_url",  # Attach the image
                            "image_url": {
                                # Insert the base64-encoded image as a data URL
                                "url": f"data:image/jpeg;base64,{encoded_image}"
                            }
                        }
                    ]
                }
            ],
            "temperature": 0.3,     # Low temperature = more accurate, less creative
            "max_tokens": 1024      # Limit the size of the response
        }

        # Send the POST request to the Groq API with the prompt and headers
        response = requests.post(self.api_url, headers=headers, json=prompt)

        # If the response is successful (status code 200)
        if response.status_code == 200:
            # Get the text output from the response
            result = response.json()['choices'][0]['message']['content']

            # Try to extract just the name from the result
            name = self.extract_name(result)

            # Return the full result and the name separately
            return result, name

        # If there was an error, return "Unknown"
        return "Unknown", ""

    # Method to extract the full name from the model's response
    def extract_name(self, content):
        # Go through each line of the content
        for line in content.splitlines():
            # Check if the line starts with "- **Full Name**:"
            if line.lower().startswith("- **full name**:"):
                # Split by ":" and return the name part
                return line.split(":")[1].strip()
        
        # If name not found, return "Unknown"
        return "Unknown"
