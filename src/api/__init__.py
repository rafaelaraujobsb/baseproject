import logging
from uuid import uuid4

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from src.api.middleware import RouterLoggingMiddleware
from src.api.routes import health
from src.config import get_settings

settings = get_settings()


def start_api(version: str) -> FastAPI:
    app = FastAPI(
        title="FastAPI with Docker",
        description="This is a simple FastAPI application with Docker",
        version=version,
        debug=settings.LOG_LEVEL == "DEBUG",
    )

    app.add_middleware(RouterLoggingMiddleware, logger=logging.getLogger(__name__))
    app.add_middleware(
        CorrelationIdMiddleware,
        header_name="X-Request-ID",
        update_request_header=True,
        generator=lambda: uuid4().hex,
    )

    add_routes(app)
    add_metrics(app)

    logging.info(f"API started on {settings.HOST}:{settings.PORT}")

    return app


def add_routes(app: FastAPI):
    app.include_router(health.router)


def add_metrics(app: FastAPI):
    Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
        should_respect_env_var=True,
        should_instrument_requests_inprogress=True,
        excluded_handlers=["/docs", "/openapi.json", "/metrics"],
        env_var_name="ENABLE_METRICS",
        inprogress_name="inprogress",
        inprogress_labels=True,
    ).instrument(app).expose(app, include_in_schema=True, should_gzip=True)
