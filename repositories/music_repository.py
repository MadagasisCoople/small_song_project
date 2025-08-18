# Music Repository Module
# Handles all music-related database operations including:
# - Music collection management
# - Music recommendations
# - Music selection based on preferences
import os
from typing import Optional
from dotenv import load_dotenv
from googleapiclient.discovery import build

class MusicRepository:
    """
    Repository class for handling music-related database operations
    """
    
    #initiating dotenv for api key
    load_dotenv()

    async def add_song(self, username: str, userMusic: str, db, required: Optional[str] = None):
        """
        Adds a new music entry to user's collection
        
        Args:
            username: Username of the user
            userMusic: Music identifier to add
            db: Database connection instance
            
        Returns:
            dict: Success status and message
        """
        youtube = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))

        request = youtube.search().list(
            q=userMusic,
            part="id",
            maxResults=1
        )
        
        response = request.execute()
        
        new_music = {
            "userMusic": userMusic,
            "musicId": response["items"][0]["id"]["videoId"],
        }

        if(required == "Do"):
            # Get the collection
            collection = db["users"]

            # Insert the new music entry into the user's collection
            await collection.update_one(
                {"userName": username},
                {"$push": {"userMusic": new_music}}
            )

        return {
            "message": f"Added successfully music with name: {userMusic} that has the id {response["items"][0]["id"]["videoId"]}",
            "musicId": str(response["items"][0]["id"]["videoId"])
        }

    async def get_all_song(self, username: str, db):
        
        """
        Retrieves all music entries for a specific user
        
        Args:
            username: Username to fetch music for
            db: Database connection instance
            
        Returns:
            list: List of music documents
        """
        
        collection = db["users"]
        cursor = collection.find({"userName": username}, {"_id": 0, "userMusic": 1, "userMusicId": 1})
        result = await cursor.to_list(length=None)
        return result

    async def delete_song(self, username: str, musicId: str, db):
        """
        Removes a music entry from user's collection
        
        Args:
            username: Username of the user
            musicId: Music identifier to remove
            db: Database connection instance
            
        Returns:
            dict: Success status and message
        """

        # Get the collection
        collection = db["users"]

        # Remove the music entry from the user's collection
        await collection.update_one(
            {"userName": username},
            {"$pull": {"userMusic": {"musicId": musicId}}}
        )

        # Return a success message
        return {"message": f"Succesfully deleted the song with name {musicId}"}
