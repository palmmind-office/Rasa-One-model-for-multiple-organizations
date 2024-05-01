from services.redis import setData, getData, flushAll
from services.httpService import http_post
import json
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())
import re


TEXT_CONVERTER_SERVICE = os.getenv('TEXT_CONVERTER_SERVICE')
TEXT_CONVERTER_KEY = os.getenv('TEXT_CONVERTER_KEY')


def CONVERTER_SERVICE(text):
    redisKey = text
    try:
        with open("services/text_converter_dict.json", "r") as f:
            data = json.load(f)
            url = f"{TEXT_CONVERTER_SERVICE}?text={text}&key={TEXT_CONVERTER_KEY}"
            headers = {'content-type': 'application/json'}
            response = http_post(url, headers, data)
            print("=========text-converter=======/n", response,
                  "/n", "=========text-converter=======")
            text = response.get('text', text)
            setData(redisKey, response)
    except Exception as error:
        print(error)
        return text

    finally:
        synonanmes = {"interest": ["byazz", "byazdar", "biyaz", "byaj", "%", "biyaj", "vyaj", "vyaaj", "biyaaj", "viyaaj", "viyaj", "vyajdar", "vyajdr", "biyajdr", "biyajdar", "percent", "percentage"],
                      "account": ["khta", "katha", "a/c"],
                      "balance": ["paisa", "rakam"],
                      "child": ["baccha", "bacha", "bcci", "bcchako", "nanilai", "chorilai", "chorilai", "chhorilai", "choralai", "xorilai", "xoralai", "naniko", "babulai", "chhora", "babuko", "choriko", "chhoriko", "chorako", "chhorako", "xoriko", "xorako", "bcchhako", "bacchako", "xora", "chora", "chhora", "xora", "newborn", "teen", "childen", "babies", "daughter", "son", "baal", "minor", "teenager", "babu", "nani", "xori", "chori", "chhori", "children", "kid", "bcchha", "baccha", "bachha", "bccha", "bcchaa", "kids", "childs", "bachhako", "bacchha"],
                      "feedback": ["advice"],
                      "loan": ["loans"]
                      }
        arrText = text.split(' ')
        for key, values in synonanmes.items():
            for it in values:
                if it in arrText:
                    text = text.replace(it, key)
        return text.lower()


def TEXT_CONVERTER_API(text):
    try:
        with open("services/exclude_convert_list.json", "r") as f:
            data = json.load(f)
            excludeText = data.get("text", [])
            if text in excludeText:
                print("excluded text", text)
                return text
            redisKey = text
            cache = getData(redisKey)
            if(text == "flush cache"):
                flushAll()
                print("=====Flush all data======")
            if "{" in text:
                text = text
                print("=====Not called rasa servce====", text)
            if cache:
                text = cache.get('text', text)
                print("=====rasa cache data======", cache)
            else:
                text = CONVERTER_SERVICE(text)
    except Exception as error:
        print(error)
    finally:
        return text


def http_translator_api(text):
    try:
        regex_pattern = r'\/\w+\s*(?:\{(?:\"[^"]+\"\s*:\s*\"[^"]+\"\s*,?\s*)*\})'
        payload = re.search(regex_pattern, text)
        if text.startswith('/'):
            return text
        else:
            headers = {"content-type": "application/json"}
            # url="http://127.0.0.1:8000/translator"
            url = f"{TEXT_CONVERTER_SERVICE}/translator"
            print(text, url)
            prompt = """
                TASK: Do the following steps: 
                1. Translate the question into the English only if the question is not already in the English Script. 
                2. Do not interpret or change the text. The result should be a straight translation of the question. 
                3. IF THE QUESTION IS ALREADY IN ENGLISH, THEN PRINT ONLY THE QUESTION. 
                Question inside triple backticks:```{question}```
                Provide the translated question with proper contextual understanding, without backticks and nothing else. 
                PROVIDE THE ANSWER IN ENGLISH WITHOUT ``` AND NOTHING ELSE.
                """
            response = http_post(url, headers, {"message": text, "prompt": prompt})
            print(response)
            return response.get("result")
    except Exception as error:
        print("Something has been wrong in dashboard server hai   hh" + str(error))
        return text