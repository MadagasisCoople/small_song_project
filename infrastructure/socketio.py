import logging
from typing import Dict, Any
from socketio import AsyncServer, ASGIApp
import asyncio

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
    await sio.emit('connected', {'sid': sid}, room=sid)


@sio.event
async def disconnect(sid):
    """Handle client disconnection"""
    logger.info(f"Client disconnected: {sid}")

async def manual_emit(task_name:str,data:Dict[str,Any],user_id: str):
    await sio.emit(task_name, data, room=user_id)