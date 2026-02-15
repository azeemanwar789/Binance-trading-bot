import logging

logging.basicConfig(
    filename="bot.log",  # Log file in root folder
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger()
