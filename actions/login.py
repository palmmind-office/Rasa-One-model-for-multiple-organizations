from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json
from actions.facebook_response import convert_to_channel_response


class ActionLogin(Action):

    def name(self) -> Text:
        return "action_login"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_type = tracker.get_slot("user_type")
        channel = tracker.get_latest_input_channel()

        org_type = tracker.latest_message["metadata"].get("type")
        file_path = f'actions/responses/{org_type}/login.json'

        if user_type:
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get(f'{user_type}_login')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]           
            
        else:
            dispatcher.utter_message(
                text=f"Are you an agent or a policyholder?",
                buttons=[
                    {
                        "title": "Agent",
                        "payload": f"/login{{\"user_type\":\"agent\"}}"
                    },
                    {
                        "title": "Policy Holder",
                        "payload": f"/login{{\"user_type\":\"policy holder\"}}"
                    }
                ]
            )
            return[]   


class ResetLogin(Action):
    def name(self):
        return "action_reset_login"

    def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("user_type", None),
            SlotSet("insurance_info", None)
        ]
