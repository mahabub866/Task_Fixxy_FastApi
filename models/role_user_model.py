#import every functionaliy and  module
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base
from sqlalchemy.dialects.mysql import JSON

#Models Create for Users
class RoleUserModel(Base):
    __tablename__="role_users"

    id = Column(Integer, primary_key=True)
    uid = Column(String(255), unique=True, nullable=False)
    username = Column(String(80), unique=True, nullable=False)
    password  = Column(String(255), nullable=False)
    token  = Column(String(500), unique=True, nullable=True)
    role_id  = Column(String(255), nullable=True)
    super_admin = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    jti = Column(String(255), nullable=True)
    logs = Column(JSON)
    create_at = Column(DateTime, nullable=True, default=datetime.now(timezone.utc))


    def __repr__(self):
        return f'<RoleUserModel {self.name}'