import json
from pathlib import Path
import re
from PIL import Image
from domain.Schema import CVEssence
from autogen_agentchat.messages import MultiModalMessage
from autogen_core import Image as AutogenImage
from autogen_agentchat.ui import Console
# from voiceService import VoiceService
from service.main_extractor_service import Extractor
from dotenv import load_dotenv
from service.image_service import ImageService

# voiceService = VoiceService()
imageService = ImageService()
load_dotenv()

directory = Path("imageToCheck")
sample_file = Path("template_image.png")
output_file = Path("extracted_data.json") 

def load_sample_image():        
        """
        Loads the sample image from the file system.

        Returns:
            An AutogenImage instance of the sample image.

        Raises:
            FileNotFoundError: If the sample image file is not found.
            Exception: If there is an error loading the sample image.
        """
        try:
            pil_image = Image.open(sample_file)
            return AutogenImage(pil_image)
        except FileNotFoundError:
            raise FileNotFoundError(f"Sample image file {sample_file} not found.")
        except Exception as e:
            raise Exception(f"Error loading sample image {sample_file}: {e}")
        
def get_image_files():
        """
        Gets a list of image files in the imageToCheck directory.

        Returns:
            A list of image files, sorted alphabetically.
        """
        image_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        image_files = []
    
        for file_path in Path(directory).rglob('*'):
            if file_path.suffix.lower() in image_extensions:
                image_files.append(str(file_path))
    
        return sorted(image_files)

async def run_team(request: str, db):

    """
    Runs a team of agents to process and extract data from images.

    This function uses a pre-defined extractor and a team of agents to analyze images
    located in a specified directory. It first ensures that a sample image is loaded,
    then it processes each image found in the directory, extracts relevant data using 
    multi-modal messages, and saves the extracted data to a JSON file.

    Args:
        request (str): The request type for the extractor.
        db: A database connection instance used to create agents.

    Returns:
        None. The function prints logs of its progress and saves extracted data to a file.
    """

    extractor = Extractor(request)
    
    team = await extractor.run_agent(db)
    
    try:
        sample_image = load_sample_image()
        print("Loaded sample image: template_image.png")
    except Exception as e:
        print(f"Error loading sample image: {e}")
        return
    
    # Get image files to process
    image_files = get_image_files()
    
    if not image_files:
        print(f"No image files found in {"imageToCheck"}")
        return
    
    print(f"Found {len(image_files)} images to process")
    print(f"Using sample image: template_image.png")
    
    extracted_data_list = []
        
    for i, image_path in enumerate(image_files, 1):
        
        print(f"Processing image {i}/{len(image_files)}: {Path(image_path).name}")

        try: 
             # Load and prepare the image to process
            pil_image = Image.open(image_path)
            image = AutogenImage(pil_image)

            # Create multi-modal message with sample image, target image, and instructions
            image_message = MultiModalMessage(
                content=[
                """
Please analyze the data from the image below and use it to extract data from the image after
                    """,
                    sample_image,  # The labeled sample image with bounding boxes
                    image  # The target image to process
                ],
                source="user"
            )
            
            # Process with the team
            result = await Console(
                team.run_stream(task=image_message),
                output_stats=True,
            )

            for msg in reversed(result.messages):
                content = getattr(msg, "content", None)
                if hasattr(msg, 'content') and isinstance(content, CVEssence):
                    extracted_data_list.append(content)
                    print(f"Extracted data of: {content.name},")
                
                passed_status = None
                if hasattr(msg, "content") and isinstance(content, str):
                    match = re.search(r'"?([A-Za-z]+)"?\s*:\s*TERMINATE', content)
                    if match:
                        passed_status = match.group(1).upper()  # e.g., "PASSED"
            
        except Exception as e:
            print(f"Error processing image {image_path}: {e}")
            continue
     # Save all extracted data
    if extracted_data_list:
        # Convert Pydantic models to dictionaries and save
        data_dict = [item.model_dump() for item in extracted_data_list]
        output_data = {
            "results": data_dict,
            "status": passed_status,
        }
        with open("extracted_data.json", 'w') as f:
            json.dump(output_data, f, indent=2)
        print(f"Successfully saved {len(extracted_data_list)} extracted records to extracted_data.json")
    else:
        print("No data was extracted successfully.")