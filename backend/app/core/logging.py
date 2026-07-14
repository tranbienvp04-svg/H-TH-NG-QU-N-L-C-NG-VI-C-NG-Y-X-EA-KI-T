from loguru import logger
logger.add("logs/system.log",rotation="10 MB",retention="30 days")
