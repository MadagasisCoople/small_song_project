from random import randint
from repositories.card_repository import CardRepository
from repositories.user_repository import UserRepository
from repositories.music_shard_repository import MusicShardRepository    

cardRepository = CardRepository()
userRepository = UserRepository()
musicShardRepository = MusicShardRepository()

class CasinoRepository:
    async def get_result_higher_lower(self, userName: str, cardId: str, guess: str, db):

        """
        Get result of higher or lower game
        
        Args:
            userName: Username of the player
            cardId: Card ID of the player
            guess: Guess of the player
            db: Database connection instance
        
        Returns:
            dict: Result of the game and the number picked
        """
        
        collection = db["users"]

        user = await collection.find_one(
            {"userName": userName, "card.cardId": cardId},
            {"card": {"$elemMatch": {"cardId": cardId}}}
        )

        if not user:
            raise ValueError("User or card not found")

        user_power = user["card"][0]["power"]        

        random_picked = randint(user_power - 50, 50+user_power)

        result = ""

       # Caculating result
        if (random_picked > user_power and guess == "Lower") or (random_picked < user_power and guess == "Higher"):
          result = "Won"

        elif random_picked == user_power and guess == "Same":
            result = "Jackpot"

        else:
            result = "Lose"

        return {
            "message": result,
            "number": random_picked
        }