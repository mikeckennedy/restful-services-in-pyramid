from dateutil.parser import parse

from restful_auto_service.data.car import Car
from restful_auto_service.viewmodels.base_viewmodel import ViewModelBase
from restful_auto_service.viewmodels.create_auto_viewmodel import CreateAutoViewModel


class UpdateAutoViewModel(CreateAutoViewModel):
    def __init__(self, data_dict, car_id):
        super().__init__(data_dict)
        self.car_id = car_id

    def compute_details(self):

        car_id = self.data_dict.get('id')
        if not self.car_id:
            self.errors.append("No car ID specified.")
        if self.car_id != car_id:
            self.errors.append("Car ID mismatch.")

        super().compute_details()

