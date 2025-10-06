"""
app.py - Assignment 4 (Lesson 4)
Flask Application Factory Runner
"""
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from application import create_app

# Choose config via FLASK_CONFIG env var: development (default), testing, production
app = create_app()

if __name__ == "__main__":
    # Dev server only (OK for classwork)
    app.run(host="127.0.0.1", port=5000, debug=True)
