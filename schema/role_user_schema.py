#import every functionaliy and  module
from pydantic import BaseModel

#User Create Schema
class RoleUserCreate(BaseModel):
    username: str
    password: str
    role: str
    active: bool = None

    class Config:
        orm_mode = True

    class Config:
        extra = "forbid"

class RoleRegularUserCreate(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True

    class Config:
        extra = "forbid"
#Login Schema
class LoginModel(BaseModel):
    username:str
    password:str

    class Config:
        orm_mode = True

    class Config:
        extra = "forbid"

#User Update Schema
class RoleUserUpdate(BaseModel):
    uid: str
    active: bool
    role:str

    class Config:
        orm_mode = True

    class Config:
        extra = "forbid"

#User Status Update Schema
class RoleUserStatusUpdate(BaseModel):
    uid: str
    active:bool

    class Config:
        orm_mode = True

    class Config:
        extra = "forbid"

#User Self Password Update Schema
class AdminSelfUserChangePasswordSchema(BaseModel):
    uid: str
    new_password: str
    old_password: str

    class Config:
        orm_mode = True
        
    class Config:
        extra = "forbid"

#User Password Update Schema
class AdminUserChangePasswordSchema(BaseModel):
    uid: str
    new_password: str

    class Config:
        orm_mode = True

    class Config:
        extra = "forbid"