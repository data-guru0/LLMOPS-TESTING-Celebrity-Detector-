# Import Flask to create the web application
from flask import Flask

# Import load_dotenv to load environment variables from a .env file
from dotenv import load_dotenv

# Import os module to work with file paths and environment variables
import os

# Define a function to create and configure the Flask app
def create_app():
    # Load environment variables from the .env file
    load_dotenv()

    # Set the path to the templates folder (used to render HTML)
    template_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))

    # Create a Flask app instance, telling it where to find the templates
    app = Flask(__name__, template_folder=template_path)  

    # Set a secret key for securely handling sessions and forms
    app.secret_key = os.getenv("SECRET_KEY", "default_secret")

    # Import the blueprint (routes) from the app.routes module
    from app.routes import main

    # Register the blueprint so Flask knows about the app routes
    app.register_blueprint(main)

    # Return the configured Flask app
    return app
