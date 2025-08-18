
# User Route Module
# Handles all user-related API endpoints including:
# - User registration
# - User authentication
# - User management

from io import BytesIO
from fastapi import APIRouter, Depends , File, UploadFile
from infrastructure.mongo_DB import getMongoDB
from fastapi.responses import FileResponse, StreamingResponse

from service.user_service import UserService
from service.pet_service import PetService
from service.voice_service import VoiceService
from service.handling_return import HandlingReturn

print("User route initialized")
router = APIRouter()

userService = UserService()
petService = PetService()
voiceService = VoiceService()
handlingReturn = HandlingReturn()

@router.post("/addUser/")
async def addUser(username: str, password: str, db = Depends(getMongoDB)):
    """
    Register a new user
    
    Args:
        username: New user's username
        password: New user's password
        
    Returns:
        dict: Success status and user details
    """
    text_output = await userService.add_user(username, password, db)
    audio_output = await voiceService.speak_up(text_output["message"])
    return await handlingReturn.text_and_audio(audio_output,text_output["message"])

@router.delete("/deleteAllUsers/")
async def deleteAllUsers(db = Depends(getMongoDB)):
    return await userService.delete_all(db)

@router.delete("/deleteUser/")
async def deleteUser(username: str, db = Depends(getMongoDB)):
    text_output = await userService.delete_user(username, db)
    audio_output = await voiceService.speak_up(text_output["message"])
    return await handlingReturn.text_and_audio(audio_output,text_output["message"])

@router.get("/numberOfUsers")
async def numberOfUsers(db = Depends(getMongoDB)):
    return await userService.count(db)

@router.get("/checkingUser/")
async def checkingUser(username: str, password: str, db = Depends(getMongoDB)):
    
    """
    Authenticate a user
    
    Args:
        username: Username to authenticate
        password: Password to authenticate
        db: Database connection instance
        
    Returns:
        dict: Success status and user details
    """
    return await userService.checking(username, password, db)

@router.get("/getUserId/")
async def getUserId(username: str, db = Depends(getMongoDB)):
    return await userService.get_user_id(username, db)


