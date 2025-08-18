class ShopRepository:
    async def get_all_cards(self,userName: str, db):
        collection = db["users"]
        cursor = collection.find(
            {"userName": userName},
            {"_id": 0, "bannedCard": 1}
        )
        result = await cursor.to_list(length = None)
        return result
    
    async def buy_banished_card(self, userName:str ,cardId: str, db):
        collection = db["users"]
        await collection.update_one(
            {"userName":userName},
            {"$pull":{"bannedCard":{"cardId":cardId}}}
        )
        return {"message": "Banished Card Purchased Successfully"}