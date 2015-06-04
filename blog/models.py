import datetime
from flask.ext.login import UserMixin

from sqlalchemy import Column, Integer, String, Text, DateTime

from .database import Base, engine

class Post(Base):
  __tablename__ = "posts"
  
  id = Column(Integer, primary_key=True)
  title = Column(String(1024))
  content = Column(Text)
  datetime = Column(DateTime, default=datetime.datetime.now)
  
class User(Base, UserMixin):
  __tablename__ = "users"
  
  id = Column(Integer, primary_key=True)
  name = Column(String(128))
  email = Column(String(128), unique=True)
  password = Column(String(128))
  
Base.metadata.create_all(engine)