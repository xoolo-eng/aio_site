from aiohttp import web
import aiohttp_jinja2
import pathlib
from jinja2 import FileSystemLoader
from rest.url.router import Controller

BASE_DIR = pathlib.Path(__file__).parent.parent.absolute()

def create_app():
    app = web.Application()
    Controller.entry_point("rest.web.root.urls")
    for route in Controller.urls():
        app.router.add_route("*", route.path, route.handler, name=route.name)

    aiohttp_jinja2.setup(
            app,
            loader=FileSystemLoader(
                [
                    path / "templates"
                    for path in (BASE_DIR / "web").iterdir()
                    if path.is_dir() and (path / "templates").exists()
                ]
            ),
        )

    return app


async def a_create_app():
    return create_app(0)