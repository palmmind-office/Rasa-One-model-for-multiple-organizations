from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json
from actions.facebook_response import convert_to_channel_response


class ActionBenefits(Action):

    def name(self) -> Text:
        return "action_benefits"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        insurance_info = tracker.get_slot("insurance_info")
        user_type = tracker.get_slot("user_type")
        channel = tracker.get_latest_input_channel()

        org_type = tracker.latest_message["metadata"].get("type")

        file_path = f'actions/responses/{org_type}/benefits.json'

        if insurance_info == "critical illness":
            
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('critical_illness')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]

        if user_type == "agent":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('agent_benefits')
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
                    response = data.get('insurance_benefits')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]


class ResetBenefits(Action):
    def name(self):
        return "action_reset_benefits"

    def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("insurance_info", None),
            SlotSet("user_type", None)
        ]
