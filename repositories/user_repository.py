# User Repository Module
# Handles all user-related database operations including:
# - User account management (creation, verification)
# - Music collection management
# - User statistics and counts

from datetime import datetime
print("User repository initialized")


class UserRepository:

    async def add_user(self, username: str, password: str, db):

        """
        Adds a new user account to the database
        
        Args:
            username: Username for the new account
            password: Password for the new account
            db: Database connection instance
        
        Returns:
            dict: Success status, userId and userName
        """
        collection = db["users"]
        userId = await collection.count_documents({}) + 1

        new_user = {
            "userId" :userId,
            "userName" : username,
            "currentDate": datetime.now(),
            "passWord": password,
            "musicShard": 0
        }

        await collection.insert_one(new_user)
        return {
            "message":  f" The user with userId  {userId} and userName {username} has been created.",
            "userId": str(userId),
            "userName": username
        }

    async def delete_all(self, db):
        """
        Deletes all users from the database.

        Args:
            db: Database connection instance.

        Returns:
            dict: Message indicating successful deletion of all users.
        """

        collection = db["users"]
        await collection.delete_many({})
        return {"message": "All users deleted successfully"}

    async def delete_user(self, username: str, db):
        """
        Deletes a user account from the database.
        
        Args:
            username: Username of the account to delete
            db: Database connection instance
        
        Returns:
            dict: Message indicating successful deletion of the user
        """
        collection = db["users"]
        await collection.delete_one({"userName": username})
        return {"message": "User deleted successfully"}

    async def count(self, db):
        
        """
        Counts the total number of users in the database.

        Args:
            db: Database connection instance

        Returns:
            dict: Dictionary containing the user count
        """

        collection = db["users"]
        _user_count = await collection.count_documents({})
        return {"userCount": _user_count}

    async def checking(self, username: str, password: str, db):
        
        """
        Checks the given username and password against the database to authenticate the user.

        Args:
            username: Username to authenticate
            password: Password to authenticate
            db: Database connection instance

        Returns:
            dict: Success status and message, and user details if login successful
        """
        collection = db["users"]
        user = await collection.find_one({"userName": username, "passWord": password})
        if not user:
            return {"message": "Login failed"}
        return {
            "message": "Login successful",
            "userId": str(user["userId"]),
            "userName": user["userName"],
        }

    async def get_user_id(self, username: str, db):
        """
        Retrieves the user ID from the database based on the given username

        Args:
            username (str): Username to retrieve the ID for
            db: Database connection instance

        Returns:
            dict: Dictionary containing the user ID if found, otherwise None
        """
        collection = db["users"]
        user = await collection.find_one({"userName": username})
        return {"userId": str(user["userId"]) if user else None}

    async def update_date(self, username: str, db):

        """
        Updates the user's currentDate in the database and resets poopPerDay to 1 if the difference
        between the old and new dates is more than 1 day.

        Args:
            username (str): Username to update the date for
            db: Database connection instance

        Returns:
            str: A message indicating the time difference between the old and new dates
        """
        
        collection = db["users"]

        user = await collection.find_one({"userName": username})

        old_time = user["currentDate"]

        new_time = datetime.now()

        await collection.update_one(
            {"userName": username},
            {"$set": {"currentDate": new_time}}
        )

        time_diff = new_time - old_time

        if time_diff.days > 1:
            await collection.update_one(
                {"userName": username},
                {"$set": {"pet.0.poopPerDay": 1}}
            )

        return "You have a " + str(time_diff.days) + " diff day from the last signing!"
