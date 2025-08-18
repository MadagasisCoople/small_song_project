from repositories.checking_data_repository import CheckingDataRepository
from repositories.card_repository import CardRepository
from repositories.music_shard_repository import MusicShardRepository
from domain.Error import conflictError, notFoundError, notProcessableData, notAllowedTo

checkingDataRepository = CheckingDataRepository()
cardRepository = CardRepository()
musicShardRepository = MusicShardRepository()

class CardService:
    async def add_card(self, userName: str, musicId: str, shardRequired: int, db):
        """
        Add a new card to user's collection

        Args:
            userName: Username to validate
            musicId: ID of the music to create card from
            shardRequired: Amount of shards required to create card
            db: Database connection instance

        Raises:
            notFoundError: If username doesn't exist
            conflictError: If card already exists in user's collection
            notProcessableData: If shard amount is not sufficient
        """
        _user_check = await checkingDataRepository.user_exist(userName, db)
        if not _user_check:
            raise notFoundError(detail="user")
        _card_check = await checkingDataRepository.card_exist(userName, musicId, db)
        if _card_check:
            raise conflictError(detail="card")
        _ban_card_check = await checkingDataRepository.banned_card(userName, musicId, db)
        if _ban_card_check:
            raise notAllowedTo(detail="card")
        await musicShardRepository.require_amount(userName, 150, db)
        return await cardRepository.add_card(userName, musicId, shardRequired, db)
    
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
        _user_check = await checkingDataRepository.user_exist(userName, db)
        if not _user_check:
            raise notFoundError(detail="user")
        _card_check = await checkingDataRepository.card_exist(userName, cardId, db)
        if not _card_check:
            raise notFoundError(detail="card")
        return await cardRepository.remove_card(userName, cardId, db)
    
    async def get_all_cards(self, userName: str, db):
        """
        Get all cards in user's collection

        Args:
            userName: Username to validate
            db: Database connection instance

        Raises:
            notFoundError: If username doesn't exist
        """
        _user_check = await checkingDataRepository.user_exist(userName, db)
        if not _user_check:
            raise notFoundError(detail="user")
        return await cardRepository.get_all_cards(userName, db)
    
    async def battle_cards(self, userName1: str, userName2: str, cardId1: str, cardId2: str, db):
        _user_check1 = await checkingDataRepository.user_exist(userName1, db)
        if not _user_check1:
            raise notFoundError(detail="user1")
        _user_check2 = await checkingDataRepository.user_exist(userName2, db)
        if not _user_check2:
            raise notFoundError(detail="user2")
        _card_check1 = await checkingDataRepository.card_exist(userName1, cardId1, db)
        if not _card_check1:
            raise notFoundError(detail="card1")
        _card_check2 = await checkingDataRepository.card_exist(userName2, cardId2, db)
        if not _card_check2:
            raise notFoundError(detail="card2")
        return await cardRepository.battle_cards(userName1, userName2, cardId1, cardId2, db)