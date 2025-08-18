import os
from pathlib import Path
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
from repositories.agent_repository import Agent
from autogen_agentchat.messages import StructuredMessage
from domain.Schema import CVEssence

agent = Agent()
class Extractor:
    def __init__(self,type):
        self.type = type

    async def run_agent(self,db):
        """
    Initializes and runs a team of agents for data extraction.

    Depending on the specified type, this function creates and configures
    agents to process data. For a "CV" type, it creates a data extractor
    and examiner agent, and arranges them into a team using a round-robin
    chat mechanism. The team is configured to process structured messages
    with a specified number of turns and a termination condition.

    Args:
        db: A database connection instance used to create agents.

    Returns:
        A RoundRobinGroupChat team composed of initialized agents.
        """

        if self.type == "CV":
            reader_agent = await agent.create_working_agent("data_extractor_CV", db)
            examine_agent = await agent.create_working_agent("data_examiner_CV", db)
        

        team = RoundRobinGroupChat(
            [reader_agent,examine_agent],
            custom_message_types=[StructuredMessage[CVEssence]],
            max_turns=2,
            termination_condition=TextMentionTermination("TERMINATE"),
            )
        return team
    
    async def extract_data (self, db):
        
        """
    Extracts data from real estate images using multi-modal messages.

    This asynchronous function verifies the existence of necessary directories and files,
    processes real estate images, and extracts relevant data. It first checks for a sample
    image file and ensures that the directory containing images to be processed exists.
    If images are present, it invokes a team of agents to perform data extraction, saves
    the results to a JSON file, and prints a preview of the extracted data.

    Args:
        db: A database connection instance used to create agents.

    Returns:
        None. The function prints logs of its progress and outputs data to a file.
        """

        print("=== Multi-Modal Real Estate Data Extractor Demo ===\n")
    
    # Check if sample image file exists
        if not os.path.exists("template_image.png"):
            print(f"Sample image file template_image.png not found.")
            print("Please ensure you have a labeled sample image with bounding boxes.")
            print("The sample image should show what real estate segments to extract and where they are located.")
            return
    
    # Check if images directory exists and has images
        if not os.path.exists("imageToCheck"):
            print(f"Creating imageToCheck directory...")
            os.makedirs("imageToCheck", exist_ok=True)
            print(f"Please add CV images to the imageToCheck directory and run this script again.")
            print("Supported formats: JPG, PNG, BMP, TIFF, WebP")
            return
    
    # Check if we have images to process
        from service.data_extractor_service  import get_image_files
        image_files = get_image_files()
    
        if not image_files:
            print(f"No image files found in directory.")
            print("Please add some real estate images and run this script again.")
            return
    
        print(f"Found {len(image_files)} images to process:")
        for img_file in image_files:
            print(f"  - {Path(img_file).name}")
    
        try:
            from service.data_extractor_service import run_team

            print("run team")

            # Run the extraction
            try:
                await run_team(self.type,db)
            except Exception as e:
                print(f"run_team() failed: {type(e).__name__}: {e}")
                return
        
            # Show a preview of the results
            if os.path.exists("extracted_data.json"):
                print(f"\n=== Extraction Complete ===")
                print("Results saved to: extracted_data")
            import json
            with open("extracted_data.json", 'r') as f:
                results = json.load(f)
            
            print(f"\nExtracted {len(results)} real estate records:")
            for i, result in enumerate(results[:3], 1):  # Show first 3 results
                print(f"  CV Segments:")
                print(f"    Name: {result['name']}")
                print(f"    Objective: {result['objective']}")
                print(f"    Skills: {result['skills']}")
                print(f"    Experience: {result['experience']}")
                print(f"    Education: {result['education']}")
                print(f"    Email: {result['email']}")
            
            if len(results) > 3:
                print(f"\n... and {len(results) - 3} more records")
        
        except Exception as e:
            print(f"Error during extraction: {e}")
            print("Please check your API key and internet connection.")
