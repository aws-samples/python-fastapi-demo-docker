from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from typing import Optional
from pydantic import BaseModel

Base = declarative_base()


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    description = Column(String, index=True)


class Event(BaseModel):
    message: str
    status: str
    type: str
    book: str
    author: str

    class Config:
        schema_extra = {
            "example": {
                "message": "Success",
                "status": "200 OK",
                "type": "my.event.type",
                "book": "1984",
                "author": "George Orwell",
            }
        }
