from pydantic import EmailStr, BaseModel, str

class Token(BaseModel):
    access_token: str
    token_type: str

