from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.user import UserInCreate, UserInLogin, UserWithToken, UserOutput
from app.core.database import get_db
from app.services.user import UserService

auth_router = APIRouter()

@auth_router.post("/login", status_code=200, response_model=UserWithToken)
def login(
    login_data: UserInLogin,
    session: Session = Depends(get_db) # inject session from get_db into session variable
):
    try:
        return UserService(session=session).login(login_data=login_data)
    except Exception as e:
        print(e)
        raise e
    
@auth_router.post("/signup", status_code=201, response_model=UserOutput)
def signup(
    signup_data: UserInCreate,
    session: Session = Depends(get_db)
):
    try:
        return UserService(session=session).signup(user_data=signup_data)
    except Exception as e:
        print(e)
        raise e
    
# router -> service -> repository -> db
# router <- service <- repository <- db