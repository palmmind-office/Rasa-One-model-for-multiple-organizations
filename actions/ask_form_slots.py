from typing import Dict, Text, List

from rasa_sdk import Tracker
from rasa_sdk.events import EventType, SlotSet, ActiveLoop
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action
from actions.facebook_response import convert_to_channel_response


class AskPolicyNoAction(Action):
    def name(self) -> Text:
        return "action_ask_policyNo"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        channel = tracker.get_latest_input_channel()
        form_asked_counter = tracker.get_slot("form_asked_counter") or 0

        print(form_asked_counter, "===form_asked_counter")

        if form_asked_counter >= 2:
            message = {
                "text": "Your Policy Number Invalid attempt exceeded. Please try again in an hour..",
                "is_form": True,
            }
            convert_to_channel_response(
                dispatcher, rasa_response=message, channel=channel
            )
            return [ActiveLoop(None)]
        if form_asked_counter == 0:
            message = {
                "text": "Please enter your Policy number.",
                "is_form": True,
            }
            convert_to_channel_response(
                dispatcher, rasa_response=message, channel=channel
            )
            form_asked_counter = form_asked_counter + 1
            return [SlotSet("form_asked_counter", form_asked_counter)]


class AsklastNameAction(Action):
    def name(self) -> Text:
        return "action_ask_lastName"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        channel = tracker.get_latest_input_channel()

        response = {
            "title": "Please enter your Last Name.",
            "type": "quick_reply",
            "multi": True,
            "is_form": True,
        }
        convert_to_channel_response(dispatcher, rasa_response=response, channel=channel)
        return []


class AskBirthYearAction(Action):
    def name(self) -> Text:
        return "action_ask_birthYear"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        channel = tracker.get_latest_input_channel()

        form_asked_counter = tracker.get_slot("form_asked_counter") or 0

        print(form_asked_counter, "===form_asked_counter")

        if form_asked_counter >= 2:
            message = {
                "text": "Your Birth Year Invalid attempt exceeded. Please try again in an hour..",
                "is_form": True,
            }
            convert_to_channel_response(
                dispatcher, rasa_response=message, channel=channel
            )
            return [ActiveLoop(None)]
        else:
            message = {
                "text": "Please enter your Birth Year.",
                "is_form": True,
            }
            convert_to_channel_response(
                dispatcher, rasa_response=message, channel=channel
            )
            form_asked_counter = form_asked_counter + 1
            return [SlotSet("form_asked_counter", form_asked_counter)]


class AskAgentIdAction(Action):
    def name(self) -> Text:
        return "action_ask_agentId"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        channel = tracker.get_latest_input_channel()

        form_asked_counter = tracker.get_slot("form_asked_counter") or 0

        print(form_asked_counter, "===form_asked_counter")

        if form_asked_counter >= 2:
            message = {
                "text": "Your Agent ID Invalid attempt exceeded. Please try again in an hour..",
                "is_form": True,
            }
            convert_to_channel_response(
                dispatcher, rasa_response=message, channel=channel
            )
            return [ActiveLoop(None)]
        if form_asked_counter == 0:
            message = {
                "text": "Please enter your Agent ID.",
                "is_form": True,
            }
            convert_to_channel_response(
                dispatcher, rasa_response=message, channel=channel
            )
            form_asked_counter = form_asked_counter + 1
            return [SlotSet("form_asked_counter", form_asked_counter)]


class AskFromDateAction(Action):
    def name(self) -> Text:
        return "action_ask_from_date"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        channel = tracker.get_latest_input_channel()
        form_asked_counter = tracker.get_slot("form_asked_counter") or 0

        print(form_asked_counter, "===form_asked_counter")

        if form_asked_counter >= 2:
            message = {
                "text": "Your Invalid attempt has exceeded. Please try again in an hour..",
                "is_form": True,
            }
            convert_to_channel_response(
                dispatcher, rasa_response=message, channel=channel
            )
            return [ActiveLoop(None)]
        else:
            message = {
                "text": "Please enter the starting date with format (YYYY-MM-DD) in AD.",
                "is_form": True,
            }
            convert_to_channel_response(
                dispatcher, rasa_response=message, channel=channel
            )
            form_asked_counter = form_asked_counter + 1
            return [SlotSet("form_asked_counter", form_asked_counter)]


class AskToDateAction(Action):
    def name(self) -> Text:
        return "action_ask_to_date"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        channel = tracker.get_latest_input_channel()
        form_asked_counter = tracker.get_slot("form_asked_counter") or 0

        print(form_asked_counter, "===form_asked_counter")

        if form_asked_counter >= 2:
            message = {
                "text": "Your Invalid attempt has exceeded. Please try again in an hour..",
                "is_form": True,
            }
            convert_to_channel_response(
                dispatcher, rasa_response=message, channel=channel
            )
            return [ActiveLoop(None)]
        else:
            message = {
                "text": "Please enter the last date with format (YYYY-MM-DD) in AD.",
                "is_form": True,
            }
            convert_to_channel_response(
                dispatcher, rasa_response=message, channel=channel
            )
            form_asked_counter = form_asked_counter + 1
            return [SlotSet("form_asked_counter", form_asked_counter)]


class AskAgent_IDAction(Action):
    def name(self) -> Text:
        return "action_ask_agent_id"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        channel = tracker.get_latest_input_channel()

        form_asked_counter = tracker.get_slot("form_asked_counter") or 0

        print(form_asked_counter, "===form_asked_counter")

        if form_asked_counter >= 2:
            message = {
                "text": "Your Agent ID Invalid attempt exceeded. Please try again in an hour..",
                "is_form": True,
            }
            convert_to_channel_response(
                dispatcher, rasa_response=message, channel=channel
            )
            return [ActiveLoop(None)]
        if form_asked_counter == 0:
            message = {
                "text": "Please enter your Agent ID.",
                "is_form": True,
            }
            convert_to_channel_response(
                dispatcher, rasa_response=message, channel=channel
            )
            form_asked_counter = form_asked_counter + 1
            return [SlotSet("form_asked_counter", form_asked_counter)]


class AskLast_nameAction(Action):
    def name(self) -> Text:
        return "action_ask_last_name"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        channel = tracker.get_latest_input_channel()

        response = {
            "title": "Please enter your Last Name.",
            "type": "quick_reply",
            "multi": True,
            "is_form": True,
        }
        convert_to_channel_response(dispatcher, rasa_response=response, channel=channel)
        return []


class AskDOBAction(Action):
    def name(self) -> Text:
        return "action_ask_dob"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        channel = tracker.get_latest_input_channel()
        form_asked_counter = tracker.get_slot("form_asked_counter") or 0

        print(form_asked_counter, "===form_asked_counter")

        if form_asked_counter >= 2:
            message = {
                "text": "Your Invalid attempt exceeded. Please try again in an hour..",
                "is_form": True,
            }
            convert_to_channel_response(
                dispatcher, rasa_response=message, channel=channel
            )
            return [ActiveLoop(None)]
        else:
            message = {
                "text": "Please enter your Date of Birth with format (YYYY-MM-DD) in AD.",
                "is_form": True,
            }
            convert_to_channel_response(
                dispatcher, rasa_response=message, channel=channel
            )
            form_asked_counter = form_asked_counter + 1
            return [SlotSet("form_asked_counter", form_asked_counter)]


class AskFeedbackComplaintsFullNameAction(Action):
    def name(self) -> Text:
        return "action_ask_feedback_complaints_full_name"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        channel = tracker.get_latest_input_channel()

        response = {
            "title": "Please provide your full name.",
            "type": "quick_reply",
            "multi": True,
            "is_form": True,
        }
        convert_to_channel_response(dispatcher, rasa_response=response, channel=channel)
        return []


class AskFeedbackComplaintsPhoneNumberAction(Action):
    def name(self) -> Text:
        return "action_ask_feedback_complaints_phone_number"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        channel = tracker.get_latest_input_channel()
        form_asked_counter = tracker.get_slot("form_asked_counter") or 0

        print(form_asked_counter, "===form_asked_counter")

        if form_asked_counter >= 2:
            message = {
                "title": "Your Phone Number Invalid attempt exceeded. Please try again in an hour..",
                "type":"quick_reply",
                "is_form": True,
            }
            convert_to_channel_response(
                dispatcher, rasa_response=message, channel=channel
            )
            return [ActiveLoop(None)]
        if form_asked_counter == 0:
            message = {
                "title": "Please provide your phone number.",
                "type":"quick_reply",
                "is_form": True,
            }
            convert_to_channel_response(
                dispatcher, rasa_response=message, channel=channel
            )
        form_asked_counter = form_asked_counter + 1
        return [SlotSet("form_asked_counter", form_asked_counter)]


class AskFeedbackComplaintsEmailAction(Action):
    def name(self) -> Text:
        return "action_ask_feedback_complaints_email"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        channel = tracker.get_latest_input_channel()
        form_asked_counter = tracker.get_slot("form_asked_counter") or 0

        print(form_asked_counter, "===form_asked_counter")

        if form_asked_counter >= 2:
            message = {
                "title": "Your email Invalid attempt exceeded. Please try again in an hour..",
                "type":"quick_reply",
                "is_form": True,
            }
            convert_to_channel_response(
                dispatcher, rasa_response=message, channel=channel
            )
            return [ActiveLoop(None)]
        else:
            message = {
                "title": "Please provide your email.",
                "type":"quick_reply",
                "is_form": True,
            }
            convert_to_channel_response(
                dispatcher, rasa_response=message, channel=channel
            )
            form_asked_counter = form_asked_counter + 1
            return [SlotSet("form_asked_counter", form_asked_counter)]


class AskFeedbackComplaintsProblemsAction(Action):
    def name(self) -> Text:
        return "action_ask_feedback_complaints_problems"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        channel = tracker.get_latest_input_channel()

        response = {
            "title": "Please provide your problem/complain.",
            "type": "quick_reply",
            "multi": True,
            "is_form": True,
        }
        convert_to_channel_response(dispatcher, rasa_response=response, channel=channel)
        return []


class AskFeedbackComplaintsSuggestionsAction(Action):
    def name(self) -> Text:
        return "action_ask_feedback_complaints_suggestions"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        channel = tracker.get_latest_input_channel()

        response = {
            "title": "Please provide your suggestion/feedback.",
            "type": "quick_reply",
            "multi": True,
            "is_form": True,
        }
        convert_to_channel_response(dispatcher, rasa_response=response, channel=channel)
        return []


class AskLeadInterestAction(Action):
    def name(self) -> Text:
        return "action_ask_lead_interest"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        channel = tracker.get_latest_input_channel()

        response = {
            "title": "Please provide your query/interest.",
            "type": "quick_reply",
            "multi": True,
            "is_form": True,
        }
        convert_to_channel_response(dispatcher, rasa_response=response, channel=channel)
        return []


class ThankComplaintAction(Action):
    def name(self) -> Text:
        return "action_thankyou_for_complaint"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        feedback_complaints_full_name = tracker.get_slot(
            "feedback_complaints_full_name"
        )

        message = {
            "text": f"Thank you {feedback_complaints_full_name} for providing your complain.",
            "is_form": True,
        }
        dispatcher.utter_message(json_message=message)
        return []


class ThankInfoAction(Action):
    def name(self) -> Text:
        return "action_thankyou_for_info"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        feedback_complaints_full_name = tracker.get_slot(
            "feedback_complaints_full_name"
        )

        message = {
            "text": f"Thank you, {feedback_complaints_full_name} for taking the time to provide your information. A representative from our team will be in touch with you shortly. We appreciate your interest and look forward to speaking with you.",
            "is_form": True,
        }
        dispatcher.utter_message(json_message=message)
        return []


class ThankInterestAction(Action):
    def name(self) -> Text:
        return "action_thankyou_for_interest"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        feedback_complaints_full_name = tracker.get_slot(
            "feedback_complaints_full_name"
        )

        message = {
            "text": f"Thank you, {feedback_complaints_full_name} for your interest in our products. A representative from our team will be in touch with you shortly. We appreciate your interest and look forward to speaking with you.",
            "is_form": True,
        }
        dispatcher.utter_message(json_message=message)
        return []
