# Music Route Module
# Handles all music-related API endpoints including:
# - Music collection management
# - Music recommendations
# - Music selection

from fastapi import APIRouter, File, HTTPException, Depends, UploadFile
from infrastructure.mongo_DB import getMongoDB
from service.music_service import MusicService
from service.random_recommender_service import RecommendService
from service.voice_service import VoiceService
from service.handling_return import HandlingReturn
print("Music route initialized")

router = APIRouter()

musicService = MusicService()
recommendService = RecommendService()
voiceService = VoiceService()
handlingReturn = HandlingReturn()

@router.post("/addMusic/")
async def addMusic(username: str, userMusic: str, db = Depends(getMongoDB)):
    """
    Add a new music to user's collection
    
    Args:
        username: Username of the user
        music: Music identifier to add
        
    Returns:
        dict: Success status and music details
    """
    
    text_output = await musicService.add_song(username, userMusic, db)
    audio_output = await voiceService.speak_up(text_output["message"])
    return await handlingReturn.text_and_audio(audio_output,text_output["message"])

@router.get("/getAllUserMusic/")
async def getAllUserMusic(username: str, db = Depends(getMongoDB)):
    """
    Get all music in user's collection
    
    Args:
        username: Username to fetch music for
        
    Returns:
        list: List of music documents
    """
    return await musicService.get_all_song(username, db)

@router.delete("/deleteMusic/")
async def deleteMusic(username: str, musicId: str, db = Depends(getMongoDB)):
    """
    Remove a music from user's collection
    
    Args:
        username: Username of the user
        music: Music identifier to remove
        
    Returns:
        dict: Success status and message
    """
    
    text_output = await musicService.delete_song(username, musicId, db)
    audio_output = await voiceService.speak_up(text_output["message"])
    return await handlingReturn.text_and_audio(audio_output,text_output["message"])

@router.post("/aiSuggestMusic/")
async def aiSuggestMusic(db = Depends(getMongoDB)):
    """
    Get AI-generated music suggestion using team. Keep track of the global_state of the team chat to avoid duplicating.
    """
    from infrastructure.socketio import client_states, global_sid
    print(client_states[global_sid])
    if client_states[global_sid] == "end":
       client_states[global_sid] = "start"
       text_output =  await recommendService.ai_suggest_music(db)
       audio_output = await voiceService.speak_up(text_output["message"])
       return await handlingReturn.text_and_audio(audio_output,text_output["message"])    

@router.post("/aiPickMusic/")
async def aiPickMusic(username: str, query: str, db = Depends(getMongoDB)):
    """
    Get AI-generated music pick from user's collection based on a query
    
    Args:
        username: Username to fetch music from
        query: Search query for music selection
        db: Database connection instance
        
    Returns:
        dict: Selected music details
    """
    
    text_output =  await recommendService.ai_pick_music(username,query,db)
    audio_output = await voiceService.speak_up(text_output["message"])
    return await handlingReturn.text_and_audio(audio_output,text_output["message"])

@router.post("/getRecord/")
async def get_record(audioFile: UploadFile = File(...),language: str = "en"):
    
   return await musicService.get_record(audioFile,language)