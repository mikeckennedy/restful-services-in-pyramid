import random

# noinspection PyPackageRequirements
from dateutil.parser import parse

from restful_auto_service.data.car import Car
from restful_auto_service.data.db_factory import DbSessionFactory


class Repository:
    __car_data = {}
    __fake_image_url = [
        'https://s1.cdn.autoevolution.com/images/models/OPEL_Vectra-GTS-2005_main.jpg',
        'http://www.opel.com/content/dam/Opel/OpelCorporate/corporate/nscwebsite/en/00_Home/252x142/'
        'Teaser_opel_group_252x142.jpg',
        'http://www.opel.com/content/dam/Opel/Europe/master/hq/en/15_ExperienceSection/02_AboutOpel/History_Heritage/'
        '1946_1970/Opel_Experience_History_Heritage_1953_Opel_Olympia_304x171_21754.jpg',
        'http://www.opel.co.za/content/dam/Opel/Europe/master/hq/en/15_ExperienceSection/11_Multimedia/02_Wallpaper/'
        'Opel_GT_992x425_16900.jpg',
        'https://pictures.topspeed.com/IMG/crop/201510/2016-opel-astra-tcr-16_600x0w.jpg',
        'https://1.bp.blogspot.com/-9l6kQpiC4nM/TnILNXWfUgI/AAAAAAAFEK4/70PPQSGCnmk/s1600/Opel-Rak-e-14.jpg',
        'http://www.opel.co.za/content/dam/Opel/Europe/master/hq/en/01_Vehicles/Concept_Cars/GT/Embargo/'
        'Opel_Concept_Cars_GT_1_1024x576_A298968.jpg',
    ]

    @classmethod
    def all_cars(cls, limit=None):
        session = DbSessionFactory.create_session()

        query = session.query(Car).order_by(Car.year.desc())

        if limit:
            cars = query[:limit]
        else:
            cars = query.all()

        session.close()

        return cars

    @classmethod
    def car_by_id(cls, car_id):
        session = DbSessionFactory.create_session()

        car = session.query(Car).filter(Car.id == car_id).first()

        session.close()

        return car

    @classmethod
    def add_car(cls, car: Car):
        session = DbSessionFactory.create_session()

        db_car = Car()
        db_car.last_seen = parse(car.last_seen)
        db_car.brand = car.brand
        db_car.image = car.image if car.image else random.choice(cls.__fake_image_url)
        db_car.damage = car.damage
        db_car.year = int(car.year)
        db_car.price = int(car.price)
        db_car.name = car.name

        session.add(db_car)
        session.commit()

        return db_car

    @classmethod
    def update_car(cls, car):

        session = DbSessionFactory.create_session()

        db_car = session.query(Car).filter(Car.id == car.id).first()
        db_car.last_seen = car.last_seen
        db_car.brand = car.brand
        db_car.image = car.image if car.image else random.choice(cls.__fake_image_url)
        db_car.damage = car.damage
        db_car.year = car.year
        db_car.price = car.price
        db_car.name = car.name

        session.commit()

        return db_car

    @classmethod
    def delete_car(cls, car_id):
        session = DbSessionFactory.create_session()
        db_car = session.query(Car).filter(Car.id == car_id).first()
        if not db_car:
            return

        session.delete(db_car)
        session.commit()
