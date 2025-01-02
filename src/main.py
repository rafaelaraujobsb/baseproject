from src import __version__
from src.api import start_api
from src.config import get_settings
from src.log import setup_logging

settings = get_settings()

setup_logging(settings.LOG_LEVEL)
app = start_api(__version__)
