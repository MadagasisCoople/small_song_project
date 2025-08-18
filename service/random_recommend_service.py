# Music Recommendation Service Module
# Provides AI-powered music suggestions and picks based on user queries
import openai
import os
from dotenv import load_dotenv

class RecommendService:
    """
    Service class for handling music recommendations using OpenAI's GPT model
    Provides functionality for suggesting new music and picking from user's collection
    """

    load_dotenv()

    openai.api_key = os.getenv('OPENAI_API_KEY')

    async def ai_suggest_music(self, query: str):
        """
        Get AI-generated music suggestion based on user query
        
        Args:
            query: User's music preference or request
            
        Returns:
            str: Formatted string with suggested song
        """
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a helpful assistant that suggests one YouTube song for a user and response based on the user's query. You MUST give a relevent response that matches with the queries, NO randomness OR creative. When given a user's query, you MUST reply ONLY with a string in this exact format:\n\nYours '{query}' is matched with [song name]\n\nDo not explain or include code. Just output a single string in that format."},
                {"role": "user", "content": query}
            ]
        )

        _content_raw = response.choices[0].message.content or "i am dumb"

        return {"message": _content_raw}

    async def ai_pick_music(self, username: str, query: str, db):
        """
        Get AI-generated music pick from user's collection based on query
        
        Args:
            username: Username to fetch music from
            query: User's music preference or request
            db: Database connection instance
            
        Returns:
            str: Formatted string with picked song from user's collection
        """
        collection = db["users"]
        
        users = await collection.find_one({"userName":username})

        _music_name_list = [songName["userMusic"] for songName in users["userMusic"] if "userMusic" in songName]

        _song_name_list = "\n".join(f"-{name}" for name in _music_name_list)

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a music producer. Based on the user's music list produced by them, suggest a song from the list that matches with their queries. You MUST NOT include any explain or code, just a plain text. You MUST follow this format : Yours {query} is matched with (suggested song)"},
                {"role": "user", "content": f"The user's songs:\n{_song_name_list}\nNow suggest one that fits {query}"}
        ]
    )
        
        content_raw =  response.choices[0].message.content or " i am dumb "

        return {"message": content_raw}