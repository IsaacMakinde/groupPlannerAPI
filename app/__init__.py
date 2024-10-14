import firebase_admin
from quart import Quart
from quart_cors import cors
import os
import json
from dotenv import load_dotenv
from firebase_admin import credentials
from app.controllers.event_controller import events_bp
from app.controllers.image_controller import images_bp

load_dotenv()

def create_app():
    app = Quart(__name__)
    app = cors(app)
    
    # Firebase setup
    firebase_creds = os.getenv('FIREBASE_CREDENTIALS')
    BUCKET_NAME = os.getenv('FIREBASE_BUCKET')
    
    if firebase_creds and BUCKET_NAME:
        cred_dict = {
            "type": "service_account",
            "project_id": os.getenv('FIREBASE_PROJECT_ID'),
            "private_key_id": os.getenv('FIREBASE_PRIVATE_KEY_ID'),
            "private_key": os.getenv('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
            "client_email": os.getenv('FIREBASE_CLIENT_EMAIL'),
            "client_id": os.getenv('FIREBASE_CLIENT_ID'),
            "auth_uri": os.getenv('FIREBASE_AUTH_URI'),
            "token_uri": os.getenv('FIREBASE_TOKEN_URI'),
            "auth_provider_x509_cert_url": os.getenv('FIREBASE_AUTH_PROVIDER'),
            "client_x509_cert_url": os.getenv('FIREBASE_CLIENT_CERT')
        }
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred, {
            "storageBucket": BUCKET_NAME,
        })
        print("Firebase initialized and Flask app created!")
    # Register blueprints
    app.register_blueprint(events_bp)
    app.register_blueprint(images_bp)

    return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)
