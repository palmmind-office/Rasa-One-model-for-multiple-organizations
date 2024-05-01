from typing import Any, Dict, List, Optional, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
from rasa_sdk.events import SlotSet


class ActionMenu(Action):
    def name(self) -> Text:
        return "action_menu"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:

        channel = tracker.get_latest_input_channel()

        org_type = tracker.latest_message["metadata"].get("type")
        file_path = f'actions/responses/{org_type}/menu.json'

        print("This is channel:", channel)

        if channel:
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get(f'menu_{channel}')
                    dispatcher.utter_message(json_message=response)
            except Exception as error:
                print(error)
            return[]

class ResetMenu(Action):
    def name(self):
        return "action_reset_menu"

    def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("user_type", None),
            SlotSet("branch_type", None),
            SlotSet("company_info", None),
            SlotSet("document", None),
            SlotSet("feedback_type", None),
            SlotSet("insurance_info", None),
            SlotSet("action", None),
            SlotSet("product_type", None),
            SlotSet("category", None),
            SlotSet("payment_option", None),
            SlotSet("social_media", None),
            SlotSet("bank_name", None),
            SlotSet("wallet_name", None),
            SlotSet("claim_type", None),
            SlotSet("office_type", None),
            SlotSet("policyNo", None),
            SlotSet("lastName", None),
            SlotSet("birthYear", None),
            SlotSet("agentId", None),
            SlotSet("from_date", None),
            SlotSet("to_date", None),
            SlotSet("agent_id", None),
            SlotSet("last_name", None),
            SlotSet("dob", None),
            SlotSet("feedback_complaints_email", None),
            SlotSet("feedback_complaints_suggestions", None),
            SlotSet("feedback_complaints_problems", None),
            SlotSet("form_asked_counter", None),
            SlotSet("lead_interest", None)
        ]
