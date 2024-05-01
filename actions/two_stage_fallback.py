from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted


class ActionTwoStageFallback(Action):
    def name(self):
        return "action_two_stage_fallback"

    async def run(self, dispatcher, tracker, domain):
       
        predicted_intents = tracker.latest_message["intent_ranking"][1:3]
        message = "Sorry, I'm not sure I've understood you correctly. Do you mean:"

        excluded_intents = ["greet", "goodbye",
                            "thankyou", "out_of_scope", "faq"]

        intent_mappings = {
            "agency": "Agency",
            "agent_login": "Agent Login",
            "become_agent": "Become Agent",
            "benefits": "Benefits",
            "callback": "Get a Callback",
            "cancel_subscription": "Cancel Subscription",
            "file_a_claim": "File a Claim",
            "about_claim": "About Claim",
            "careers": "Careers",
            "company_profile": "Company Profile",
            "contact": "Branches and Contact",
            "documents_required": "Documents Required",
            "downloads": "Download Forms",
            "feedback": "Complains and Feedback",
            "faq": "FAQ",
            "live_agent": "Talk to Live Agent",
            "loan": "Loan",
            'login': "Login",
            "menu": "Main menu",
            "office_time": "Office Time",
            "offers": "Offers",
            "payment": "Payment",
            "policy": "Policy Details",
            "premium_calculation": "Premium Calculation",
            "product_info": "Product Information",
            "purchase": "Purchase",
            "update_profile": "Update Profile",
            "view_details": "View Details",
            "greet": "Greet",
            "goodbye": "Goodbye",
            "thankyou": "Thank You",
            "out_of_scope": "Out of Scope"
        }

        buttons = []
        for intent in predicted_intents:
            if intent.get("name") not in excluded_intents:
                buttons.append(
                    {
                        "title": intent_mappings[intent['name']],
                        "payload": "/{}".format(intent['name'])
                    }
                )

        buttons.append({
            "title": "None of These",
            "payload": "/out_of_scope"
        })
        dispatcher.utter_message(text=message, buttons=buttons)
        return [UserUtteranceReverted()]
