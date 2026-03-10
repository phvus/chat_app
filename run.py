import os
import sys
from app import create_app, socketio
from app.network_utils import print_network_info

# Get host and port from environment variables or use defaults
HOST = os.environ.get('CHAT_APP_HOST', '0.0.0.0')
PORT = int(os.environ.get('CHAT_APP_PORT', 5000))
DEBUG = os.environ.get('CHAT_APP_DEBUG', 'True').lower() == 'true'

app = create_app()

if __name__ == '__main__':
    try:
        print_network_info(PORT, HOST)
        print("Starting Chat Application...\n")
        socketio.run(app, debug=DEBUG, host=HOST, port=PORT, 
                     allow_unsafe_werkzeug=True)
    except OSError as e:
        if e.errno == 10048:  # Port already in use (Windows error)
            print(f"\n❌ ERROR: Port {PORT} is already in use!")
            print(f"   Either:")
            print(f"   1. Close the other application using port {PORT}")
            print(f"   2. Or use a different port: set CHAT_APP_PORT=5001 and try again")
            sys.exit(1)
        else:
            print(f"\n❌ ERROR: {e}")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n👋 Chat Application stopped.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        sys.exit(1)
