from restful_auto_service.renderers.abstract_renderer import RendererAbstractBase


class CSVRendererFactory(RendererAbstractBase):
    def __init__(self):
        self.adapters = {}

    def __call__(self, info):
        return self._render

    # noinspection PyMethodMayBeStatic
    def _render(self, value, system):

        request = system.get('request')
        request.response.content_type = 'text/csv'

        if not value:
            return ''

        value = self.adapt_type(value)

        if not isinstance(value, list):
            raise ValueError("Can only process lists.")
        first = value[0]
        if not isinstance(first, dict):
            raise ValueError("Could not convert type: {}.".format(type(first)))

        first = value[0]
        headers = first.keys()

        response_rows = [','.join(headers)]
        for row in value:
            line_data = []
            for k in headers:
                line_data.append(row[k])
            line = ','.join(line_data)
            response_rows.append(line)

        return '\n'.join(response_rows)

    def adapt_type(self, value):
        if isinstance(value, dict):
            value = [value]

        t = type(value)
        if t in self.adapters:
            value = [self.adapters[t](value, _)]

        if isinstance(value, list):
            first = value[0]
            adapter = self.adapters.get(type(first))
            if adapter:
                for idx, item in enumerate(value):
                    value[idx] = adapter(item, None)

        return value

    def add_adapter(self, cls, method):
        self.adapters[cls] = method

    def can_serialize_value(self, value):
        return type(value) in self.adapters or isinstance(value, list)

