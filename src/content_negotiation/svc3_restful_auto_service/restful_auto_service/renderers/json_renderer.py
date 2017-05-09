from pyramid.renderers import JSON

from restful_auto_service.renderers.abstract_renderer import RendererAbstractBase


class JSONRendererFactory(JSON, RendererAbstractBase):

    def can_serialize_value(self, value):
        return True  # how do we know?


