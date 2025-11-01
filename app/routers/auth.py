from fastapi import APIRouter,  Depends
from app.database import get_db
from utils import sign_jwt, decode_jwt

# define authentication router
authentication_router = APIRouter(
    prefix="/auth",
    tags =["authentication"]
)

@authentication_router.get("/register")
def authenticate_user(db = Depends(get_db)):
    # check if useer exists 




