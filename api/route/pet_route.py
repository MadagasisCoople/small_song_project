from fastapi import APIRouter,Depends
from infrastructure.mongo_DB import getMongoDB
from repositories.pet_repository import PetRepository
from repositories.checking_data_repository import CheckingDataRepository
from service.voice_service import VoiceService
from service.handling_return import HandlingReturn
router = APIRouter () 

petRepository = PetRepository()
checkingDatasRepository = CheckingDataRepository()
voiceService = VoiceService()
handlingReturn = HandlingReturn()
@router.post("/levelUp/")
async def levelUp(username:str, db = Depends(getMongoDB)):
    """
    Level up user's pet
    
    Args:
        username: Username of the pet owner
        
    Returns:
        dict: Updated pet details
    """
    
    text_output = await petRepository.level_up_pet(username,db)

    audio_output = await voiceService.speak_up(text_output["message"]) 
    
    return await handlingReturn.text_and_audio(audio_output,text_output["message"])   
