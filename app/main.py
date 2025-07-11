from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.logging import LoggingConfig

from app.config.settings import settings
from app.controllers.auth import AuthController
from app.controllers.user import UserController
from app.core.database import database_manager
from app.core.dependencies import dependencies


async def on_startup() -> None:
    """Application startup event."""
    await database_manager.create_all()


async def on_shutdown() -> None:
    """Application shutdown event."""
    await database_manager.close()


def create_app() -> Litestar:
    """Create Litestar application."""

    cors_config = CORSConfig(
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    logging_config = LoggingConfig(
        root={"level": "INFO", "handlers": ["console"]},
        formatters={
            "standard": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            }
        },
        configure_root_logger=True,
    )

    # Define dependencies correctly
    dependencies_config = dependencies

    return Litestar(
        route_handlers=[AuthController, UserController],
        dependencies=dependencies_config,
        cors_config=cors_config,
        logging_config=logging_config,
        on_startup=[on_startup],
        on_shutdown=[on_shutdown],
        debug=settings.debug,
    )


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
