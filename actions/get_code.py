from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher


class ActionGetCode(Action):

    def name(self) -> Text:
        return "action_get_code"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text="Dear Customer, if you have forgot or lost your details such as policy number or agent code, please visit or contact our nearest branch.",
            buttons=[
                {
                    "title": "Branch",
                    "payload": f"/contact{{\"office_type\":\"branch office\"}}"
                }]
        )
        return[SlotSet("user_type", None),
               SlotSet("insurance_info", None)]
