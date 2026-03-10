from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO(cors_allowed_origins="*", manage_session=False)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-change-this'
    
    socketio.init_app(app, manage_session=False)
    
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
