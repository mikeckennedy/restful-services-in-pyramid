import csv
import os
import random
import uuid

from restful_auto_service.data.car import Car


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
        if not cls.__car_data:
            cls.__load_data()

        cars = list(cls.__car_data.values())
        if limit:
            cars = cars[:limit]

        return cars

    @classmethod
    def car_by_id(cls, car_id):
        cls.__load_data()
        return cls.__car_data.get(car_id)

    @classmethod
    def __load_data(cls):
        if cls.__car_data:
            return

        file = os.path.join(
            os.path.dirname(__file__),
            'opel.csv'
        )

        with open(file, 'r', encoding='utf-8') as fin:
            # brand,name,price,year,damage,last_seen
            reader = csv.DictReader(fin)
            for row in reader:
                key = Repository.generate_id()
                row['id'] = key
                row['image'] = random.choice(cls.__fake_image_url)
                cls.__car_data[key] = Car(**row)

                # Converting this to cars is kinda slow,
                # 100 records is enough to get started with.
                if len(cls.__car_data) > 100:
                    break

    @classmethod
    def generate_id(cls):
        return str(uuid.uuid4())

    @classmethod
    def add_car(cls, car):
        if not cls.__car_data:
            cls.__load_data()
        key = Repository.generate_id()
        car.id = key
        cls.__car_data[key] = car

        return car

    @classmethod
    def update_car(cls, car):
        key = car.id
        cls.__car_data[key] = car

        return car

    @classmethod
    def delete_car(cls, car_id):
        del cls.__car_data[car_id]
