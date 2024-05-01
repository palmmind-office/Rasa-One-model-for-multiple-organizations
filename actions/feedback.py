from typing import Any, Text, Dict, List
from rasa_sdk.events import AllSlotsReset, FollowupAction
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json


class ActionFeedback(Action):

    def name(self) -> Text:
        return "action_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        feedback_type = tracker.get_slot("feedback_type")
        document = tracker.get_slot("document")
        channel = tracker.get_latest_input_channel()

        org_type = tracker.latest_message["metadata"].get("type")
        file_path = f'actions/responses/{org_type}/feedback.json'

        except_web = ["facebook", "instagram", "viber", "whatsapp"]

        if channel != "rest":
            if org_type == "himalayan":
                return [FollowupAction("feedback_complaints_form")]
            
            elif org_type == "reliable":
                dispatcher.utter_message(text = f"Please provide your feedback/complaints and your details as asked below. To assist you further, we will get back to you shortly.")
                return [SlotSet("feedback_type", 'callback'), FollowupAction("feedback_complaints_form")]
            

        else:
            if document == "form":
                if feedback_type == "feedback":
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            response = data.get('feedback')
                            dispatcher.utter_message(json_message=response)
                    except Exception as error:
                        print(error)
                    return[]

                elif feedback_type == "complain":
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            response = data.get('complain')
                            dispatcher.utter_message(json_message=response)
                    except Exception as error:
                        print(error)
                    return[]

            if feedback_type == "feedback":
                dispatcher.utter_message(
                    text=f"Please fill up the given form to provide your valuable feedback.",
                    buttons=[
                        {"title": "Feedback",
                        "payload": f"/feedback{{\"document\":\"form\",\"feedback_type\":\"feedback\"}}"}
                    ])
                return[]

            elif feedback_type == "complain":
                dispatcher.utter_message(
                    text=f"Please fill up the given form to register your complain.",
                    buttons=[
                        {
                            "title": "Complain",
                            "payload": f"/feedback{{\"document\":\"form\",\"feedback_type\":\"complain\"}}"
                        }
                    ])

            else:
                buttons = [
                    {"title": "Feedback",
                    "payload": f"/feedback{{\"document\":\"form\",\"feedback_type\":\"feedback\"}}"},
                    {"title": "Complain",
                    "payload": f"/feedback{{\"document\":\"form\",\"feedback_type\":\"complain\"}}"}]

                dispatcher.utter_message(
                    text=f"Please click the buttons below to register your complain/feedback.",
                    buttons=buttons
                )
                return[]


class ResetFeedback(Action):
    def name(self):
        return "action_reset_feedback"

    def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("feedback_type", None),
            SlotSet("document", None),
            SlotSet("user_type", None)
        ]
