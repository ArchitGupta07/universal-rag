from dependency_injector import containers, providers
from src.services.health import HealthService
from src.services.item import ItemService
from src.repositories.item_repository import ItemRepository
from src.db.db_manager import db_manager


class Services(containers.DeclarativeContainer):
    health_service = providers.Singleton(HealthService)

    item_repository = providers.Singleton(
        ItemRepository,
        # collection=providers.Callable(
        #     lambda: db_manager.get_collection("items")
        # ),
    )

    item_service = providers.Singleton(
        ItemService,
        item_repository=item_repository,
    )


class ApplicationContainer(containers.DeclarativeContainer):
    services = providers.Container(Services)

    wiring_config = containers.WiringConfiguration(
        modules=[
            "src.controllers.health",
            "src.controllers.item",
        ]
    )
