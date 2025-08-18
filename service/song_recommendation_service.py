from datetime import datetime
from autogen_core import SingleThreadedAgentRuntime
from service.voice_service import VoiceService
from googleapiclient.discovery import build
from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_agentchat.teams import RoundRobinGroupChat, SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_agentchat.conditions import TextMentionTermination
import os
import json

from repositories.agent_repository import Agent
from repositories.emotional_repository import EmotionalIssue
from service.console_sub_service import ConsoleSub
from infrastructure.model_cilent import ModelCilent
from dotenv import load_dotenv
load_dotenv()
voiceService = VoiceService()
modelCilent = ModelCilent()

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY") or ""
OPEN_AI_KEY = os.environ.get("OPENAI_API_KEY") or ""

agent = Agent()

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()  # Or str(obj)
        return super().default(obj)
    
class SongRecommender:
    def __init__(self,model_cilent: OpenAIChatCompletionClient):
        self.model_client = model_cilent

    async def get_song_recommendations(self, db, n=5):
        """
    Get a list of song recommendations based on a user's emotional state.

    The user's emotional state is determined by a chat with a mood reader AI.
    The AI is given the user's past emotional issues, and from that, it
    determines the user's current emotional state.
    The AI then recommends a list of songs based on the user's emotional state.
    The user can then give feedback to the AI on the recommended songs, and
    the AI will revise the list based on the feedback.
    The user can continue to give feedback until they are satisfied with the
    recommended songs.

    Args:
        n (int): The number of song recommendations to return.

    Returns:
        A list of song recommendations.
        """

        # Get emotional history and other user's data
        collection = db["userNameList"]
        emotional_issue = EmotionalIssue(collection)
        issue_history = emotional_issue.get_user_issues("user_default")

        # Initialize the agents 
        # song agents
        mood_agent = await agent.create_working_agent("mood_reader",db) 
        song_agent = await agent.create_working_agent("song_recommender",db)
        critic_agent = await agent.create_working_agent("song_critic",db)

        # emotion agents
        issue_agent= await agent.create_working_agent("Ms_Robin",db)
        issue_agent_assistant = await agent.create_working_agent("Mr_Madagas",db)
        user_proxy_agent = UserProxyAgent("user_proxy", input_func = lambda _: input(""))

        # Initialize the termination conditions
        text_termination_song = TextMentionTermination(text="PERFECT")

        # Intialize the selector_prompt
        selector = """
Select an agent to perform the task.
{roles}
Conversation history:

{history}

Select an agent from {participants} to perform the next task based on these instructions:
The flow should be issue_agent asks the user_proxy_agents till, the user said "I want songs" then, mood_reader then end with calling song_recommender followed by song_critic till song_critic said "Perfect"
The issue_assistant_agent will ONLY RUN when issue_agent said "HELP ME DARLING"
After the mood_reader ran, ALWAYS CALL SONG_RECOMMENDER after
After the song_recommender run, ALWAYS CALL SONG_CRITIC after it
Never run issue_agents again after mood_reader, song_recommender or song_critic
Only one agent should act at a time.
"""

        # Run the teams with tasks
        tasks = f"""
Get ready. The patient is coming now. Treat them carefully. 
Remember to give them a heart warming greeting!
As well as a welcoming introduction of yourself
Remember! Focus on read their emotion instead of suggest them a solution
Here is the patient's past issue:
Emotional history: {issue_history}
"""
        
        # Initialize the team
        team = SelectorGroupChat(
            [issue_agent,  user_proxy_agent, mood_agent, issue_agent_assistant, song_agent, critic_agent],
            model_client=self.model_client,
            selector_prompt=selector,
            termination_condition=text_termination_song,
            max_selector_attempts=5,
        )

        console_sub = ConsoleSub()
       
        while True:
            result = await console_sub.run(
                team.run_stream(task=tasks),
                output_stats=True,)

            if hasattr(result, 'messages') and result.messages:
                user_prompt = input("Give me your feedback: (or 'thanks' to quit): ")    
                if user_prompt.lower().strip() == "thanks":
                    break
            tasks = f"Revise your previous list based on this feedback: {user_prompt}."

        # Extract the song recommendations list
        response = ""

        state = await team.save_state()
        with open("agent_state.json", "w") as f:
            json.dump(state, f, indent=4, cls=DateTimeEncoder)

        if hasattr(result, "messages") and result.messages:
            for msg in reversed(result.messages):
                source = getattr(msg, "source", None)
                if source == "song_recommender":
                    content = getattr(msg, "content", None)
                    if isinstance(content, str):
                        response = content
                        break
            else:
                response = str(result.messages[-1])

        songs = [line.strip() for line in response.split("\n") if line.strip()]
        return songs[:n] # alist of n songs

    @classmethod
    async def get_youtube_link(cls, song_name: str):
        print(song_name)
        """
        Retrieve a YouTube link for a given song name.

        This function uses the YouTube Data API to search for a video matching
        the specified song name and returns the URL of the video if found.
        If no video is found or an error occurs, an appropriate message is returned.

        Args:
            song_name (str): The name of the song to search for on YouTube.

        Returns:
            str: A YouTube link for the song or an error message if not found or an error occurs.
        """

        if not YOUTUBE_API_KEY:
            return None
        try:
            youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
            request = youtube.search().list(
                q=song_name, part="snippet", type="video", maxResults=1
            )
            response = request.execute()
            items = response.get("items", [])
            if items:
                video_id = items[0]["id"]["videoId"]
                return f"https://www.youtube.com/watch?v={video_id}"
            return f"No link was found for the song {song_name}"
        except Exception as e:
            return f"Could not fetch YouTube link due to network error: {e}"

    async def runRecommendService(self,db):

        """
        Run the song recommendation system.

        This function runs the song recommendation system which:
            1. Asks the user for their emotional state
            2. Retrieves a list of recommended songs based on the user's emotional state
            3. Prints the recommended songs
            4. Retrieves a YouTube link for each of the recommended songs
            5. Prints the YouTube links for the recommended songs
        """
        recommended_songs = await self.get_song_recommendations(db)
        for idx, song in enumerate(recommended_songs, 1):
            print(f"{idx}. {song}")
            youtube_link = await self.get_youtube_link(song)
            if youtube_link:
                print(f"YouTube: {youtube_link}")
        await self.model_client.close()

