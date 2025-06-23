# Import necessary Flask modules
from flask import Blueprint, render_template, request

# Import utility functions and classes from other parts of the app
from app.utils.image_handler import process_image
from app.utils.celebrity_detector import CelebrityDetector
from app.utils.qa_engine import QAEngine

# Import base64 to encode image data for displaying in HTML
import base64

# Create a Flask Blueprint named "main" for organizing routes
main = Blueprint("main", __name__)

# Create an instance of the CelebrityDetector class
celebrity_detector = CelebrityDetector()

# Create an instance of the QAEngine class
qa_engine = QAEngine()

# Define the main route for the app, handling both GET and POST requests
@main.route("/", methods=["GET", "POST"])
def index():
    # Initialize variables for displaying results
    player_info = ""
    result_img_data = ""
    user_question = ""
    answer = ""

    # Check if the form was submitted using POST method
    if request.method == "POST":
        
        # If an image was uploaded
        if "image" in request.files:
            # Get the image file from the form
            image_file = request.files["image"]

            # Check if a valid file was uploaded
            if image_file:
                # Process the image: detect face and get image bytes
                img_bytes, face_box = process_image(image_file)

                # Use the celebrity detector to identify the person in the image
                player_info, player_name = celebrity_detector.identify(img_bytes)

                # If a face was found, convert image bytes to base64 for HTML display
                if face_box is not None:
                    result_img_data = base64.b64encode(img_bytes).decode()
                else:
                    # If no face detected, show a message
                    player_info = "No face detected. Please try another image."

        # If the user submitted a question about the celebrity
        elif "question" in request.form:
            # Get the question from the form input
            user_question = request.form["question"]

            # Also get the previously saved name, info, and image to keep context
            player_name = request.form["player_name"]
            player_info = request.form["player_info"]
            result_img_data = request.form["result_img_data"]

            # Use the QA engine to answer the question based on the celebrity's name
            answer = qa_engine.ask_about_celebrity(player_name, user_question)

    # Render the HTML template with all the variables passed in
    return render_template(
        "index.html",
        player_info=player_info,
        result_img_data=result_img_data,
        user_question=user_question,
        answer=answer
    )
