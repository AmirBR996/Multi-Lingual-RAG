from deep_translator import GoogleTranslator
from langdetect import detect
from roman import roman_to_nepali_text, nepali_to_text

def preprocess_query(text):
    try:
        lang = detect(text)
    except:
        lang = "unknown"

    if lang == "en":
        nepali_query = GoogleTranslator(source="en", target="ne").translate(text)
        return nepali_query, "en"
    elif lang in ("ne", "hi"):
        return text, "ne"
    else:
        nepali_query = roman_to_nepali_text(text)
        return nepali_query, "roman"

def output_query(text, source):
    if source == "en":
        return GoogleTranslator(source="ne", target="en").translate(text)
    elif source == "ne":
        return text
    else:
        return nepali_to_text(text)