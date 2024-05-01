from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json
from actions.facebook_response import convert_to_channel_response


class ActionDownloads(Action):

    def name(self) -> Text:
        return "action_downloads"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        org_type = tracker.latest_message["metadata"].get("type")
        file_path = f'actions/responses/{org_type}/downloads.json'

        company_info = tracker.get_slot("company_info")
        channel = tracker.get_latest_input_channel()

        if company_info == "app":
            if org_type == "himalayan":
                response = {
                    "title": "You can easily get our app by downloading it from both the Apple Store for iOS users and Google Play for Android users.",
                    "type": "quick_reply",
                    "multi": True,
                    "data": [{
                        "title": "Apple Store",
                        "link": "https://www.apple.com/app-store/"
                    },
                        {
                        "title": "Google Play",
                        "link": "https://play.google.com/store/apps/details?id=com.sourcecode.primelife"
                    }]
                }
                convert_to_channel_response(
                    dispatcher, rasa_response=response, channel=channel)
            else:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                response = data.get('downloads')
                convert_to_channel_response(
                    dispatcher, rasa_response=response, channel=channel)
            return[]

        else:
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('downloads')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]

class ResetDownloads(Action):
    def name(self):
        return "action_reset_downloads"

    def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("company_info", None),
            SlotSet("user_type", None)
        ]
