from pyramid.config import Configurator
from pyramid.events import NewRequest


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')

    allow_cors(config)
    register_routes(config)

    return config.make_wsgi_app()


def allow_cors(config):
    def add_cors_headers_response_callback(event):
        def cors_headers(_, response):
            print("Adding headers")
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
