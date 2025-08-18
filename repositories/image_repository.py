import base64
import os
import uuid
from domain.Schema import Images
class ImageRepository:
    async def store_image_file(self,username: str,image: Images ,db):
        """
        Store an image file in the database

        Args:
            image: An `Images` object containing the image data
            db: A database connection instance

        Returns:
            A dictionary containing the message "Image from file {image.fileName} added Successfully"
        """
        collection = db["userImage"]
        _, b64data = image.fileData.split(",", 1)
        binary = base64.b64decode(b64data)
        imageDecoded =  {
            "userName" : image.userName,
            "fileName" : image.fileName,
            "fileData" : binary
        }
        await collection.insert_one(imageDecoded)
        await self.get_image_file(username,image.fileName,db)
        return {"message": f"Image from file {image.fileName} added Successfully"}
    
    async def get_image_file(self, userName:str, fileName:str , db):
        
        """
        Get an image file from the database

        Args:
            userName: Username of the image owner
            fileName: Name of the image file
            db: A database connection instance

        Returns:
            A dictionary containing the message "Image from file {fileName} was written to file Successfully" if the image was found, otherwise None
        """
        collection = db["userImage"]
        image = await collection.find_one({"userName": userName,"fileName": fileName})
        if not image:
            print("Image not found")
            return
        
        os.makedirs("imageToCheck", exist_ok=True)
        random_id = str(uuid.uuid4())

        file_path = os.path.join("imageToCheck", f"{random_id}.png")
        with open(file_path, "wb") as f:
            f.write(image["fileData"])
            return image["fileData"]
