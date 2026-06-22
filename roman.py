roman_to_nepali = {
    "ma": "म",
    "mero": "मेरो",
    "malai": "मलाई",
    "timro": "तिम्रो",
    "timilai": "तिमीलाई",
    "tapai": "तपाईं",
    "tapailai": "तपाईंलाई",
    "hami": "हामी",
    "hamro": "हाम्रो",
    "u": "ऊ",
    "uni": "उनी",
    "unihar": "उनीहरू",

    "k": "के",
    "ke": "के",
    "kina": "किन",
    "kasari": "कसरी",
    "kata": "कता",
    "kahile": "कहिले",
    "kasto": "कस्तो",
    "ko": "को",
    "kun": "कुन",

    "cha": "छ",
    "chha": "छ",
    "chu": "छु",
    "chuina": "छैन",
    "chaina": "छैन",
    "chan": "छन्",
    "thiyo": "थियो",
    "thiye": "थिए",
    "huncha": "हुन्छ",
    "hunuhuncha": "हुनुहुन्छ",
    "bhayo": "भयो",
    "garyo": "गर्यो",

    "ghar": "घर",
    "school": "विद्यालय",
    "college": "कलेज",
    "office": "कार्यालय",
    "pani": "पानी",
    "khana": "खाना",
    "chiya": "चिया",
    "dudh": "दूध",
    "sathi": "साथी",
    "kitab": "किताब",

    "ramro": "राम्रो",
    "thik": "ठिक",
    "sano": "सानो",
    "thulo": "ठूलो",
    "naya": "नयाँ",
    "purano": "पुरानो",

    "ho": "हो",
    "hoina": "होइन",
    "ra": "र",
    "ani": "अनि",
    "tara": "तर",
    "yes": "हो",
    "no": "होइन",

    "namaste": "नमस्ते",
    "dhanyabad": "धन्यवाद",
    "dhanyabaad": "धन्यवाद",
    "kripaya": "कृपया",
    "sanchai": "सन्चै",
    "bhetau": "भेटौँ",
}
def roman_to_nepali_text(text):
    words = text.lower().split()

    converted = []
    for word in words:
        converted.append(
            roman_to_nepali.get(word, word)
        )

    return " ".join(converted)