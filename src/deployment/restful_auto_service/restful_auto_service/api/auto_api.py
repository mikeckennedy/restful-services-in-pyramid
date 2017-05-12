from pyramid.request import Request
from pyramid.response import Response
from pyramid.view import view_config
import logbook

import restful_auto_service.infrastructure.auth as auth
from restful_auto_service.data.repository import Repository
from restful_auto_service.viewmodels.create_auto_viewmodel import CreateAutoViewModel
from restful_auto_service.viewmodels.update_auto_viewmodel import UpdateAutoViewModel

log = logbook.Logger("API/Auto")


@view_config(route_name='autos_api',
             request_method='GET',
             renderer='negotiate')
@auth.require_api_auth
def all_autos(request):
    log.trace("Listing cars for {}".format(request.api_user.name))
    cars = Repository.all_cars(limit=25)
    return cars


@view_config(route_name='auto_api',
             request_method='GET',
             renderer='negotiate')
@auth.require_api_auth
def single_auto(request: Request):
    car_id = request.matchdict.get('car_id')
    log.trace("Car details for car {} and user {}".format(
        car_id,
        request.api_user.name))

    if car_id == '__first__':
        car_id = Repository.all_cars()[0].id

    car = Repository.car_by_id(car_id)
    if not car:
        msg = "The car with id '{}' was not found.".format(car_id)
        return Response(status=404, json_body={'error': msg})

    return car


@view_config(route_name='autos_api',
             request_method='POST',
             renderer='json')
@auth.require_api_auth
def create_auto(request: Request):
    log.info("The user {} is creating a car".format(request.api_user.name))

    try:
        car_data = request.json_body
    except Exception as x:
        log.warn("The submitted JSON body couldn't be parsed for {}".format(
            request.api_user.name))
        return Response(status=400, body='Could not parse your post as JSON.' + str(x))

    vm = CreateAutoViewModel(car_data)
    vm.compute_details()
    if vm.errors:
        log.warn("The submitted invalid car by {}, reasons: {}".format(
            request.api_user.name, '; '.join(vm.errors)))
        return Response(status=400, body=vm.error_msg)

    try:
        car = Repository.add_car(vm.car)
        log.info("{} has successfully created car {}".format(
            request.api_user.name, car.id))
        return Response(status=201, json_body=car.to_dict())
    except Exception as x:
        log.error("Failed to save car: {}".format(x))
        return Response(status=500, body='Could not save car. ' + str(x))


# noinspection PyBroadException
@view_config(route_name='auto_api',
             request_method='PUT')
@auth.require_api_auth
def update_auto(request: Request):
    car_id = request.matchdict.get('car_id')
    car = Repository.car_by_id(car_id)
    if car_id == '__first__':
        car_id = Repository.all_cars()[0].id

    if not car:
        msg = "The car with id '{}' was not found.".format(car_id)
        return Response(status=404, json_body={'error': msg})

    try:
        car_data = request.json_body
    except:
        return Response(status=400, body='Could not parse your post as JSON.')

    vm = UpdateAutoViewModel(car_data, car_id)
    vm.compute_details()
    if vm.errors:
        return Response(status=400, body=vm.error_msg)

    try:
        Repository.update_car(vm.car)
        return Response(status=204, body='Car updated successfully.')
    except:
        return Response(status=400, body='Could not update car.')


# noinspection PyBroadException
@view_config(route_name='auto_api',
             request_method='DELETE')
@auth.require_api_auth
def delete_auto(request: Request):
    car_id = request.matchdict.get('car_id')
    car = Repository.car_by_id(car_id)
    if not car:
        msg = "The car with id '{}' was not found.".format(car_id)
        return Response(status=404, json_body={'error': msg})

    try:
        Repository.delete_car(car_id)
        return Response(status=204, body='Car deleted successfully.')
    except:
        return Response(status=400, body='Could not update car.')
