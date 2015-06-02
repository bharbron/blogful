import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from .database import Base, engine

class Post(Base):
  __tablename__ = "posts"
  
  id = Column(Integer, primary_key=True)
  title = Column(String(1024))
  content = Column(Text)
  datetime = Column(DateTime, default=datetime.datetime.now)
  
Base.metadata.create_all(engine)