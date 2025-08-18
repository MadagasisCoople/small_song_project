from contextlib import asynccontextmanager
from infrastructure.mongo_DB import MongoDB

@asynccontextmanager
async def lifeSpanConnect(app):
    print("Lifespan connect initialized")
    await MongoDB.connectMongo()
    await MongoDB.createCollection("users")
    await MongoDB.createCollection("userNameList")
    await MongoDB.createCollection("userImage")
    await MongoDB.createCollection("connectionSocket")
    app.state.db = MongoDB.db
    yield
    await MongoDB.closeMongo()
