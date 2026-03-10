import uuid
from datetime import datetime

class Utils:
    """Utility functions for chat application"""
    
    @staticmethod
    def generate_id():
        """Generate unique ID"""
        return str(uuid.uuid4())
    
    @staticmethod
    def get_timestamp():
        """Get current timestamp"""
        return datetime.now().isoformat()
    
    @staticmethod
    def validate_username(username: str) -> bool:
        """Validate username format"""
        if len(username) < 3 or len(username) > 20:
            return False
        return username.isalnum() or '_' in username
    
    @staticmethod
    def validate_password(password: str) -> bool:
        """Validate password strength"""
        return len(password) >= 6
    
    @staticmethod
    def format_timestamp(timestamp_str: str) -> str:
        """Format timestamp for display"""
        try:
            dt = datetime.fromisoformat(timestamp_str)
            return dt.strftime("%I:%M %p")
        except:
            return timestamp_str
