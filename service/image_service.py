from repositories.image_repository import ImageRepository
from repositories.checking_data_repository import CheckingDataRepository
from domain.Error import notFoundError
from domain.Schema import Images

imageRepository = ImageRepository()
checkingDataRepository = CheckingDataRepository()


class ImageService:
    async def store_image_file(self, username: str, image: Images, db):
        """
        Store an image file in the database for a specific user.

        This function checks if the user exists in the database before storing the image file.
        If the user does not exist, it raises a notFoundError.

        Args:
            username: Username of the user storing the image.
            image: An `Images` object containing the image data.
            db: A database connection instance.

            Returns:
            A dictionary containing a success message after the image is stored.
        """

        _user_check = await checkingDataRepository.user_exist(image.userName, db)
        if not _user_check:
            raise notFoundError(detail="user")
        return await imageRepository.store_image_file(username,image, db)

    async def get_image_file(self, userName: str, fileName: str, db):
        """
        Get an image file from the database

        Args:
            userName: Username of the image owner
            fileName: Name of the image file
            db: A database connection instance

        Returns:
            A dictionary containing the message "Image from file {fileName} was written to file Successfully" if the image was found, otherwise None
        """
        _user_check = await checkingDataRepository.user_exist(userName, db)
        if not _user_check:
            raise notFoundError(detail="user")
        return await imageRepository.get_image_file(userName, fileName, db)
