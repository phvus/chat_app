from datetime import datetime
from typing import List

class User:
    """OOP Model for User"""
    def __init__(self, user_id: str, username: str, password: str):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.created_at = datetime.now()
        self.is_online = False
    
    def set_online(self, status: bool):
        """Set user online/offline status"""
        self.is_online = status
    
    def to_dict(self):
        """Convert user to dictionary"""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'is_online': self.is_online,
            'created_at': self.created_at.isoformat()
        }


class Message:
    """OOP Model for Message"""
    def __init__(self, message_id: str, sender_id: str, room_id: str, content: str):
        self.message_id = message_id
        self.sender_id = sender_id
        self.room_id = room_id
        self.content = content
        self.timestamp = datetime.now()
    
    def to_dict(self):
        """Convert message to dictionary"""
        return {
            'message_id': self.message_id,
            'sender_id': self.sender_id,
            'room_id': self.room_id,
            'content': self.content,
            'timestamp': self.timestamp.isoformat()
        }


class ChatRoom:
    """OOP Model for Chat Room"""
    def __init__(self, room_id: str, room_name: str, creator_id: str):
        self.room_id = room_id
        self.room_name = room_name
        self.creator_id = creator_id
        self.members: List[str] = [creator_id]
        self.messages: List[Message] = []
        self.created_at = datetime.now()
    
    def add_member(self, user_id: str):
        """Add member to room"""
        if user_id not in self.members:
            self.members.append(user_id)
            return True
        return False
    
    def remove_member(self, user_id: str):
        """Remove member from room"""
        if user_id in self.members:
            self.members.remove(user_id)
            return True
        return False
    
    def add_message(self, message: Message):
        """Add message to room"""
        self.messages.append(message)
    
    def get_messages(self, limit: int = 50):
        """Get last N messages"""
        return self.messages[-limit:]
    
    def to_dict(self):
        """Convert room to dictionary"""
        return {
            'room_id': self.room_id,
            'room_name': self.room_name,
            'creator_id': self.creator_id,
            'members': self.members,
            'member_count': len(self.members),
            'created_at': self.created_at.isoformat()
        }
