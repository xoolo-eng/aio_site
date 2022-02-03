import importlib
import traceback
from typing import Union, TypeVar, Generator
from collections import namedtuple


__all__ = ("Controller", "ControllerError")

View = TypeVar("View")


Route = namedtuple("Route", "path, handler, name")


class ControllerError(Exception):
    """Controller exception."""


class Controller:
    """Url controller."""

    _urlpatterns = set()
    _sub_path = ""

    @classmethod
    def add(cls, path: str, handler: View, name: str) -> None:
        """Add new url to all urls.

        :param path: path to resource.
        :type path: str
        :param handler: view object.
        :type handler: View
        :param name: name of route.
        :type name: str
        """
        cls._urlpatterns.add(Route("".join((cls._sub_path, path)), handler, name))

    @classmethod
    def include(cls, path: str, module: str) -> None:
        """Include other url file.

        :param path: path to resource.
        :type path: str
        :param module: app.urls
        :type module: str
        :raises ConnectionError: if import error.
        """
        old_sub_path = cls._sub_path
        cls._sub_path += path
        try:
            importlib.import_module(module)
        except Exception:
            raise ConnectionError(
                "Import {!r} from {!r}:/n{}".format(
                    path, module, traceback.format_exc()
                )
            )
        cls._sub_path = old_sub_path

    @classmethod
    def get(cls, name: str) -> Union[Route, None]:
        """Get route by name.

        :param name: route name.
        :type name: str
        :return: route.
        :rtype: Union[Route, None]
        """
        for route in cls._urlpatterns:
            if route.name == name:
                return route
        return None

    @classmethod
    def entry_point(cls, module: str) -> None:
        """Set root urls file.

        :param module: app.urls
        :type module: str
        :raises ConnectionError: if import error.
        """
        try:
            importlib.import_module(module)
        except Exception:
            raise ConnectionError(
                "Import {!r}:\n{}".format(module, traceback.format_exc())
            )

    @classmethod
    def urls(cls) -> Generator:
        """Urls generator.

        :yield: next router.
        :rtype: Generator
        """
        for route in cls._urlpatterns:
            yield route
