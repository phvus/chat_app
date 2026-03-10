from app import create_app, socketio

app = create_app()

if __name__ == '__main__':
    print("Starting Chat Application...")
    print("Open your browser and visit: http://localhost:5000")
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
