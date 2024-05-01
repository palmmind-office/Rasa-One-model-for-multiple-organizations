from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re
from rasa_sdk.events import AllSlotsReset, FollowupAction


class ActionCallback(Action):

    def name(self) -> Text:
        return "action_callback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        return [SlotSet("feedback_type", 'callback'), FollowupAction("feedback_complaints_form")]
    

