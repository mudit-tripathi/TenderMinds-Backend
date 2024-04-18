from langdetect import detect, LangDetectException

def safe_detect(text):
    try:
        return detect(text)
    except LangDetectException:
        return "No detectable language"
