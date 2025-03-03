from loguru import logger
import sys

def setup_logger():
    logger.remove()
    logger.add(sys.stdout, format="<fg #8A2BE2>{time:mm-ss}</fg #8A2BE2> | <fg #bfa9d3>{level}</fg #bfa9d3> | <fg #968e9e>{message}</fg #968e9e>", level="INFO")
