from .config import config
from .logging import configure_logging, get_logger

# Configure logging early
logger = configure_logging(
    log_level=config.get("logging.level"),
    log_file=config.get("logging.file")
)