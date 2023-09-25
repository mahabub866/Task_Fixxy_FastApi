#import every functionaliy and  module
from pydantic import BaseModel
from typing import  Optional

#Role Create Schema
class RoleModelCreate(BaseModel):
    name: str
    active: Optional[bool] = True
    property_management: Optional[str] = 'a'
    regular_user_management: Optional[str] = 'a'
    user_management: Optional[str] = 'a'

    class Config:
        orm_mode = True

    class Config:
        extra = "forbid"

#Role Update Schema
class RoleUpdate(BaseModel):
    uid: str
    name: str
    active: bool
    property_management: str 
    regular_user_management: str 
    user_management: str 


    class Config:
        orm_mode = True

    class Config:
        extra = "forbid"

#Role Status Update Schema
class RoleStatusUpdate(BaseModel):
    uid: str
    active:bool
    
    class Config:
        orm_mode = True

    class Config:
        extra = "forbid"

