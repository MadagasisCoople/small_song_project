from repositories.checking_data_repository import CheckingDataRepository
from repositories.card_repository import CardRepository
from repositories.casino_repository import CasinoRepository
from repositories.music_shard_repository import MusicShardRepository
from domain.Error import conflictError, notFoundError, notProcessableData, notAllowedTo
import openai
import os
from dotenv import load_dotenv

checkingDataRepository = CheckingDataRepository()
cardRepository = CardRepository()
musicShardRepository = MusicShardRepository()
casinoRepository = CasinoRepository()

class CasinoService:

    """
    Casino service. A small web game for playing with theirs cards and may also lose their cards.

    """

    load_dotenv()

    openai.api_key = os.getenv('OPENAI_API_KEY')

    async def handle_result(self, userName: str, cardId: str, guess : str, db):

        _user_check = await checkingDataRepository.user_exist(userName,db) 

        if not _user_check: raise notFoundError(detail="user")

        _card_check = await checkingDataRepository.card_exist(userName, cardId, db)
        
        if not _card_check: raise notFoundError(detail="card")

        _ban_card_check = await checkingDataRepository.banned_card(userName, cardId, db)
        
        if _ban_card_check: raise notAllowedTo(detail="card")

        raw_result = await casinoRepository.get_result_higher_lower(userName, cardId, guess, db)
        
        result = raw_result["message"]

        number_picked = raw_result["number"]

        re_act = ""
        
        if result == "Lose":
            await cardRepository.ban_card(userName, cardId, db)
            re_act = ". Every victory requires a sacrifice right. Losing your precious card ,but you are still able to raise from the ashe, no?"

        elif result == "Won":
            await musicShardRepository.add_music_shard(userName, 80, db)
            re_act = ". Here is 80 music shards as a little reward for your bravery!."

        elif result == "Jackpot":
            await musicShardRepository.add_music_shard(userName, 10100, db)
            re_act = ". Mind, mind got a lucky cup here! Surely enough to fullfill your wish of wealthiness. Here, take this 10000 music shards and a free card as my compliment!"

        exclaimination = await self.exclaimination(result)

        textOutput = exclaimination["message"] + re_act + " As the result is " + str(number_picked)

        return{
            "message": textOutput 
        }

    async def exclaimination(self, result: str):

        query = "The result is " + result + ". Show me your response."

        response = openai.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": f"You are a glamorous, cheeky casino card dealer. You speak with flair and confidence. "
                 "When you got the result, you ALWAYS respond with a dramatic one-liner to mock them when lose or say something flirty"
                 "when they won or hit a jackpot like what a casino dealer would say. "
                 "Generating a related response to the result and try to sound like a charming female casino dealer as much as possible."
                 "Your response must be in this format exactly:"
                 "[A fun or flirty one-liner][Your response on their result]"
                 "Do NOT explain your reasoning. Do NOT include code. Do NOT repeate the query. Just say the line and your response."
                 "Example: Hehehe luck is part of skill yeah? Congratulations!That wild move brings you a game~~~"
                 ""},
                {"role": "user", "content": query}]
        )

        # Extract the response
        contentRaw = response.choices[0].message.content or "i am dumb"

        return {"message": contentRaw}


    