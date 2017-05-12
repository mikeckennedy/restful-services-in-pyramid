import datetime

import logbook
from pyramid.config import Configurator
from pyramid.events import NewRequest

import restful_auto_service.infrastructure.logging as logging
from restful_auto_service.data.car import Car
from restful_auto_service.data.db_factory import DbSessionFactory
from restful_auto_service.data.repository import Repository
from restful_auto_service.renderers.csv_renderer import CSVRendererFactory
from restful_auto_service.renderers.image_direct_renderer import ImageDirectRendererFactory
from restful_auto_service.renderers.image_renderer import ImageRedirectRendererFactory
from restful_auto_service.renderers.json_renderer import JSONRendererFactory
from restful_auto_service.renderers.negotiate_renderer import NegotiatingRendererFactory


def main(_, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')

    log = init_logging(config)
    allow_cors(config, log)
    init_db(config, log)
    configure_renderers(config)
    register_routes(config)

    return config.make_wsgi_app()


def init_logging(config):
    settings = config.get_settings()
    logfile = settings.get('logbook_logfile')

    logging.global_init(logfile)

    log = logbook.Logger("App Startup")
    log.info("Configured logbook in {} mode with file '{}'.".format(
        'dev_mode' if not logfile else 'prod_mode',
        logfile
    ))

    return log


def init_db(config, log):
    settings = config.get_settings()
    db_file = settings.get('db_filename')

    DbSessionFactory.global_init(db_file)
    log.info('Configured DB with Sqlite file: {}.'.format(db_file))


def allow_cors(config, log):
    def add_cors_headers_response_callback(event):
        def cors_headers(_, response):
            # log.trace("Adding CORS permission to request: {}".format(
            #     request.url
            # ))
            response.headers.update({
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST,GET,DELETE,PUT,OPTIONS',
                'Access-Control-Allow-Headers': 'Origin, Content-Type, Accept, Authorization',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Max-Age': '1728000',
            })

        event.request.add_response_callback(cors_headers)

    log.info("Configuring Pyramid for CORS permissions")
    config.add_subscriber(add_cors_headers_response_callback, NewRequest)


def register_routes(config):
    config.add_static_view('static', 'static', cache_max_age=1)

    config.add_route('home', '/')

    config.add_route('autos_api', '/api/autos')
    config.add_route('auto_api', '/api/autos/{car_id}')

    config.scan()


def configure_renderers(config):
    json_renderer = JSONRendererFactory(indent=4)
    json_renderer.add_adapter(Car, lambda c, _: c.to_dict())
    json_renderer.add_adapter(datetime.datetime, lambda d, _: str(d.isoformat()))
    config.add_renderer('json', json_renderer)

    csv_renderer = CSVRendererFactory()
    csv_renderer.add_adapter(Car, lambda c, _: c.to_dict())
    config.add_renderer('csv', csv_renderer)

    # image_renderer = ImageRedirectRendererFactory()
    image_renderer = ImageDirectRendererFactory()
    image_renderer.add_adapter(Car, lambda c, _: c.to_dict())
    config.add_renderer('png', image_renderer)

    negotiate_renderer = NegotiatingRendererFactory()
    negotiate_renderer.add_accept_all_renderer(json_renderer)
    negotiate_renderer.add_renderer('application/json', json_renderer)
    negotiate_renderer.add_renderer('text/csv', csv_renderer)
    negotiate_renderer.add_renderer('image/png', image_renderer)
    negotiate_renderer.add_adapter(Car, lambda c, _: c.to_dict())
    config.add_renderer('negotiate', negotiate_renderer)
