from pydantic import BaseModel, EmailStr
from typing import Union

class UserInCreate(BaseModel): # sign up
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    
class UserOutput(BaseModel): # output information back to the user
    id: int
    first_name: str
    last_name: str
    email: EmailStr

class UserInUpdate(BaseModel): # update any user's information
    id: int
    first_name: Union[str, None] = None # str | None
    last_name: Union[str, None] = None
    email: Union[EmailStr, None] = None
    password: Union[str, None] = None
    
class UserInLogin(BaseModel): # login
    email: EmailStr
    password: str

class UserWithToken(BaseModel): # send back to the user a token
    token: str