from repositories.pet_repository import PetRepository
from repositories.checking_data_repository import CheckingDataRepository
from repositories.user_repository import UserRepository
from repositories.music_shard_repository import MusicShardRepository
petRepository = PetRepository()
checkingDataRepository = CheckingDataRepository()
userRepository = UserRepository()
musicShardRepository = MusicShardRepository()


class PetService:
    async def pet_summoning(self, username: str, db):
        """
        Summon a pet for a given user

        Args:
            username (str): Username to validate
            db: Database connection instance

        Returns:
            dict: Updated pet details
        """
        return await petRepository.pet_summoning(username, db)

    async def level_up_pet(self, username: str, db):
        """

        Level up the user's pet and update related data.

        This function checks the user's date for potential actions, updates the user's date
        in the database, levels up the user's pet, and adds music shards based on the pet's
        new level.

        Args:
            username (str): Username to validate
            db: Database connection instance

        Returns:
            dict: Updated details including a message about the pet levelling up and the current shard count.
        """

        await checkingDataRepository.checking_date(username, db)
        await userRepository.update_date(username, db)
        shards_gained = await petRepository.level_up_pet(username, db)
        return await musicShardRepository.add_music_shard(username, shards_gained["shardGained"], db)
