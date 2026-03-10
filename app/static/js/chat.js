// WebSocket connection
const socket = io();
let currentRoom = null;

// Initialize chat when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Authenticate with WebSocket
    const usernameSpan = document.getElementById('username-display');
    const username = usernameSpan.textContent;
    const userId = usernameSpan.dataset.userId;
    
    if (username && userId) {
        socket.emit('auth', {
            user_id: userId,
            username: username
        });
    }
    
    loadRooms();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    document.getElementById('create-room-btn').addEventListener('click', openCreateRoomModal);
    document.getElementById('message-form').addEventListener('submit', sendMessage);
    
    // Modal close
    const modal = document.getElementById('create-room-modal');
    const closeBtn = document.querySelector('.close');
    closeBtn.addEventListener('click', closeCreateRoomModal);
    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            closeCreateRoomModal();
        }
    });
}

// Load all rooms
async function loadRooms() {
    try {
        const response = await fetch('/api/rooms');
        const rooms = await response.json();
        
        const roomsList = document.getElementById('rooms-list');
        roomsList.innerHTML = '';
        
        rooms.forEach(room => {
            const roomItem = createRoomElement(room);
            roomsList.appendChild(roomItem);
        });
    } catch (error) {
        console.error('Error loading rooms:', error);
    }
}

// Create room element
function createRoomElement(room) {
    const div = document.createElement('div');
    div.className = 'room-item';
    div.innerHTML = `
        <div class="room-item-name">${room.room_name}</div>
        <div class="room-item-members">${room.member_count} members</div>
    `;
    
    div.addEventListener('click', () => selectRoom(room));
    return div;
}

// Select room
function selectRoom(room) {
    currentRoom = room;
    
    // Update UI
    document.getElementById('no-selection').style.display = 'none';
    document.getElementById('chat-area').style.display = 'flex';
    document.getElementById('room-title').textContent = room.room_name;
    
    // Clear messages
    document.getElementById('messages').innerHTML = '';
    
    // Update active room
    document.querySelectorAll('.room-item').forEach(item => {
        item.classList.remove('active');
    });
    event.target.closest('.room-item').classList.add('active');
    
    // Join room via socket
    socket.emit('join', { room_id: room.room_id });
    
    // Load previous messages (you can implement this)
}

// Send message
function sendMessage(event) {
    event.preventDefault();
    
    if (!currentRoom) {
        alert('Please select a room first');
        return;
    }
    
    const input = document.getElementById('message-input');
    const content = input.value.trim();
    
    if (!content) return;
    
    socket.emit('send_message', {
        room_id: currentRoom.room_id,
        content: content
    });
    
    input.value = '';
}

// Open create room modal
function openCreateRoomModal() {
    document.getElementById('create-room-modal').style.display = 'block';
}

// Close create room modal
function closeCreateRoomModal() {
    document.getElementById('create-room-modal').style.display = 'none';
    document.getElementById('create-room-form').reset();
}

// Create room
async function createRoom(event) {
    event.preventDefault();
    
    const roomName = document.getElementById('room-name').value;
    
    try {
        const response = await fetch('/api/rooms', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ room_name: roomName })
        });
        
        if (response.ok) {
            closeCreateRoomModal();
            loadRooms();
        } else {
            alert('Failed to create room');
        }
    } catch (error) {
        console.error('Error creating room:', error);
        alert('Error creating room');
    }
}

// Socket event listeners
socket.on('message', function(data) {
    const messagesDiv = document.getElementById('messages');
    const messageDiv = document.createElement('div');
    
    const isSystemMessage = data.username === 'System';
    messageDiv.className = `message ${isSystemMessage ? 'system-message' : ''}`;
    
    messageDiv.innerHTML = `
        <div class="message-user">${data.username}</div>
        <div class="message-content">${escapeHtml(data.content)}</div>
        <div class="message-timestamp">${formatTime(data.timestamp)}</div>
    `;
    
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
});

socket.on('user_connected', function(data) {
    console.log(data.username + ' connected');
});

// Helper functions
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function formatTime(timestamp) {
    try {
        const date = new Date(timestamp);
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    } catch {
        return timestamp;
    }
}
