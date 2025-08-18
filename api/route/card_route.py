# Card Route Module
# Handles all card game-related API endpoints including:
# - Card collection management
# - Card battles
# - Card statistics

from fastapi import APIRouter, Depends
from infrastructure.mongo_DB import getMongoDB
from service.card_service import CardService
from service.voice_service import VoiceService
from service.handling_return import HandlingReturn
from repositories.music_shard_repository import MusicShardRepository

router = APIRouter()

cardService = CardService()
voiceServices = VoiceService()
handlingReturn = HandlingReturn()
musicShardRepository = MusicShardRepository()

print("Card route initialized")

# Endpoint to add a new card to user's collection
@router.post("/addCard/")
async def add_card(userName: str, musicId: str, shardRequired: int, db = Depends(getMongoDB)):
    """
    Add a new card to user's collection
    
    Args:
        userName: Username of the card owner
        musicId: ID of the music to create card from
        
    Returns:
        dict: Success status and card details
    """

    text_output = await cardService.add_card(userName, musicId, shardRequired, db)
    
    audio_output= await voiceServices.speak_up(text_output["message"])
    return await handlingReturn.text_and_audio(audio_output,text_output["message"]+text_output["data"])


# Endpoint to remove a card from user's collection
@router.get("/removeCard/")
async def remove_card(userName: str, cardId: str, db = Depends(getMongoDB)):
    """
    Remove a card from user's collection
    
    Args:
        userName: Username of the card ownera
        cardId: ID of the card to remove
        
    Returns:
        dict: Success status and message
    """

    text_output = await cardService.remove_card(userName, cardId, db)
    audio_output =  await voiceServices.speak_up(text_output["message"]) 
    return await handlingReturn.text_and_audio(audio_output,text_output["message"])

# Endpoint to get all cards in user's collection
@router.get("/getAllUserCards/")
async def get_all_user_cards(userName: str, db = Depends(getMongoDB)):
    """
    Get all cards in user's collection
    
    Args:
        userName: Username to fetch cards for
        
    Returns:
        list: List of card documents
    """
    return await cardService.get_all_cards(userName, db)
    

# Endpoint to handle card battles between two users
@router.get("/battleCard/")
async def battle_cards(userName1: str, userName2: str, cardId1: str, cardId2: str, db = Depends(getMongoDB)):
    """
    Handle a card battle between two users
    
    Args:
        userName1: Username of first player
        userName2: Username of second player
        cardId1: Card ID of first player
        cardId2: Card ID of second player
        
    Returns:
        dict: Battle result and winner information
    """

    text_output =  await cardService.battle_cards(userName1, userName2, cardId1, cardId2, db)
    audio_output = await voiceServices.speak_up(" The result is ..."+ text_output["message"])
    return await handlingReturn.text_and_audio(audio_output,text_output["message"])
