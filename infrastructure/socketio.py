import logging
from typing import Dict, Any
from socketio import AsyncServer, ASGIApp
from collections import deque
import asyncio

# Global queue for messages from frontend
user_message_queue: asyncio.Queue[str] = asyncio.Queue()
print(user_message_queue.qsize())
logger = logging.getLogger(__name__)

# Socket.IO server instance
sio = AsyncServer(
    async_mode='asgi',
    cors_allowed_origins="*",
)

# Socket.IO app
socket_app = ASGIApp(sio)

global_sid = None
@sio.event
async def connect(sid:str, environ, auth):
    global global_sid
    print(f"Client connected: {sid}")
    global_sid = sid
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
    #Save input
    if msg:
        print(msg)
        await user_message_queue.put(msg)
        logger.info(f"Received from {sid}: {msg}")
        print(user_message_queue.qsize())

async def manual_emit(task_name:str,data:Dict[str,Any],user_id=global_sid):
    await sio.emit(task_name, data, user_id)

class SocketIOSever:
    def __init__(self):
        pass