# Import required FastAPI modules and custom routers
from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
# Router for user authentication and management
from api.route.user_name_route import router as userRouter
# Router for music collection management
from api.route.music_route import router as musicRouter
# Router for card game functionality
from api.route.card_route import router as cardRouter
# Router for pet management
from api.route.pet_route import router as petRouter
# Router for card game functionality
from api.route.casino_route import router as casinoRouter
# Router for shop functionality
from api.route.shop_route import router as shopRouter
# Router for image extraction
from api.route.image_extract_route import router as imageRouter
#socket io
from infrastructure.socketio import socket_app

from core.lifespan import lifeSpanConnect
# from pipecat_ai.integrations.webrtc import *

# import pipecat_ai.integrations.webrtc  # Removed because module could not be resolved


# Initialize FastAPI application with custom lifespan handler
# This ensures proper database connection management during application lifecycle
print("Starting FastAPI application...")
app = FastAPI(lifespan=lifeSpanConnect)

# Configure CORS middleware to allow cross-origin requests
# This enables the frontend to communicate with the API from different domains
# Important for development and production environments
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin for development
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers for maximum compatibility
    expose_headers=["header"],  # Allow Js to read specific headers
)

# Register API routers for different endpoints
# Each router handles a specific set of related endpoints and functionality
# User-related endpoints (login, signup, user management)
app.include_router(userRouter)
# Music-related endpoints (add, remove, list music)
app.include_router(musicRouter)
# Card-related endpoints (card game functionality)
app.include_router(cardRouter)
app.include_router(petRouter)    # Pet-related endpoints
app.include_router(casinoRouter)  # Casino-related endpoints
app.include_router(shopRouter)   # Shop-related endpoints
app.include_router(imageRouter)   # Shop-related endpoints

# Mount socket.io app
app.mount("/", socket_app)

# Run the BE in app
@app.get("/")
def root():
    print("Backend is running")
    return {"message": "Backend is running"}


if __name__ == "__main__":
    uvicorn.run("song_project:app", host="127.0.0.1", port=8000, reload=False)
