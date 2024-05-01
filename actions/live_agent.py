from typing import Any, Dict, List, Optional, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
from rasa_sdk.events import SlotSet


class ActionLiveAgent(Action):
    def name(self) -> Text:
        return "action_live_agent"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:

        button = [{"title": "Talk to Live Agent",
                   "payload": "livechat:request:all"}]

        dispatcher.utter_message(
            text=f"If you would like to speak with one of our live agents during our office hours (10:00 am to 5:00 pm), please click the button below.",
            buttons=button
        )
        return[SlotSet("user_type", None),
               SlotSet("insurance_info", None)]
