import csv
import os
import uuid


class Repository:
    __car_data = {}

    @classmethod
    def all_cars(cls, limit=None):
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
                key = str(uuid.uuid4())
                row['id'] = key
                cls.__car_data[key] = row

    @classmethod
    def add_car(cls, car_data):
        key = str(uuid.uuid4())
        car_data['id'] = key
        cls.__car_data[key] = car_data

        return car_data

    @classmethod
    def update_car(cls, car_data):
        key = car_data['id']
        cls.__car_data[key] = car_data

        return car_data

    @classmethod
    def delete_car(cls, car_id):
        del cls.__car_data[car_id]
