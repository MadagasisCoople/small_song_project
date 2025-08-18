# Music Service Module
# Handles music-related business logic and validation
from io import BytesIO
from repositories.music_repository import MusicRepository
from repositories.checking_data_repository import CheckingDataRepository
from domain.Error import notFoundError, notAllowedTo, conflictError , notProcessableData
from fastapi import File, UploadFile
from service.voice_service import VoiceService

print("Music service initialized")

musicRepository = MusicRepository()
checkingDataRepository = CheckingDataRepository()
voiceService = VoiceService()

class MusicService:
    """
    Service class for handling music-related operations
    Provides validation and business logic for music management
    """

    async def add_song(self, username: str, userMusic: str, db):
        """
        Adds a new music entry to user's collection

        Args:
            username: Username of the user
            userMusic: Music identifier to add
            db: Database connection instance

        Returns:
            dict: Success status and message
        """

        _user_check = await checkingDataRepository.user_exist(username, db)

        if not _user_check:
            raise notFoundError(detail="user")

        _raw_data = await musicRepository.add_song(username, userMusic, db)
        
        _music_Id = _raw_data["musicId"]
        print(_music_Id)
        _music_check = await checkingDataRepository.music_exist(username, _music_Id, db)

        if _music_check:
            await musicRepository.delete_song(username, _music_Id, db)
            raise conflictError(detail="music")
        
        await musicRepository.add_song(username, userMusic, db,"Do")

        return {"message": f"Added successfully music with name: {userMusic}, {_music_Id}"}

    async def get_all_song(self, username: str, db):
        """
        Retrieves all music entries for a specific user

        Args:
            username: Username to fetch music for
            db: Database connection instance

        Returns:
            list: List of music documents
        """

        _user_check = await checkingDataRepository.user_exist(username, db)

        if not _user_check:
            raise notFoundError(detail="user")

        return await musicRepository.get_all_song(username, db)
    
    async def delete_song(self, username: str, musicId: str, db):
        """
        Removes a music entry from user's collection

        Args:
            username: Username of the user
            userMusic: Music identifier to remove
            db: Database connection instance

        Returns:
            dict: Success status and message
        """

        _user_check = await checkingDataRepository.user_exist(username, db)

        if not _user_check:
            raise notFoundError(detail="user")
        
        _music_check = await checkingDataRepository.music_exist(username, musicId, db)

        if not _music_check:
            raise notFoundError(detail="music")
        return await musicRepository.delete_song(username, musicId, db)
    
    async def get_record (self, audioFile: UploadFile = File(...), language: str = "en"):
        wav_bytes = await audioFile.read()
        text_output = await voiceService.speak_down(language, wav_bytes)
        audio_output = BytesIO(wav_bytes)
        return {
            "message": f"Added record succesfully",
            "text": text_output["message"],
            "audio": audio_output,}
    
