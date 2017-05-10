import abc
from typing import Optional, Any

from pyramid.renderers import RendererHelper


class RendererAbstractBase(metaclass=abc.ABCMeta):
    # noinspection PyUnusedLocal
    @abc.abstractmethod
    def __call__(self, info: RendererHelper):
        pass

    # noinspection PyUnusedLocal
    @abc.abstractmethod
    def can_serialize_value(self, value: Optional[Any]) -> bool:
        pass

    @abc.abstractmethod
    def add_adapter(self, cls_type, convert_function):
        return
