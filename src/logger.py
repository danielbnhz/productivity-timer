import logging
from pathlib import Path

LOG_PATH = Path("productivity.log")

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

logger = logging.getLogger("productivity")
