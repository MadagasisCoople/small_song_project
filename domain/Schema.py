# Import required modules
from typing import Optional 
from pydantic import BaseModel, Field
from datetime import datetime
print("Schema module initialized")

# Data model for music entries
class Musics(BaseModel):
    userMusic: str          # The music identifier (e.g., YouTube URL/ID)
    userMusicId: Optional[int] = None  # Optional unique identifier for the music

# Data model for user accounts
class userNames(BaseModel):
    userId: int             # Unique identifier for the user
    userName: str           # User's username
    passWord: str           # User's password
    currentDate: datetime
    userMusic: Optional[list[Musics]] = []  # List of user's music entries
    musicShard: Optional[int]# MusicShard getting from bulding tree

# Data model for card game entries
class cardNames(BaseModel):
    cardId: str             # Unique identifier for the card
    cardName: str           # Name of the card
    power: int             # Base power level of the card
    specialPower: Optional[int]  # Optional special power level 

class musicPet(BaseModel):
    level: int #The number of day built
    poopPerDay: int #shard returning
    hp: Optional[int] #Will updated soon

class Images(BaseModel):
    userName: str
    fileName: str
    fileData: str

class CVEssence(BaseModel):
    name: str = Field(description="Segment 1: The name of the user")
    objective: str = Field(description="Segment 2: The objective of the user")
    skills: str = Field(description="Segment 3: The skills of the user")
    experience: str = Field(description="Segment 4: The title of the experiences of the user")
    education: str = Field(description="Segment 5: The title of the educational background of the user")
    email: str = Field(description="Segment 6: The email of the user")