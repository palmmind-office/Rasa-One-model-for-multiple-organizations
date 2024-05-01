from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json
from actions.facebook_response import convert_to_channel_response

class ActionBecomeAgent(Action):

    def name(self) -> Text:
        return "action_become_agent"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        channel = tracker.get_latest_input_channel()
        org_type = tracker.latest_message["metadata"].get("type")


        file_path = f'actions/responses/{org_type}/become_agent.json'
       
        try:
            with open(file_path, 'r', encoding='utf8') as f:
                data = json.load(f)
                response = data.get('become_agent')
                convert_to_channel_response(
                    dispatcher, rasa_response=response, channel=channel)
                return []
        except Exception as error:
            print(error)
        return[SlotSet("user_type", None)]

