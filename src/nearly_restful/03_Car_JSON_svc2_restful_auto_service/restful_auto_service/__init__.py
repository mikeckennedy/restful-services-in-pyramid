from pyramid.config import Configurator
from pyramid.events import NewRequest
from pyramid.renderers import JSON

from restful_auto_service.data.car import Car


def main(_, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')

    allow_cors(config)
    configure_renderers(config)
    register_routes(config)

    return config.make_wsgi_app()


def allow_cors(config):
    def add_cors_headers_response_callback(event):
        def cors_headers(_, response):
            response.headers.update({
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Max-Age': '1728000',
            })

        event.request.add_response_callback(cors_headers)

    config.add_subscriber(add_cors_headers_response_callback, NewRequest)


def register_routes(config):
    config.add_static_view('static', 'static', cache_max_age=1)

    config.add_route('home', '/')

    config.add_route('autos_api', '/api/autos')
    config.add_route('auto_api', '/api/autos/{car_id}')

    config.scan()


def configure_renderers(config):
    json_renderer = JSON(indent=4)
    json_renderer.add_adapter(Car, lambda c, _: c.to_dict())
    config.add_renderer('json', json_renderer)
