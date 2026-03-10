from flask import Flask
from flask_socketio import SocketIO
import os

# Initialize SocketIO with CORS settings to allow connections from any device on the network
socketio = SocketIO(
    cors_allowed_origins="*",  # Allow connections from any origin (for LAN/network use)
    manage_session=False,
    ping_timeout=60,
    ping_interval=25,
    logger=False,
    engineio_logger=False
)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-this')
    
    # Enable CORS and allow all origins for network connectivity
    app.config['JSON_SORT_KEYS'] = False
    
    socketio.init_app(
        app,
        manage_session=False,
        cors_allowed_origins="*"
    )
    
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
