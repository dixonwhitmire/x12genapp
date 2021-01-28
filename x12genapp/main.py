from fastapi import FastAPI
from x12genapp.routes import (customers,
                              x12)

from x12genapp.config import get_app_settings
import uvicorn


def get_app() -> FastAPI:
    """
    Configures the Fast API application
    """
    app = FastAPI()
    app.include_router(x12.router, prefix='/x12')
    app.include_router(customers.router, prefix='/customers')
    return app


app = get_app()

if __name__ == '__main__':
    """Launches the uvicorn application"""
    settings = get_app_settings()

    uvicorn_params = {
        'host': settings.uvicorn_host,
        'port': settings.uvicorn_port,
        'reload': settings.uvicorn_reload
    }

    uvicorn.run(settings.uvicorn_app, **uvicorn_params)
