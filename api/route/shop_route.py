from service.shop_service import ShopService
from service.card_service import CardService
from service.voice_service import VoiceService
from service.handling_return import HandlingReturn
from fastapi import Depends, APIRouter
from infrastructure.mongo_DB import getMongoDB

router = APIRouter()

cardService = CardService()
shopService = ShopService()
voiceService = VoiceService()
handlingReturn = HandlingReturn()

@router.get("/getAllBanishedCard/")
async def getAllBanishedCard(userName: str, db = Depends(getMongoDB)):
    """
    Get all banished cards for a given user
    
    Args:
        userName: Username of the user to fetch banished cards for
        
    Returns:
        list: List of banished card documents
    """
    return await shopService.get_all_cards(userName, db)

@router.get("/buyBanishedCard/")
async def buyBanishedCard(userName: str, cardId: str, shardRequired: int, db = Depends(getMongoDB)):
    """
    Buy a banished card for a given user
    
    Args:
        userName: Username of the user to buy the card for
        cardId: Card ID of the card to buy
        
    Returns:
        dict: Success status and message
    """

    text_output = await shopService.buy_banished_card(userName, cardId,shardRequired, db)
    await cardService.add_card(userName, cardId, shardRequired, db)
    audio_output = await voiceService.speak_up(text_output["message"])  
    return await handlingReturn.text_and_audio(audio_output,text_output["message"])  