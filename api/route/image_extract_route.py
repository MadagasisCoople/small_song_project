from fastapi import APIRouter, Depends
from domain.Schema import Images
from infrastructure.mongo_DB import getMongoDB
from service.image_service import ImageService
from service.voice_service import VoiceService
from service.handling_return import HandlingReturn

handlingReturn = HandlingReturn()
voiceService = VoiceService()
imageService = ImageService()

router = APIRouter()

@router.post("/store_image_file/")
async def store_image_file(username: str,image: Images ,db = Depends(getMongoDB)):
    print(username)
    return await imageService.store_image_file(username,image,db)