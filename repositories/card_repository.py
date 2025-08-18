from domain.Schema import cardNames, userNames, Musics
from googleapiclient.discovery import build
import math
import os
from dotenv import load_dotenv

class CardRepository:
    
    load_dotenv()

    async def add_card(self, userName: str, musicId: str, shardRequired: int, db):

        """
        Add a new card to user's collection
        
        Args:
            userName: Username to validate
            musicId: ID of the music to create card from
            shardRequired: Amount of shards required to create card
            db: Database connection instance
        Returns:
            dict: Success status and message
        Raises:
            notFoundError: If username doesn't exist
            conflictError: If card already exists in user's collection
            notProcessableData: If shard amount is not sufficient
        """
        collection = db["users"]

        # setup youtube and search song
        youtube = build("youtube", "v3",
                        developerKey=os.getenv("YOUTUBE_API_KEY"))
        request = youtube.videos().list(
            id=musicId,
            part="snippet,statistics"
        )

        response = request.execute()

        # Data getting for card
        _view_count = int(response["items"][0]["statistics"].get("viewCount", 0))
        _like_count = int(response["items"][0]["statistics"].get("likeCount", 0))
        _comment_count = int(response["items"][0]["statistics"].get("commentCount", 0)) # Extra power for commentCount

        if _view_count < 1000:
            return {"message":"Your shjtty video is piece of trash"}

        if _comment_count <= 10000:
            _comment_score = _comment_count
        else:
            _comment_score = 10000 + (_comment_count - 10000) ** 0.5  # or use other smooth formulas above

        _max_view_reward = 10000
        _view_reward = min(math.log10(_view_count + 1) * 2000, _max_view_reward)    
        _power = round(_like_count/_view_count * 1000000 + _comment_score + _view_reward,0)
        _power = max(10, _power)
        while _power>100: 
            _power = _power/10
        _power = math.ceil(_power)
         
        _card_name = response["items"][0]["snippet"]["title"]
        # creating new card
        _new_card = {
            "cardId": musicId,
            "cardName": _card_name,
            "power": _power,
            "specialPower": _comment_count
        }

        # Adding a new card
        await collection.update_one(
            {"userName": userName},
            {"$push": {"card": _new_card}}
        )

        collection.update_one(
            {"userName": userName},
            {"$inc": {"musicShard":-shardRequired}}
            )

        # return values
        return {
            "message": f"The card with the name {_card_name} and the power {_power} has been added to your collection. Well done!",
            "data": f"View count {_view_count} and likeCount {_like_count}  and specialPower {_comment_count}",
        }

    async def remove_card(self, userName: str, cardId: str, db):
        """
        Remove a card from user's collection

        Args:
            userName: Username to validate
            cardId: Card ID to remove
            db: Database connection instance

        Raises:
            notFoundError: If username doesn't exist
            notFoundError: If card doesn't exist in user's collection
        """

        collection = db["users"]
        await collection.update_one(
            {"userName": userName},
            {"$pull": {"card": {"cardId": cardId}}}
        )
        return{
            "message": f"The card with the name {cardId} has been deleted from your collection. Well done!",
        }
    
    async def get_all_cards(self, userName:str, db):
        """
        Get all cards in user's collection

        Args:
            userName: Username to validate
            db: Database connection instance

        Returns:
            list: List of card documents
        """
        collection = db["users"]
        cursor = collection.find(
            {"userName": userName},
            {"card": 1, "_id": 0}
        )
        result = await cursor.to_list(length = None)
        return result
    
    async def battle_cards(self, userName1:str, userName2:str, cardId1: str, cardId2: str, db):

        """
        Handle a card battle between two users

        Args:
            userName1: Username of first player
            userName2: Username of second player
            cardId1: Card ID of first player
            cardId2: Card ID of second player
            db: Database connection instance

        Returns:
            dict: Battle result and winner information
        """
        
        collection =  db["users"]

        user_1_card_raw_power = await collection.find_one({
            "userName":userName1,
            "card.cardId": cardId1
            },{"card.$":1}
        )
        
        user_2_card_raw_power = await collection.find_one({
            "userName":userName2,
            "card.cardId": cardId2
            },{"card.$":1}
        )

        user_1_card_power = user_1_card_raw_power["card"][0]["power"]
        user_2_card_power = user_2_card_raw_power["card"][0]["power"]

        if user_1_card_power > user_2_card_power:
            return {
                "user1CardPower":user_1_card_power,
                "user2CardPower":user_2_card_power,
                "message":"Well done!Player 1... Won!"
            }
                
        if user_1_card_power < user_2_card_power:
            return {
                "user1CardPower":user_1_card_power,
                "user2CardPower":user_2_card_power,
                "message":"Well done!Player 2... Won!"
            }
        
        else:
            return { "message": "Well! What a pity~~ A draw"}
        
    async def ban_card(self, userName: str, cardId: str, db):
        
        """
    Ban a card from a user's collection.

    Args:
        userName: The username of the card owner.
        cardId: The ID of the card to be banned.
        db: The database connection instance.

    Returns:
        dict: A confirmation message indicating the card has been banned.

    This function retrieves the specified card from the user's collection,
    removes it from the active card list, and adds it to the banished card list.
        """

        collection = db["users"]
        
        card_target = await collection.find_one(
            {"userName": userName,"card.cardId":cardId},
            {"card":{"$elemMatch": {"cardId": cardId}}})
        
        card_to_move = card_target["card"][0]

        print("Pushing:", card_to_move)

        await collection.update_one(
            {"userName": userName},
            {"$pull": {"card":{"cardId" : cardId}}}
        )

        await collection.update_one(
            {"userName":userName},
            {"$push": {"banishedCard": card_to_move}}
        )

        return{
            "message": f"The card with the cardId {cardId} has been banned from your collection. Sorry!",
        }