import uuid

import sqlalchemy
import datetime

from restful_auto_service.data.sqlalchemy_base import SqlAlchemyBase


class Car(SqlAlchemyBase):

    __tablename__ = 'Car'

    id = sqlalchemy.Column(sqlalchemy.String, primary_key=True,
                           default=lambda: str(uuid.uuid4()))
    brand = sqlalchemy.Column(sqlalchemy.String, index=True, nullable=False)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    damage = sqlalchemy.Column(sqlalchemy.String)
    image = sqlalchemy.Column(sqlalchemy.String)
    price = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=False)
    year = sqlalchemy.Column(sqlalchemy.Integer, index=True, nullable=False)
    last_seen = sqlalchemy.Column(sqlalchemy.DateTime, index=True,
                                  default=datetime.datetime.now)

    def to_dict(self):
        return {
            'brand': self.brand,
            'name': self.name,
            'price': self.price,
            'year': self.year,
            'damage': self.damage,
            'last_seen': self.last_seen.isoformat(),
            'id': self.id,
            'image': self.image
        }
