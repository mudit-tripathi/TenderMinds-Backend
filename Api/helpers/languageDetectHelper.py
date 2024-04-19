from langdetect import detect, LangDetectException

from Api.config import logging_config
logging_config.setup_logging()
import logging

# Create a logger for this module
logger = logging.getLogger(__name__)

def safe_detect(text):
    logger.info("Entered safe_detect helper")
    try:
        return detect(text)
    except LangDetectException:
        return "No detectable language"
