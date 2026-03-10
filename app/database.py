import sqlite3
import os
import time
from typing import Optional, List
from app.models import User, ChatRoom, Message

class Database:
    """OOP Database handler for chat application with improved concurrency handling"""
    
    def __init__(self, db_path: str = 'chat_app.db'):
        self.db_path = db_path
        self._configure_sqlite()
        self.init_database()
    
    def _configure_sqlite(self):
        """Configure SQLite for better multi-user support"""
        try:
            conn = sqlite3.connect(self.db_path, timeout=10.0)
            cursor = conn.cursor()
            
            # Enable WAL mode for better concurrency
            cursor.execute('PRAGMA journal_mode=WAL')
            
            # Optimize cache size
            cursor.execute('PRAGMA cache_size=-64000')
            
            # Allow multiple readers
            cursor.execute('PRAGMA query_only=FALSE')
            
            # Set synchronous mode (NORMAL is faster than FULL, still safe)
            cursor.execute('PRAGMA synchronous=NORMAL')
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Warning: Could not configure SQLite optimally: {e}")
    
    def get_connection(self):
        """Create and return database connection with timeout and threading support"""
        # timeout=10.0 means wait 10 seconds if database is locked
        # check_same_thread=False allows usage across different threads (SocketIO requirement)
        return sqlite3.connect(
            self.db_path,
            timeout=10.0,
            check_same_thread=False,
            isolation_level='DEFERRED'
        )
    
    def init_database(self):
        """Initialize database tables"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_online BOOLEAN DEFAULT 0
            )
        ''')
        
        # Chat Rooms table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_rooms (
                room_id TEXT PRIMARY KEY,
                room_name TEXT NOT NULL,
                creator_id TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (creator_id) REFERENCES users(user_id)
            )
        ''')
        
        # Room Members table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS room_members (
                room_id TEXT NOT NULL,
                user_id TEXT NOT NULL,
                joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (room_id, user_id),
                FOREIGN KEY (room_id) REFERENCES chat_rooms(room_id),
                FOREIGN KEY (user_id) REFERENCES users(user_id)
            )
        ''')
        
        # Messages table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                message_id TEXT PRIMARY KEY,
                sender_id TEXT NOT NULL,
                room_id TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sender_id) REFERENCES users(user_id),
                FOREIGN KEY (room_id) REFERENCES chat_rooms(room_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    # User methods
    def create_user(self, user: User) -> bool:
        """Create new user with retry logic for database locks"""
        max_retries = 5
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO users (user_id, username, password) VALUES (?, ?, ?)',
                    (user.user_id, user.username, user.password)
                )
                conn.commit()
                conn.close()
                return True
            except sqlite3.OperationalError as e:
                if 'database is locked' in str(e):
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(0.5)  # Wait 500ms before retry
                        continue
                    else:
                        print(f"Database locked after {max_retries} retries")
                        return False
                else:
                    raise
            except sqlite3.IntegrityError:
                return False
            finally:
                try:
                    if 'conn' in locals():
                        conn.close()
                except:
                    pass
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Get user by ID with retry logic for locks"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT user_id, username, password FROM users WHERE user_id = ?', (user_id,))
                row = cursor.fetchone()
                conn.close()
                
                if row:
                    user = User(row[0], row[1], row[2])
                    user.is_online = True
                    return user
                return None
            except sqlite3.OperationalError as e:
                if 'database is locked' in str(e):
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(0.2)
                        continue
                else:
                    raise
            finally:
                try:
                    if 'conn' in locals():
                        conn.close()
                except:
                    pass
        
        return None
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Get user by username with retry logic for locks"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT user_id, username, password FROM users WHERE username = ?', (username,))
                row = cursor.fetchone()
                conn.close()
                
                if row:
                    return User(row[0], row[1], row[2])
                return None
            except sqlite3.OperationalError as e:
                if 'database is locked' in str(e):
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(0.3)
                        continue
                else:
                    raise
            finally:
                try:
                    if 'conn' in locals():
                        conn.close()
                except:
                    pass
        
        return None
    
    def update_user_status(self, user_id: str, is_online: bool):
        """Update user online status with retry logic for locks"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                cursor.execute('UPDATE users SET is_online = ? WHERE user_id = ?', (is_online, user_id))
                conn.commit()
                conn.close()
                return
            except sqlite3.OperationalError as e:
                if 'database is locked' in str(e):
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(0.2)
                        continue
                else:
                    raise
            finally:
                try:
                    if 'conn' in locals():
                        conn.close()
                except:
                    pass
    
    # ChatRoom methods
    def create_room(self, room: ChatRoom) -> bool:
        """Create new chat room with retry logic for locks"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO chat_rooms (room_id, room_name, creator_id) VALUES (?, ?, ?)',
                    (room.room_id, room.room_name, room.creator_id)
                )
                # Add creator as member
                cursor.execute(
                    'INSERT INTO room_members (room_id, user_id) VALUES (?, ?)',
                    (room.room_id, room.creator_id)
                )
                conn.commit()
                conn.close()
                return True
            except sqlite3.OperationalError as e:
                if 'database is locked' in str(e):
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(0.2)
                        continue
                else:
                    raise
            except sqlite3.IntegrityError:
                return False
            finally:
                try:
                    if 'conn' in locals():
                        conn.close()
                except:
                    pass
        
        return False
    
    def get_room(self, room_id: str) -> Optional[ChatRoom]:
        """Get room by ID with retry logic for locks"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT room_id, room_name, creator_id FROM chat_rooms WHERE room_id = ?', (room_id,))
                row = cursor.fetchone()
                
                if row:
                    room = ChatRoom(row[0], row[1], row[2])
                    # Get members
                    cursor.execute('SELECT user_id FROM room_members WHERE room_id = ?', (room_id,))
                    members = [member[0] for member in cursor.fetchall()]
                    room.members = members
                    
                    # Get messages
                    cursor.execute('SELECT message_id, sender_id, room_id, content FROM messages WHERE room_id = ? ORDER BY timestamp', (room_id,))
                    for msg_row in cursor.fetchall():
                        msg = Message(msg_row[0], msg_row[1], msg_row[2], msg_row[3])
                        room.messages.append(msg)
                    
                    conn.close()
                    return room
                conn.close()
                return None
            except sqlite3.OperationalError as e:
                if 'database is locked' in str(e):
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(0.2)
                        continue
                else:
                    raise
            finally:
                try:
                    if 'conn' in locals():
                        conn.close()
                except:
                    pass
        
        return None
    
    def get_all_rooms(self) -> List[ChatRoom]:
        """Get all chat rooms with retry logic for locks"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                cursor.execute('SELECT room_id, room_name, creator_id FROM chat_rooms')
                rows = cursor.fetchall()
                conn.close()
                
                rooms = []
                for row in rows:
                    room = self.get_room(row[0])
                    if room:
                        rooms.append(room)
                return rooms
            except sqlite3.OperationalError as e:
                if 'database is locked' in str(e):
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(0.2)
                        continue
                else:
                    raise
            finally:
                try:
                    if 'conn' in locals():
                        conn.close()
                except:
                    pass
        
        return []
    
    def add_member_to_room(self, room_id: str, user_id: str) -> bool:
        """Add member to room with retry logic for locks"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO room_members (room_id, user_id) VALUES (?, ?)',
                    (room_id, user_id)
                )
                conn.commit()
                conn.close()
                return True
            except sqlite3.OperationalError as e:
                if 'database is locked' in str(e):
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(0.2)
                        continue
                else:
                    raise
            except sqlite3.IntegrityError:
                return False
            finally:
                try:
                    if 'conn' in locals():
                        conn.close()
                except:
                    pass
        
        return False
    
    # Message methods
    def save_message(self, message: Message) -> bool:
        """Save message to database with retry logic for locks"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO messages (message_id, sender_id, room_id, content) VALUES (?, ?, ?, ?)',
                    (message.message_id, message.sender_id, message.room_id, message.content)
                )
                conn.commit()
                conn.close()
                return True
            except sqlite3.OperationalError as e:
                if 'database is locked' in str(e):
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(0.2)
                        continue
                else:
                    raise
            except sqlite3.IntegrityError:
                return False
            finally:
                try:
                    if 'conn' in locals():
                        conn.close()
                except:
                    pass
        
        return False
    
    def get_room_messages(self, room_id: str, limit: int = 50) -> List[Message]:
        """Get messages from a room with retry logic for locks"""
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                conn = self.get_connection()
                cursor = conn.cursor()
                cursor.execute(
                    'SELECT message_id, sender_id, room_id, content FROM messages WHERE room_id = ? ORDER BY timestamp DESC LIMIT ?',
                    (room_id, limit)
                )
                rows = cursor.fetchall()
                conn.close()
                
                messages = []
                for row in reversed(rows):
                    msg = Message(row[0], row[1], row[2], row[3])
                    messages.append(msg)
                return messages
            except sqlite3.OperationalError as e:
                if 'database is locked' in str(e):
                    retry_count += 1
                    if retry_count < max_retries:
                        time.sleep(0.2)
                        continue
                else:
                    raise
            finally:
                try:
                    if 'conn' in locals():
                        conn.close()
                except:
                    pass
        
        return []
