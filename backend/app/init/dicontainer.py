from dependency_injector import containers, providers

from app.infra.db_client import init_db_pool
from app.services.example_service import ExampleService


class AppContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=["app.api.endpoints.example_endpoint"],
    )

    settings = providers.Configuration()

    db_pool = providers.Resource(
        init_db_pool,
        conn_info=settings.database_url,
    )

    example_service = providers.Factory(
        ExampleService,
        pool=db_pool, 
    )
