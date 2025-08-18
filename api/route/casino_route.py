from fastapi import APIRouter, Depends
from infrastructure.mongo_DB import getMongoDB
from service.casino_service import CasinoService
from service.voice_service import VoiceService
from service.handling_return import HandlingReturn

handlingReturn = HandlingReturn()
voiceService = VoiceService()
casinoService = CasinoService()
casinoService = CasinoService()

router = APIRouter()

@router.post("/higherOrLower/")
async def higherOrLower(userName: str, cardId: str, guess: str, db = Depends(getMongoDB)):
    textOutput = await casinoService.handle_result(userName, cardId, guess, db = db)
    audio_output = await voiceService.speak_up(textOutput["message"])
    return await handlingReturn.text_and_audio(audio_output,textOutput["message"])