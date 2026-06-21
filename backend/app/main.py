from fastapi import FastAPI

from app.api.endpoints import example_endpoint, health
from app.configs.settings import get_settings
from app.init.dicontainer import AppContainer


def create_app() -> FastAPI:
    app = FastAPI(title="software-project-template-backend")
    container = AppContainer()
    container.settings.from_dict(get_settings().model_dump())
    setattr(app, "container", container)

    container.wire(modules=[example_endpoint])
    app.include_router(health.router)
    app.include_router(example_endpoint.router)
    return app


app = create_app()
