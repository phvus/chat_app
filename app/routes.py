from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from flask_socketio import emit, join_room, leave_room, disconnect
from app import socketio
from app.database import Database
from app.models import User, ChatRoom, Message
from app.utils import Utils
import hashlib

main_bp = Blueprint('main', __name__)
db = Database()
connected_users = {}  # Track connected users {request.sid: {'user_id': ..., 'username': ...}}

def hash_password(password: str) -> str:
    """Hash password"""
    return hashlib.sha256(password.encode()).hexdigest()

@main_bp.route('/')
def index():
    """Home page"""
    if 'user_id' in session:
        return redirect(url_for('main.chat'))
    return redirect(url_for('main.login'))

@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = db.get_user_by_username(username)
        if user and user.password == hash_password(password):
            session['user_id'] = user.user_id
            session['username'] = user.username
            db.update_user_status(user.user_id, True)
            return redirect(url_for('main.chat'))
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@main_bp.route('/register', methods=['GET', 'POST'])
def register():
    """Register page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not Utils.validate_username(username):
            return render_template('register.html', error='Invalid username (3-20 chars, alphanumeric or underscore)')
        
        if not Utils.validate_password(password):
            return render_template('register.html', error='Password must be at least 6 characters')
        
        if password != confirm_password:
            return render_template('register.html', error='Passwords do not match')
        
        user = User(Utils.generate_id(), username, hash_password(password))
        if db.create_user(user):
            session['user_id'] = user.user_id
            session['username'] = user.username
            return redirect(url_for('main.chat'))
        
        return render_template('register.html', error='Username already exists')
    
    return render_template('register.html')

@main_bp.route('/chat')
def chat():
    """Chat page"""
    if 'user_id' not in session:
        return redirect(url_for('main.login'))
    
    rooms = db.get_all_rooms()
    return render_template('chat.html', username=session['username'], rooms=rooms)

@main_bp.route('/logout')
def logout():
    """Logout user"""
    if 'user_id' in session:
        db.update_user_status(session['user_id'], False)
        session.clear()
    return redirect(url_for('main.login'))

@main_bp.route('/api/rooms', methods=['GET', 'POST'])
def rooms_api():
    """API for room operations"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if request.method == 'POST':
        data = request.get_json()
        room_name = data.get('room_name')
        
        if not room_name or len(room_name) < 2:
            return jsonify({'error': 'Invalid room name'}), 400
        
        room = ChatRoom(Utils.generate_id(), room_name, session['user_id'])
        if db.create_room(room):
            return jsonify(room.to_dict()), 201
        
        return jsonify({'error': 'Failed to create room'}), 400
    
    rooms = db.get_all_rooms()
    return jsonify([room.to_dict() for room in rooms])

@main_bp.route('/api/rooms/<room_id>/join', methods=['POST'])
def join_room_api(room_id):
    """Join a chat room"""
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    if db.add_member_to_room(room_id, session['user_id']):
        return jsonify({'message': 'Joined room'}), 200
    
    return jsonify({'error': 'Already in room or room does not exist'}), 400

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle user connection"""
    # User will authenticate via join_room with auth data
    print(f"Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle user disconnection"""
    if request.sid in connected_users:
        user_data = connected_users[request.sid]
        username = user_data.get('username', 'Anonymous')
        emit('user_left', {'username': username}, broadcast=True)
        del connected_users[request.sid]
    print(f"Client disconnected: {request.sid}")

@socketio.on('auth')
def handle_auth(data):
    """Authenticate user via WebSocket"""
    user_id = data.get('user_id')
    username = data.get('username')
    
    if user_id and username:
        connected_users[request.sid] = {'user_id': user_id, 'username': username}
        emit('auth_success', {'message': 'Authenticated'})
    else:
        emit('auth_failed', {'message': 'Authentication failed'})

@socketio.on('join')
def on_join(data):
    """Handle user joining a room"""
    if request.sid not in connected_users:
        emit('error', {'message': 'Not authenticated'})
        return
    
    user_data = connected_users[request.sid]
    room_id = data.get('room_id')
    username = user_data.get('username', 'Anonymous')
    user_id = user_data.get('user_id')
    
    join_room(room_id)
    emit('message', {
        'username': 'System',
        'content': f'{username} joined the room',
        'timestamp': Utils.get_timestamp()
    }, room=room_id)

@socketio.on('send_message')
def handle_message(data):
    """Handle new message"""
    if request.sid not in connected_users:
        emit('error', {'message': 'Not authenticated'})
        return
    
    user_data = connected_users[request.sid]
    room_id = data.get('room_id')
    content = data.get('content')
    
    if not content or not room_id:
        return
    
    user_id = user_data.get('user_id')
    username = user_data.get('username')
    
    message = Message(Utils.generate_id(), user_id, room_id, content)
    db.save_message(message)
    
    emit('message', {
        'username': username,
        'content': content,
        'timestamp': Utils.get_timestamp()
    }, room=room_id)

@socketio.on('leave')
def on_leave(data):
    """Handle user leaving a room"""
    if request.sid not in connected_users:
        emit('error', {'message': 'Not authenticated'})
        return
    
    user_data = connected_users[request.sid]
    room_id = data.get('room_id')
    username = user_data.get('username', 'Anonymous')
    
    leave_room(room_id)
    emit('message', {
        'username': 'System',
        'content': f'{username} left the room',
        'timestamp': Utils.get_timestamp()
    }, room=room_id)
