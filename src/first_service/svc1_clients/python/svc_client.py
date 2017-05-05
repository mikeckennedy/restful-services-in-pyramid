import requests
from pprint import pprint


def main():
    cars = list_cars()
    show_cars(cars)

    car_id = input("What car do you want to see? (car ID): ")
    show_car_details(car_id)


def show_cars(cars):
    print("Cars for sale: ")
    for c in cars:
        print('{}: {}'.format(c[0], c[1]))


def show_car_details(car_id):
    car = get_car(car_id)
    pprint(car)


def list_cars():
    url = 'http://localhost:6543/api/autos'

    resp = requests.get(url)
    if resp.status_code != 200:
        print("Error contacting server... {}".format(resp.status_code))
        return

    cars = resp.json()

    return [
        (car.get('id'), car.get('name'))
        for car in cars
    ]


def get_car(car_id):
    url = 'http://localhost:6543/api/autos/{}'.format(car_id)

    resp = requests.get(url)
    if resp.status_code != 200:
        print("Error contacting server... {}".format(resp.status_code))
        return

    car = resp.json()
    return car


if __name__ == '__main__':
    main()
