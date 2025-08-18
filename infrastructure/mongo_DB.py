# MongoDB database connection and operations module
from motor.motor_asyncio import AsyncIOMotorClient

class MongoDB:
    """
    MongoDB database connection handler class
    Manages database connections and provides methods for database operations
    """
    def __init__(self):
        # Initialize connection to local MongoDB instance
        self.connection_string = "mongodb://localhost:27017"
        self.client = AsyncIOMotorClient(self.connection_string)
        self.db = self.client.fpt
        
    def get_db(self):
        """Returns the database instance"""
        return self.db

    @classmethod
    async def connectMongo(cls) -> None:
        """
        Establishes connection to MongoDB in Docker environment
        Uses host.docker.internal to connect to host machine's MongoDB
        """
        cls.client = AsyncIOMotorClient("mongodb://localhost:27017")
        cls.db = cls.client["fpt"]

    @classmethod
    async def closeMongo(cls) -> None:
        """Closes the MongoDB connection"""
        cls.client.close()

    @classmethod
    async def createCollection(cls, collection_name: str) -> None:
        """
        Creates a new collection in the database if it doesn't exist
        
        Args:
            collection_name: Name of the collection to create
            
        Raises:
            ValueError: If database connection is not established
        """
        if cls.db is not None:
            # Check if collection exists before creating it
            collections = await cls.db.list_collection_names()
            if collection_name not in collections:
                await cls.db.create_collection(collection_name)
        else:
            raise ValueError("Database connection is not established.")
        
def getMongoDB():
    """
    Returns the database instance if connection is established
    
    Returns:
        Database instance
        
    Raises:
        ValueError: If database connection is not established
    """
    db_instance = MongoDB()
    return db_instance.get_db()