import multiprocessing

from src.config import get_settings

settings = get_settings()

bind = f"{settings.HOST}:{settings.PORT}"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120
keepalive = 5
max_requests = settings.MAX_REQUESTS
loglevel = settings.LOG_LEVEL
accesslog = "-"
errorlog = "-"

preload_app = True
capture_output = True
