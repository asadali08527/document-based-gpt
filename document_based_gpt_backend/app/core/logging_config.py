# Placeholder for logging configuration if needed in future
import logging


# Configuring the logging format and level
def setup_logging():
    logging.basicConfig(
        filename="query_logs.log",
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

