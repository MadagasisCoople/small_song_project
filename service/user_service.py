from repositories.user_repository import UserRepository
from repositories.pet_repository import PetRepository
from repositories.checking_data_repository import CheckingDataRepository
from domain.Error import conflictError, notFoundError, notProcessableData, notAllowedTo

userRepository = UserRepository()
petRepository = PetRepository()
checkingDataRepository = CheckingDataRepository()

class UserService:
    async def add_user(self, username: str, password: str, db):
        _user_check = await checkingDataRepository.user_exist(username, db)

        if _user_check:
            raise conflictError(detail="user")
        
        _user_text = await userRepository.add_user(username, password, db)

        _pet_text = await petRepository.pet_summoning(username, db)

        return {"message": f"{_user_text["message"]} and also is the {_pet_text["message"]}"}
    
    async def delete_all(self, db):
        return await userRepository.delete_all(db)
    
    async def delete_user(self, username: str, db):
        _user_check = await checkingDataRepository.user_exist(username, db)

        if not _user_check:
            raise notFoundError(detail="user")
        
        return await userRepository.delete_user(username, db)
    
    async def count(self, db):
        return await userRepository.count(db)
    
    async def checking(self, username: str, password: str, db):
        _user_check = await checkingDataRepository.user_exist(username, db)

        if not _user_check:
            raise notFoundError(detail="user")
        
        return await userRepository.checking(username, password, db)
    
    async def get_user_id(self, username: str, db):
        _user_check = await checkingDataRepository.user_exist(username, db)

        if not _user_check:
            raise notFoundError(detail="user")

        return await userRepository.get_user_id(username, db)
    
    async def update_date(self, username: str, db):
        _user_check = await checkingDataRepository.user_exist(username, db)

        if not _user_check:
            raise notFoundError(detail="user")

        return await userRepository.update_date(username, db)
    