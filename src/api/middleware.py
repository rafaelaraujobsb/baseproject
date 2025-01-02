import logging
import time
from uuid import uuid4

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware

from src.api.schema.default_message import MESSAGE_500


def request_logging_data(request: Request) -> dict:
    return {
        "method": request.method,
        "path": request.url.path,
        "ip": request.client.host,
    }


def response_logging_data(response: Response, process_time: float) -> dict:
    return {
        "status": "successful" if response and response.status_code < 400 else "failed",
        "status_code": response.status_code,
        "time_taken": f"{process_time / 10**9:.4f}s",
    }


def add_middleware(app: FastAPI, logger: logging.Logger, enable_logging_exception: bool = True):
    @app.middleware("http")
    async def logging_middleware(request: Request, call_next) -> Response:
        start_time = time.perf_counter_ns()

        logger.info(request_logging_data(request))

        try:
            response = await call_next(request)

        except Exception:
            response = MESSAGE_500
            if enable_logging_exception:
                logger.exception("Uncaught exception")

        finally:
            process_time = time.perf_counter_ns() - start_time

            logger.info(response_logging_data(response, process_time))

            response.headers["X-Process-Time"] = str(process_time / 10**9)

            return response

    app.add_middleware(
        CorrelationIdMiddleware,
        header_name="X-Request-ID",
        update_request_header=True,
        generator=lambda: uuid4().hex,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
