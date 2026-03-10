# Chat Application

A real-time web chat application built with Python Flask, WebSockets, and OOP principles. Users can create chat rooms, join conversations, and message friends in real-time.

## Features

- **User Authentication**: Register and login system with password hashing
- **Chat Rooms**: Create and join chat rooms with multiple users
- **Real-time Messaging**: WebSocket-based instant messaging
- **User Presence**: See online/offline status of users
- **Message History**: Messages are stored in SQLite database
- **OOP Architecture**: Clean, modular code using Object-Oriented Programming
- **Responsive UI**: Works on desktop and mobile devices

## Project Structure

```
chat_app/
├── app/
│   ├── __init__.py           # Flask app initialization
│   ├── models.py             # OOP Models (User, Message, ChatRoom)
│   ├── database.py           # Database handler class
│   ├── routes.py             # Flask routes and WebSocket events
│   ├── utils.py              # Utility functions
│   ├── templates/
│   │   ├── login.html        # Login page
│   │   ├── register.html     # Registration page
│   │   └── chat.html         # Main chat interface
│   └── static/
│       ├── css/
│       │   └── style.css     # Application styling
│       └── js/
│           └── chat.js       # Frontend JavaScript
├── venv/                     # Virtual environment
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
├── setup.bat                 # Setup script for Windows
├── setup.sh                  # Setup script for Linux/Mac
├── .gitignore               # Git ignore file
└── README.md                # This file
```

## Installation

### Windows

1. Download and extract the project
2. Double-click `setup.bat`
3. The virtual environment will be created and dependencies installed

### Linux/Mac

1. Download and extract the project
2. Run:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

## Running the Application

### Windows

```bash
# Activate virtual environment
venv\Scripts\activate.bat

# Run the application
python run.py
```

### Linux/Mac

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
python run.py
```

Then open your browser and visit: **http://localhost:5000**

## Usage

1. **Register**: Create a new account with username and password
2. **Login**: Login with your credentials
3. **Create Room**: Click "Create Room" to start a new chat room
4. **Join Room**: Click on any room in the list to join
5. **Send Message**: Type a message and click Send to chat with other users
6. **Leave Room**: Close the room to leave

## OOP Architecture

### Models (app/models.py)

- **User Class**: Manages user information, online status, and user data
- **Message Class**: Represents chat messages with sender, timestamp, and content
- **ChatRoom Class**: Manages chat rooms, members, and message history

### Database Handler (app/database.py)

- **Database Class**: Handles all database operations using SQLite
- Methods for CRUD operations on users, rooms, and messages
- Ensures data persistence and integrity

### Routes & WebSocket (app/routes.py)

- **Flask Routes**: HTTP endpoints for login, registration, and chat interface
- **WebSocket Events**: Real-time communication using Socket.IO
- **Event Handlers**: Handle user connections, messages, and room operations

## Technologies Used

- **Backend**: Python Flask, Flask-SocketIO
- **Frontend**: HTML5, CSS3, JavaScript, Socket.IO Client
- **Database**: SQLite3
- **Real-time Communication**: WebSockets
- **Architecture**: Object-Oriented Programming (OOP)

## Future Enhancements

- User profiles and avatars
- Direct messaging between users
- File sharing
- Emoji reactions
- Message search
- User blocking
- Admin controls
- Database migration to PostgreSQL
- Deployment to cloud (Heroku, AWS, etc.)

## License

This project is open source and available for personal and educational use.

## Support

For issues or questions, please refer to the code documentation or create an issue.
