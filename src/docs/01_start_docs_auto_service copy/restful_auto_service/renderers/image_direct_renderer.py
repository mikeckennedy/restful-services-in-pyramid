import requests
from io import BytesIO

from restful_auto_service.renderers.abstract_renderer import RendererAbstractBase


class ImageDirectRendererFactory(RendererAbstractBase):
    def __init__(self):
        self.adapters = {}

    def __call__(self, info):
        return self._render

    def _render(self, value, system):

        request = system.get('request')
        request.response.content_type = 'image/png'

        adapter = self.adapters.get(type(value))
        if adapter:
            value = adapter(value, None)

        if not isinstance(value, dict):
            raise Exception("Could not convert type {}".format(type(value)))

        image_url = value.get('image')
        if not image_url:
            raise Exception("Could not find URL")

        resp = requests.get(image_url)
        resp.raise_for_status()

        return BytesIO(resp.content)

    def can_serialize_value(self, value):
        return type(value) in self.adapters or isinstance(value, dict)

    def add_adapter(self, cls, method):
        self.adapters[cls] = method
