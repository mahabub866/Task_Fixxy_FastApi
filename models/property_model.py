#import every functionaliy and  module
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import Base
from sqlalchemy.dialects.mysql import JSON

#Models Create for Property
class PropertyModel(Base):
    __tablename__="properties"

    id = Column(Integer, primary_key=True)
    uid = Column(String(255), unique=True, nullable=False)
    name = Column(String(80), nullable=False)
    active = Column(Boolean, default=True)
    logs = Column(JSON)
    create_at = Column(DateTime, nullable=True, default=datetime.now(timezone.utc))



    def __repr__(self):
        return f'<RoleModel {self.name}'