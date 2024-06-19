import requests
import logging

def translate_text(text, dest="de"):
    url = "https://api.mymemory.translated.net/get"
    params = {
        "q": text,
        "langpair": f"en|{dest}"
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        result = response.json()
        translated_text = result["responseData"]["translatedText"]
        return translated_text
    else:
        logging.error(f"Translation Error: {response.status_code} {response.reason}")
        return f"Translation Error: {response.status_code} {response.reason}"
