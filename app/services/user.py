from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.user import UserRepository
from app.schemas.user import UserOutput, UserInCreate, UserInLogin, UserWithToken
from app.utils.auth import verify_password, get_password_hash, sign_jwt, decode_jwt

class UserService:
    def __init__(self, session: Session):
        self.__user_repository = UserRepository(session=session)
    
    def signup(self, user_data: UserInCreate) -> UserOutput:
        # check if email of user already exists or not
        if self.__user_repository.user_exist_by_email(email=user_data.email):
            raise HTTPException(status_code=400, detail="Email already exists")
        # hash password
        hashed_password = get_password_hash(plain_password=user_data.password)
        user_data.password = hashed_password
        
        # create new user and save into db
        return self.__user_repository.create_user(user_data=user_data)
    
    def login(self, login_data: UserInLogin) -> UserWithToken:
        # check if email of user exists or not
        if not self.__user_repository.user_exist_by_email(email=login_data.email):
            raise HTTPException(status_code=400, detail="Invalid credentials")
        
        # get user by email
        user = self.__user_repository.get_user_by_email(email=login_data.email)
        
        # check if login password matches with user password
        if verify_password(plain_password=login_data.password, hashed_password=user.password):
            token = sign_jwt(user_id=user.id)
            if token: # return token to the user
                return UserWithToken(token=token)
            else:
                raise HTTPException(status_code=500, detail="Unable to process request")
        else:
            raise HTTPException(status_code=400, detail="Invalid credentials")

    def get_user(self, user_id: int):
        user = self.__user_repository.get_user_by_id(id=user_id)
        if user:
            return user
        raise HTTPException(status_code=400, detail="User is not available")