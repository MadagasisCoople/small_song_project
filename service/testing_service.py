import asyncio
from infrastructure.mongo_DB import getMongoDB
from infrastructure.model_cilent import ModelCilent
from service.song_recommendation_service import SongRecommender  # Update path if different
from service.main_extractor_service import Extractor

modelCilent = ModelCilent()


# async def test():
#     db = getMongoDB()
#     extractor = Extractor("CV")
#     await extractor.extract_data(db)

# if __name__ == "__main__":
#     asyncio.run(test())

async def test():
    db = getMongoDB()
    
    # Initialize and run the SongRecommender
    model_cilent = modelCilent.generate_cilent("o4-mini")
    recommender = SongRecommender(model_cilent)
    await recommender.runRecommendService(db)

if __name__ == "__main__":
    asyncio.run(test())
