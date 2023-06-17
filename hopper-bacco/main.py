from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.gzip import GZipMiddleware

from routes.api_router import APIRouter
from shared.middlewares.exception_handler_middleware import ExceptionHandlerMiddleware
from shared.middlewares.list_string_flattening_middleware import QueryStringFlatteningMiddleware
from shared.utilities.configurator import Configurator

settings = Configurator.instance().get_settings()
allowed_hosts = settings.allowed_hosts


def get_application() -> FastAPI:
    # Doc: http://127.0.0.1:YOUR_PORT/redoc
    application = FastAPI(
        # TODO: Set title, description and version from setup.py or pyproject.toml
        title=settings.title,
        description=settings.description,
        version=settings.version
    )

    application.add_middleware(CORSMiddleware, allow_origins=allowed_hosts)
    application.add_middleware(GZipMiddleware)
    application.add_middleware(QueryStringFlatteningMiddleware)
    application.add_middleware(ExceptionHandlerMiddleware)

    api = APIRouter()
    application.include_router(
        api.router,
        prefix='/api/v1',
        tags=['api']
    )
    return application


app = get_application()
