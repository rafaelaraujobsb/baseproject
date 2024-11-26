from src import __version__
from src.api import start_api
from src.log import setup_log

setup_log()
app = start_api(__version__)
