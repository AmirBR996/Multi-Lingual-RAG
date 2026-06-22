import re
from googletrans import Translator
from langdetect import detect
from roman import roman_to_nepali_text

translator = Translator()

def contains_nepali(text):
    return bool(re.search(r'[\u0900-\u097F]', text))

def preprocess_query(text):
    if contains_nepali(text):
        return text, "ne"

    try:
        lang = detect(text)
    except:
        lang = "unknown"

    if lang == "en":
        nepali_query = translator.translate(
            text,
            src="en",
            dest="ne"
        ).text
        return nepali_query, "en"

    nepali_query = roman_to_nepali_text(text)
    return nepali_query, "roman"