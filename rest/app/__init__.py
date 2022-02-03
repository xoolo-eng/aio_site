
from aiohttp import web
from rest.app.server import create_app, a_create_app


def run():
    app = create_app()
    web.run_app(app, host="127.0.0.1", port=8008)