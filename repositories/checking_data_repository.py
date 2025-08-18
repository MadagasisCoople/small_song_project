# Card Service Module
# Handles card game-related business logic and validation
import datetime
from domain.Error import conflictError, notFoundError, notProcessableData, notAllowedTo

class CheckingDataRepository:
    
    """
    Service class for handling card game-related operations
    Provides validation and business logic for card management and battles
    """

    async def card_exist(self, userName: str, cardId: str, db):
        """
        Validate card removal request
        
        Args:
            userName: Username to validate
            cardId: Card ID to remove
            db: Database connection instance
            
        Raises:
            userNameNotFoundError: If username doesn't exist
            cardNameNotFoundError: If card doesn't exist in user's collection
        """
        collection = db["users"]

        card = await collection.find_one({
            "userName": userName,
            "card.cardId": cardId
        })

        if not card: return False

        return True
    
    async def user_exist(self, userName: str,db):
        """
        Validate card retrieval request
        
        Args:
            userName: Username to validate
            db: Database connection instance
            
        Raises:
            userNameNotFoundError: If username doesn't exist
        """
        collection = db["users"]

        _card_user = await collection.find_one({
            "userName": userName
        })

        if not _card_user: return False

        return True
    
    async def music_exist(self, userName: str, musicId: str, db):
        """
        Validate card retrieval request
        
        Args:
            userName: Username to validate
            db: Database connection instance
            
        Raises:
            userNameNotFoundError: If username doesn't exist
        """
        collection = db["users"]
        
        _music_user = await collection.find_one({
            "userName": userName,
            "userMusic.musicId": musicId}
        )

        if not _music_user: return False

        return True

    async def battle_cards_exist(self, userName1: str, userName2: str, cardId1: str, cardId2: str, db):
        """
        Validate card battle request
        
        Args:
            userName1: Username of first player
            userName2: Username of second player
            cardId1: Card ID of first player
            cardId2: Card ID of second player
            db: Database connection instance
            
        Raises:
            cardNameNotFoundError: If either player's card doesn't exist
        """
        collection = db["users"]

        _card1 = await collection.find_one({
            "userName": userName1,
            "card.cardId": cardId1
            }
        )

        if not _card1: return False

        _card2 = await collection.find_one({
            "userName": userName2,
            "card.cardId" : cardId2
        })

        if not _card2: return False

        return True
            
    async def banned_card(self, userName: str, cardId: str, db):
        """
        Validate card removal request
        
        """
        collection = db["users"]

        card_user = await collection.find_one({
            "userName": userName,
            "bannedCard.cardId" : cardId},
        )
        
        if not card_user: return False

        return True

    async def checking_date(self, username:str, db):

        """
            Validate the user's date for potential actions in the system.

            This method checks if the current date matches or precedes the stored date for the user.
            It raises an exception if the date is older or if the date is the same, indicating a conflict.

    Args:
        username: Username to validate the date for.
        db: Database connection instance.

    Raises:
        notAllowedTo: If the stored date is in the future compared to the current date.
        conflictError: If the stored date is the same as the current date.
    
        Returns:
        True if the date is valid for proceeding.
        """

        collection = db["users"]
        
        user = await collection.find_one({"userName": username})

        old_time = user["currentDate"].date()

        new_time = datetime.datetime.now().date()

        if old_time > new_time:
            raise notAllowedTo(detail="date")

        if old_time == new_time:
            raise conflictError(detail="date")

        return True