#import every functionaliy and  module
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from sqlalchemy.dialects.mysql import JSON

#Models Create for Block unused token
class BlockModel(Base):
    __tablename__="blocks"

    id = Column(Integer, primary_key=True)
    block_id = Column(String(255), unique=True, nullable=False)
    token = Column(String(500), unique=True, nullable=False)
    username = Column(String(80), nullable=False)
    jti = Column(String(80), unique=True, nullable=False)
    role = Column(JSON)
    logs = Column(JSON)
    create_at = Column(DateTime, nullable=True, default=datetime.now(timezone.utc))


    def __repr__(self):
        return f'<BlockModel {self.jti}'