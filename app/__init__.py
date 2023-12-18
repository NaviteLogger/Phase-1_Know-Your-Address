from flask import Flask
from dotenv import load_dotenv
import os

""" 
The "Application Factory" (in this case the 'create_app' function) is a 
pattern in Flask where the application is created inside a function,
allowing for different instances of the app to be created with different 
configurations. This is particularly useful for:
- Configuring applications differently for different environments (development, testing, production, etc.)
- Ensuring that resources (like databases) are correctly set up every time an app instance is created.
- Facilitating unit testing by easily allowing the creation of a fresh app instance for each test.
"""


def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__)

    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Get the secret key from the configuration file
    app.secret_key = app.config["SECRET_KEY"]

    # Load environment variables from .env file
    load_dotenv()

    # Load the appropriate config file
    if os.environ.get("FLASK_ENV") == "development":
        app.config.from_object("instance.config.DevelopmentConfig")
    elif os.environ.get("FLASK_ENV") == "testing":
        app.config.from_object("instance.config.TestingConfig")
    elif os.environ.get("FLASK_ENV") == "production":
        app.config.from_object("instance.config.ProductionConfig")
    else:
        print("FLASK_ENV environment variable is not set!")

    # Register blueprints within app context
    from app.main.routes import main_bp

    # Register the main blueprint
    app.register_blueprint(main_bp)

    return app
