from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func 
from database import Base

class Note(Base):
    __tablename__="notes"

    id = Column(Integer, primary_key=True, index=True) #index creates a table in the bg specifically for this column
    #primary key automatically means Index = True, which means mentioning index is redundant here, its mentioned just for the sake of it
    #index key can be used for columns which will be used to call for a row frequently
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now())
    updated_at = Column(DateTime(timezone=True),onupdate=func.now())
