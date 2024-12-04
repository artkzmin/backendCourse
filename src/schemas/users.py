from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserRequestAdd(UserBase):
    password: str


class UserAdd(UserBase):
    hashed_password: str


class User(UserBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class UserWithHashedPassword(User):
    hashed_password: str
