import sys
from loguru import logger


logger.add("{time:YYYY-MM-DD}.log",rotation="12:00", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}")
