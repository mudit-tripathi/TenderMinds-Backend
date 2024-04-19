from datetime import datetime, timezone

from Api.config import logging_config
logging_config.setup_logging()
import logging

# Create a logger for this module
logger = logging.getLogger(__name__)

def date_string_to_timestamp(date_string, format_string="%d-%b-%Y %I:%M %p"):
    logger.info(f"Entering date_string_to_timestamp")
    # Convert the date string to a timezone-aware datetime object assuming UTC
    date_object = datetime.strptime(date_string, format_string)
    date_object = date_object.replace(tzinfo=timezone.utc)
    # Convert the datetime object to a UNIX timestamp (seconds since epoch)
    timestamp = int(date_object.timestamp())
    logger.info(f"Exiting date_string_to_timestamp")
    return timestamp