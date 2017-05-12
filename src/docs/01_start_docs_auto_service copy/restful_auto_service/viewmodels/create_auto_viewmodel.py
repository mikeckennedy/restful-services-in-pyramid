from dateutil.parser import parse

from restful_auto_service.data.car import Car
from restful_auto_service.viewmodels.base_viewmodel import ViewModelBase


class CreateAutoViewModel(ViewModelBase):
    def __init__(self, data_dict):
        super().__init__()
        self.data_dict = data_dict
        self.car = None

    def compute_details(self):

        last_seen = self.data_dict.get('last_seen', None)
        if last_seen:
            last_seen = parse(last_seen)
        name = self.data_dict.get('name')
        brand = self.data_dict.get('brand')
        price = int(self.data_dict.get('price', -1))
        year = int(self.data_dict.get('year', -1))
        damage = self.data_dict.get('damage')
        image = self.data_dict.get('image')
        car_id = self.data_dict.get('id')

        if not name:
            self.errors.append("Name is a required field.")
        if not brand:
            self.errors.append("Brand is a required field.")
        if price is None:
            self.errors.append("You must specify a price")
        elif price < 0:
            self.errors.append("Price must be non-negative.")
        if year is None:
            self.errors.append("You must specify a year")
        elif year < 0:
            self.errors.append("Year must be non-negative.")

        if not self.errors:
            car = Car(brand=brand, name=name, price=price,
                      year=year, damage=damage, image=image,
                      last_seen=last_seen, id=car_id)
            self.car = car
