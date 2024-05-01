from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json
from actions.facebook_response import convert_to_channel_response


class ActionPremiumCalculation(Action):

    def name(self) -> Text:
        return "action_premium_calculation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        channel = tracker.get_latest_input_channel()

        org_type = tracker.latest_message["metadata"].get("type")
        file_path = f'actions/responses/{org_type}/premium_calculation.json'


        response = {
            "title": "The cost of life insurance is typically based on factors such as:<br>• Age, sex, height and weight<br>• Health status, including whether or not you smoke<br>• Participation in high-risk occupations",
            "type": "quick_reply"}
        convert_to_channel_response(
            dispatcher, rasa_response=response, channel=channel)

        try:
            with open(file_path, 'r', encoding='utf8') as f:
                data = json.load(f)
                response = data.get('premium_calculation')
                convert_to_channel_response(
                    dispatcher, rasa_response=response, channel=channel)
                return []
        except Exception as error:
            print(error)
        return[]

