import logging
from typing import Dict, Any
from socketio import AsyncServer, ASGIApp
from collections import deque

# Global queue for messages from frontend
user_message_queue =  deque()
logger = logging.getLogger(__name__)

# Socket.IO server instance
sio = AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*",
)

# Socket.IO app
socket_app = ASGIApp(sio)

@sio.event
async def connect(sid, environ, auth):
    print(f"Client connected: {sid}")
    await manual_emit("connected",{},sid)


@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {sid}")

@sio.event
async def response(sid,data):
    """Handle client's response"""
    #Checking input data 
    if not isinstance(data, dict):
        print("Not match data")
        return
    msg = data.get("message")  # expect frontend sends {"message": "..."}
    print(msg)
    #Save input
    if msg:
        user_message_queue.append(msg)
        logger.info(f"Received from {sid}: {msg}")
        print(list(user_message_queue))

async def manual_emit(task_name:str,data:Dict[str,Any],user_id: str):
    await sio.emit(task_name, data, user_id)