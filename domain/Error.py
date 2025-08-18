from typing import Any, Dict
from typing_extensions import Annotated, Doc
from fastapi import HTTPException
print("Error module initialized")

# Custom error class for application-specific errors
class AppError(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

# Error class for conflicts (409 Conflict)
# Used when attempting creating an existing data
class conflictError(HTTPException):
    def __init__(self, detail: str ):
        super().__init__(status_code=409, detail= "Already got that "+ detail)

# Error class for not found (404 Not Found)
# Used when attempting to access a non-existent data
class notFoundError(HTTPException): 
    def __init__(self, detail: str):
        super().__init__(status_code=404, detail= "Unable to dig up that "+ detail)

# Error class for not enough ()
# Used when attempting to access a non-existent data
class notProcessableData(HTTPException): 
    def __init__(self, detail: str):
        super().__init__(status_code=422, detail= "Lack of "+detail)
        
# Error class for not allowed ()
# Used when attempting to access a non-usable data
class notAllowedTo(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=403, detail= "This is a banished "+detail)