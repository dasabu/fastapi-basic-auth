from .base import BaseRepository
from app.models.user import User
from app.schemas.user import UserInCreate

class UserRepository(BaseRepository): # contain methods to communicate with the db
    def create_user(self, user_data: UserInCreate):
        # dump the data from user_data schema into an user object
        new_user = User(**user_data.model_dump(exclude_none=True)) # make sure no value in the schema is None
        
        self.session.add(instance=new_user)
        self.session.commit()
        self.session.refresh(instance=new_user)
        
        return new_user

    def user_exist_by_email(self, email: str) -> bool:
        user = self.session.query(User).filter_by(email=email).first()
        return bool(user) # True if exists, else False
    
    def get_user_by_email(self, email: str) -> User:
        user = self.session.query(User).filter_by(email=email).first()
        return user

    def get_user_by_id(self, id: str) -> User:
        user = self.session.query(User).filter_by(id=id).first()
        return user