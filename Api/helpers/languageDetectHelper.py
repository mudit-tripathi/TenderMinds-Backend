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

from googletrans import Translator

def is_english(sentence):
    logger.info("Entered is_english helper")
    # Create a translator object
    translator = Translator()

    # Split the sentence into words
    words = sentence.split()

    # Initialize count of English words
    english_count = 0

    # Check each word's language
    for word in words:
        # Check if the word has sufficient length
        if len(word) > 1:
            lang = translator.detect(word).lang
            if lang == 'en':
                english_count += 1

    # Calculate the percentage of English words
    percentage_english = english_count / len(words) * 100
    return percentage_english >= 90

