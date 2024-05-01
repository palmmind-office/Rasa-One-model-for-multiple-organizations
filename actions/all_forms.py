from typing import Text, List, Any, Dict

from rasa_sdk import Tracker, Action, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.events import SlotSet, FollowupAction
import re
from actions.actionServices.leadCaptureService import DashboardPost
from actions.actionServices.feedbackService import FeedbackComplaintPost
import os



class resetFeedbackComplaintsForm(Action):
    def name(self):
        return "action_reset_feedback_complaints_slot"

    def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("feedback_complaints_suggestions", None),
            SlotSet("feedback_complaints_problems", None),
            SlotSet("form_asked_counter", None),
            SlotSet("lead_interest", None)]


class ValidateFeedbackComplaintsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_feedback_complaints_form"

    def validate_feedback_complaints_full_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:
        feedback_complaints_full_name = tracker.get_slot(
            "feedback_complaints_full_name")
        is_valid_name = re.match(
            r'^[a-zA-Z]{2,}( {1,2}[a-zA-Z]{2,}){0,}$', feedback_complaints_full_name)
        if len(feedback_complaints_full_name) == 0:
            dispatcher.utter_message(text="Full Name is required.")
            return {"feedback_complaints_full_name": None}
        if is_valid_name is None:
            dispatcher.utter_message(text="Please give valid Name")
            return {"feedback_complaints_full_name": None}
        return {"feedback_complaints_full_name": feedback_complaints_full_name}

    def validate_feedback_complaints_phone_number(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:
        mobile_email = tracker.get_slot("feedback_complaints_phone_number")
        is_valid_mobile_email = re.match(
            r'^(\+?\d{1,3})?(\d{10})$', mobile_email)
        if len(mobile_email) == 0:
            dispatcher.utter_message(text="Phone No is required.")
            return {"feedback_complaints_phone_number": None}
        if(is_valid_mobile_email is None):
            dispatcher.utter_message(text="Invalid contact number.")
            return {"feedback_complaints_phone_number": None}
        return {"feedback_complaints_phone_number": mobile_email}

    def validate_feedback_complaints_email(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:
        email = tracker.get_slot("feedback_complaints_email")
        print(email, "feedback_complaints_email>>>>>>>>>>>>>>>>>>>>>>>")
        is_valid_email = re.match(
            r'^\w+([.-]?\w+)@\w+([.-]?\w+)(.\w{2,3})+$', email)
        if len(email) == 0:
            dispatcher.utter_message(text="Email is required.")
            return {"feedback_complaints_email": None}
        if(is_valid_email is None):
            dispatcher.utter_message(text="Invalid Email.")
            return {"feedback_complaints_email": None}
        return {"feedback_complaints_email": email}

    async def required_slots(
        self,
        domain_slots: List[Text],
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: "DomainDict",
    ) -> List[Text]:
        additional_slots = []
        feedback_type = tracker.get_slot("feedback_type")

        if(feedback_type == 'feedback'):
            additional_slots.append("feedback_complaints_suggestions")
            return additional_slots + domain_slots

        elif feedback_type == "callback":
            additional_slots.append("lead_interest")
            return additional_slots + domain_slots
        elif feedback_type == "buy_policy":
            return domain_slots
        elif(feedback_type == 'complain'):
            additional_slots.append("feedback_complaints_problems")
            return additional_slots + domain_slots
        elif feedback_type == None:
            additional_slots.append("feedback_complaints_problems")
            return additional_slots + domain_slots

    def validate_feedback_complaints_problems(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:
        feedback_complaints_problems = tracker.get_slot(
            "feedback_complaints_problems")
        return {"feedback_complaints_problems": feedback_complaints_problems}

    def validate_feedback_complaints_suggestions(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:
        feedback_complaints_suggestions = tracker.get_slot(
            "feedback_complaints_suggestions")
        return {"feedback_complaints_suggestions": feedback_complaints_suggestions}

    def validate_lead_interest(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:
        lead_interest = tracker.get_slot(
            "lead_interest")
        return {"lead_interest": lead_interest}

class ActionFeedbackSubmit(Action):
    def name(self) -> Text:
        return "action_feedback_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        customerName = tracker.get_slot("feedback_complaints_full_name")
        source = tracker.get_latest_input_channel()
        phonenumber = tracker.get_slot("feedback_complaints_phone_number")
        sender_id = tracker.sender_id
        org_type=tracker.latest_message['metadata'].get('type')
        form_asked_counter=tracker.get_slot("form_asked_counter")
        if form_asked_counter==2:
            dispatcher.utter_message(text="Please ask me the queries related to life insurance, agent benefits, policies, etc.")
            return[FollowupAction("action_listen"), SlotSet("form_asked_counter", None)]

        print("I am inside forms")
        if tracker.slots.get("feedback_type", None) == "feedback":
            source = tracker.get_latest_input_channel()
            source = 'Web' if source == 'rest' else source
            print("This is viber source", source)
            feedback = {
                'full_name': customerName,
                'mobile_number': tracker.get_slot("feedback_complaints_phone_number"),
                'email_address': tracker.get_slot("feedback_complaints_email"),
                'suggestion': tracker.get_slot("feedback_complaints_suggestions"),
                "organizationId": os.getenv('ORGANIZATION_ID')
            }
            print("This is ffedback")
            obj = FeedbackComplaintPost(org_type)
            obj.DASHBOARD_POST_FEEDBACK(feedback,sender_id)
            # obj.SENDEMAIL_FEEDBACK(feedback)
           
            dispatcher.utter_message(
                text=f"Thank you {customerName} for providing your valuable feedback.")
            
        elif tracker.slots.get("feedback_type", None) == "complain" or tracker.slots.get("feedback_type", None) == None:
            source = tracker.get_latest_input_channel()
            source = 'Web' if source == 'rest' else source
            complaints = {
                'full_name': customerName,
                'mobile_number': tracker.get_slot("feedback_complaints_phone_number"),
                'email_address': tracker.get_slot("feedback_complaints_email"),
                'title': tracker.get_slot("feedback_complaints_problems"),
                'problem': tracker.get_slot("feedback_complaints_problems"),
                "organizationId": os.getenv('ORGANIZATION_ID')
            }
            obj = FeedbackComplaintPost(org_type)
            obj.DASHBOARD_POST_COMPLAINTS(complaints,sender_id)
            # obj.SENDEMAIL_FEEDBACK(complaints)
           
            dispatcher.utter_message(
                text=f"Thank you {customerName} for providing your complain.")
            
                    
        if tracker.slots.get("feedback_type", None) == "callback":
            source = tracker.get_latest_input_channel()
            source = 'Web' if source == 'rest' else source
            lead = {
                'fullname': customerName,
                'mobile': tracker.get_slot("feedback_complaints_phone_number"),
                'email': tracker.get_slot("feedback_complaints_email"),
                'description': "",
                'source': source,
                'visitorId': tracker.sender_id,
                'location': '',
              
                'interest': tracker.get_slot("lead_interest")
            }

            buttons = [
                {"title": "Menu", "payload": "/menu"}
            ]

            Obj=DashboardPost(org_type)
            Obj.DASHBOARD_POST_LEAD(lead)
            # Obj.SENDEMAIL(lead)

            dispatcher.utter_message(
                text=f"Thank you, {customerName} for taking the time to provide your information. A representative from our team will be in touch with you shortly. We appreciate your interest and look forward to speaking with you.",
                buttons=buttons
            )
            
        if tracker.slots.get("feedback_type", None) == "buy_policy":
            source = tracker.get_latest_input_channel()
            source = 'Web' if source == 'rest' else source
            product_type = tracker.get_slot("product_type")
            if product_type is not None:
                abc = f"Purchase {product_type} Plan"
            else:
                abc = f"Insurance Purchase"
            lead = {
                'fullname': customerName,
                'mobile': tracker.get_slot("feedback_complaints_phone_number"),
                'email': tracker.get_slot("feedback_complaints_email"),
                'description': "",
                'source': source,
                'visitorId': tracker.sender_id,
                'location': '',
                'interest': abc
                
            }
            dispatcher.utter_message(
                text=f"Thank you {customerName} for your interest in our products. A  representative from our team will be in touch with you shortly.")

            Obj=DashboardPost(org_type)
            Obj.DASHBOARD_POST_LEAD(lead)
            # Obj.SENDEMAIL(lead)