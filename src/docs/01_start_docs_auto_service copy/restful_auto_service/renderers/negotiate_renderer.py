from typing import Optional, Any

from restful_auto_service.renderers.abstract_renderer import RendererAbstractBase


class NegotiatingRendererFactory(RendererAbstractBase):
    def __init__(self):
        self.adapters = {}
        self.renderers = {}
        self.info = None

    def __call__(self, info):
        self.info = info
        return self._render

    def _render(self, value, system):
        request = system.get('request')
        accept_headers = request.headers.get('accept')

        if not accept_headers:
            return self.renderers['*/*'](self.info)(value, system)

        accept_headers = self.parse_accept_headers(accept_headers)
        for accept_type in accept_headers:
            renderer = self.renderers.get(accept_type)
            if renderer:
                return renderer(self.info)(value, system)

        raise Exception("Could not find renderer for content type {}"
                        .format(accept_headers))

    def can_serialize_value(self, value: Optional[Any]) -> bool:
        return True

    # noinspection PyMethodMayBeStatic
    def parse_accept_headers(self, header_value) -> list:
        # text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
        if not header_value:
            return []

        accept_types = []
        values = header_value.split(',')
        for value in values:
            parts = value.split(';')
            if len(parts) == 1:
                accept_types.append(value.strip().lower())
            elif len(parts) == 2:
                accept_types.append(parts[0].strip().lower())

        return accept_types

    def add_adapter(self, cls_type, convert_function):
        self.adapters[cls_type] = convert_function
        for renderer in self.renderers.values():
            renderer.add_adapter(cls_type, convert_function)

    def add_accept_all_renderer(self, renderer: RendererAbstractBase):
        self.add_renderer('*/*', renderer)

    def add_renderer(self, content_type, renderer: RendererAbstractBase):
        if not isinstance(renderer, RendererAbstractBase):
            raise Exception("Renderer must be a base renderer type.")

        content_type = content_type.strip().lower()
        self.renderers[content_type] = renderer
