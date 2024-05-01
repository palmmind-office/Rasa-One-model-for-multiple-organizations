from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json


class ActionCancelSubscription(Action):

    def name(self) -> Text:
        return "action_cancel_subscription"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text=f"Cancellation is permissible after three years from the date of commencement, in accordance with the guidelines provided by the Beema Pradikaran directives.")

        dispatcher.utter_message(
            text="You will get cash value (surrender value) of the policy if surrendered. Surrender value amount will be calculated on sum assured, policy term, number of years premium paid, bonus amount, number of years remaining for maturity.")

        dispatcher.utter_message(text="To get the surrender value payment, please contact to our nearest branch with all the necessary documents.",
                                 buttons=[{
                                     "title": "Required Documents",
                                     "payload": f"/documents_required{{\"insurance_info\":\"surrender\"}}"
                                 }]
                                 )
        return [SlotSet("user_type", None)]
