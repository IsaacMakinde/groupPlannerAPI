import firebase_admin
from quart import Quart
from quart_cors import cors
import os
from dotenv import load_dotenv
from firebase_admin import credentials
from app.controllers.event_controller import events_bp
from app.controllers.image_controller import images_bp
from app.controllers.user_controller import users_bp
from app.controllers.category_controller import categories_bp


def create_app():
    app = Quart(__name__)
    app = cors(app)
    load_dotenv()
    
    # Firebase setup
    # Decode the private key in Python
    private_key = os.getenv("FIREBASE_PRIVATE_KEY", "").replace('\\n', '\n')

    firebase_creds_dict = {
        "type": os.getenv("FIREBASE_TYPE"),
        "project_id": os.getenv("FIREBASE_PROJECT_ID"),
        "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": private_key,
        "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
        "client_id": os.getenv("FIREBASE_CLIENT_ID"),
        "auth_uri": os.getenv("FIREBASE_AUTH_URI"),
        "token_uri": os.getenv("FIREBASE_TOKEN_URI"),
        "auth_provider_x509_cert_url": os.getenv("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
    }    
    firebase_creds = credentials.Certificate(firebase_creds_dict)
    
    BUCKET_NAME = os.getenv('FIREBASE_BUCKET')  # Add this to your `.env`
    
    try:
        firebase_admin.initialize_app(firebase_creds, {
            'storageBucket': BUCKET_NAME
        })
    except ValueError:
        print("Could not initialize Firebase app.")
        
    # Register blueprints
    app.register_blueprint(events_bp)
    app.register_blueprint(images_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(categories_bp)
    return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)
