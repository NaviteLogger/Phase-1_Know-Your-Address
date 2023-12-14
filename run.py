"""
This is the main file that will be used to run the application
"""
from app import create_app

# Create the app instance
app = create_app()

if __name__ == "__main__":
    with app.app_context():
        app.run()
