import datetime
import uuid

from sqlalchemy import Column, Integer, DateTime, String

from restful_auto_service.data.sqlalchemy_base import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, autoincrement=True)
    created = Column(DateTime, default=datetime.datetime.now)

    name = Column(String, nullable=False, unique=True, index=True)
    hashed_password = Column(String)
    api_key = Column(String, default=lambda: str(uuid.uuid4()),
                     index=True, unique=True)
