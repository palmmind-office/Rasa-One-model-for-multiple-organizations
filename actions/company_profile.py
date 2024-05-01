from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json
from actions.facebook_response import convert_to_channel_response


class ActionCompanyProfile(Action):

    def name(self) -> Text:
        return "action_company_profile"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        company_info = tracker.get_slot("company_info")
        channel = tracker.get_latest_input_channel()

        org_type = tracker.latest_message["metadata"].get("type")

        file_path = f'actions/responses/{org_type}/company_profile.json'
        
        if company_info == "ceo":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('ceo')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]
        
        else:
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('about_company')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]



class ResetCompanyProfile(Action):
    def name(self):
        return "action_reset_company_profile"

    def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("company_info", None),
            SlotSet("user_type", None)
        ]
