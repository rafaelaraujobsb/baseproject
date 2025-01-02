from src.config import get_settings

settings = get_settings()

bind = f"{settings.HOST}:{settings.PORT}"
workers = settings.WORKERS
worker_class = "uvicorn.workers.UvicornWorker"
timeout = settings.GUNICORN_TIMEOUT
keepalive = settings.KEEPALIVE
max_requests = settings.MAX_REQUESTS
loglevel = settings.LOG_LEVEL
accesslog = "-"
errorlog = "-"

preload_app = True
capture_output = True
