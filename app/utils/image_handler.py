# Importing OpenCV library for image processing
import cv2

# Importing NumPy library for handling arrays
import numpy as np

# Importing BytesIO to handle in-memory file operations
from io import BytesIO

# Function to process the uploaded image file
def process_image(image_file):
    # Create a BytesIO object to temporarily store the image in memory
    in_memory_file = BytesIO()

    # Save the uploaded image file into the in-memory file
    image_file.save(in_memory_file)

    # Get the byte data (raw image data) from the in-memory file
    image_bytes = in_memory_file.getvalue()

    # Convert the byte data into a NumPy array
    nparr = np.frombuffer(image_bytes, np.uint8)

    # Decode the NumPy array into an actual image (OpenCV format)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Convert the color image into grayscale (face detection works better on gray images)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Load the pre-trained face detection model (Haar cascade for frontal faces)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect all the faces in the grayscale image
    faces = face_cascade.detectMultiScale(gray, 1.1, 5)

    # If no faces are found, return the original image bytes and None
    if len(faces) == 0:
        return image_bytes, None

    # If multiple faces are found, choose the largest one (usually the main subject)
    largest_face = max(faces, key=lambda r: r[2] * r[3])

    # Extract the position and size of the largest face
    (x, y, w, h) = largest_face

    # Draw a green rectangle around the largest face on the image
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 3)

    # Encode the image with the rectangle into JPEG format
    is_success, buffer = cv2.imencode(".jpg", img)

    # Return the JPEG image bytes and the coordinates of the largest face
    return buffer.tobytes(), largest_face
