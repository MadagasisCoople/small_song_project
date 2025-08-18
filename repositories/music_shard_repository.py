from domain.Error import notProcessableData

class MusicShardRepository:
        
    async def add_music_shard(self, username: str, shardGained: int, db):

        """
        Increment music shard in user's profile by shardGained
        
        Args:
            username (str): Username to validate
            shardGained (int): Amount of shard to gain
            db: Database connection instance
        
        Returns:
            dict: Updated pet details
        """
        collection = db["users"] 

        await collection.update_one(
            {"userName":username},
            {"$inc":{"musicShard":shardGained}}
        ) 

        _current_levelling_pet = await collection.find_one(
               {"userName":username},
        )

        _current_level = _current_levelling_pet["pet"][0]["level"]

        _music_shard_gained = _current_levelling_pet["pet"][0]["poopPerDay"]

        _current_shard = _current_levelling_pet["musicShard"]

        return {
               "message": f"Pet levelled up! Currently, the level is {_current_level} and you have just obtained {_music_shard_gained} so, the current shard is {_current_shard}"
        }
    
    async def require_amount(self, userName: str, amount: int, db):
        """
        Validate if user has sufficient shards
        
        Args:
            userName: Username to validate
            amount: Amount of shards required
            db: Database connection instance
        
        Raises:
            notProcessableData: If user doesn't have sufficient shards
        """
        collection = db["users"]
        user = await collection.find_one({"userName": userName})
        
        if user["musicShard"] < amount:
            raise notProcessableData(detail="Shards")