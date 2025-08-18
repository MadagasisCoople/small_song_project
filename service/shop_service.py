from repositories.shop_repository import ShopRepository
from repositories.card_repository import CardRepository
from repositories.music_shard_repository import MusicShardRepository  
from repositories.checking_data_repository import CheckingDataRepository
from domain.Error import notFoundError, notAllowedTo, conflictError, notProcessableData

shopRepository = ShopRepository()
cardRepository = CardRepository()
musicShardRepository = MusicShardRepository()    
checkingDataRepository = CheckingDataRepository()

class ShopService:
    async def get_all_cards(self, userName: str, db):
        _user_check = await checkingDataRepository.user_exist(userName, db)
        if not _user_check: raise notFoundError(detail="user")
        return await shopRepository.get_all_cards(userName, db)
    
    async def buy_banished_card(self, userName : str, cardId : str, shardRequired : int, db):
        _user_check = await checkingDataRepository.user_exist(userName, db)
        if not _user_check: raise notFoundError(detail="user")
        _card_check = await checkingDataRepository.banned_card(userName, cardId, db)
        if not _card_check: raise notFoundError(detail="card")
        await musicShardRepository.require_amount(userName, shardRequired, db)
        return await shopRepository.buy_banished_card(userName, cardId, db)