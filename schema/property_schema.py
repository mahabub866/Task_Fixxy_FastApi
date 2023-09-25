#import every functionaliy and  module
from pydantic import BaseModel
from typing import  Optional

#Property Create Schema
class PropertyModelCreate(BaseModel):
    name: str
    active: Optional[bool] = True

    class Config:
        orm_mode = True

    class Config:
        extra = "forbid"

#Property Update Schema
class PropertyUpdate(BaseModel):
    uid: str
    name: str
    active: bool


    class Config:
        orm_mode = True

    class Config:
        extra = "forbid"

#Property Status Update Schema
class PropertyStatusUpdate(BaseModel):
    uid: str
    active:bool
    
    class Config:
        orm_mode = True

    class Config:
        extra = "forbid"

