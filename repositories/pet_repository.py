class PetRepository:

#Function to create the tree whenver an account is created
    async def pet_summoning(self, username: str, db):

        """
        Summon a pet for a given user

        Args:
            username (str): Username to validate
            db: Database connection instance

        Returns:
            dict: Updated pet details
        """
        collection = db["users"]

        new_pet = {
            "level": 1,
            "poopPerDay": 1,
        }

        await collection.update_one(
            {"userName": username},
            {"$push": {"pet": new_pet}}
        )

        return {
            "message": "pet summoned at level 1 with 1 poop",
            "petCreated": new_pet
        }
     
    # Levelling up the pet everyday the account is logged in
    async def level_up_pet(self, username: str, db):

        """
        Level up user's pet

        Args:
            username (str): Username to validate
            db: Database connection instance

        Returns:
            dict: Updated pet details
        """
        collection = db["users"]

        _levelling_pet = await collection.find_one(
            {"userName": username},
        )

        _levelPet = _levelling_pet["pet"][0]["level"]

        if _levelPet == 0:
            _updating_poop = 0

        await collection.update_one(
            {"userName": username},
            {"$inc": {"pet.0.level": 1, "pet.0.poopPerDay": 1}}
        )

        _current_levelling_pet = await collection.find_one(
            {"userName": username},
        )

        _current_level = _current_levelling_pet["pet"][0]["level"]

        _music_shard_gained = _current_levelling_pet["pet"][0]["poopPerDay"]

        return {
            "message": "Pet levelled up!",
            "level": _current_level,
            "shardGained": _music_shard_gained
        }

