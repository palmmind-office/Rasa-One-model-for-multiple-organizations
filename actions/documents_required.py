from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json
from actions.facebook_response import convert_to_channel_response


class ActionDocumentsRequired(Action):

    def name(self) -> Text:
        return "action_documents_required"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_type = tracker.get_slot("user_type")
        category = tracker.get_slot("category")
        insurance_info = tracker.get_slot("insurance_info")
        claim_type = tracker.get_slot("claim_type")
        channel = tracker.get_latest_input_channel()

        org_type = tracker.latest_message["metadata"].get("type")
        file_path = f'actions/responses/{org_type}/documents_required.json'

        if insurance_info == "endorsement":
            response = {
                "type": "quick_reply",
                "title": f"Following are the documents required for Policy Endorsement:<br>1.Application of assured<br>2.Original policy bond<br>3.Other related documents"
            }
            convert_to_channel_response(
                dispatcher, rasa_response=response, channel=channel)
            return[]

        if category == "revive":
            response = {
                "type": "quick_reply",
                "title": "Following are the documents required for revival of lapsed policy:<br>1.Application of assured<br>2.Personal Health Declaration Form<br>3.Medical Report"
            }
            convert_to_channel_response(
                dispatcher, rasa_response=response, channel=channel)
            return[]

        if insurance_info == "duplicate":
            response = {
                "type": "quick_reply",
                "title": "Following are the documents required to duplicate policy if lost or destroyed:<br>1.Application of assured<br>2.Original of 35 days' notice.<br>3.Deposit Bank voucher of Rs200 deposited in Company's Account"
            }
            convert_to_channel_response(
                dispatcher, rasa_response=response, channel=channel)
            return[]

        if insurance_info == "purchase":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('policy_issue')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]

        if user_type == "agent":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('agent_qualifications')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]

        if insurance_info == "claim":
            if claim_type == "death":
                try:
                    with open(file_path, 'r', encoding='utf8') as f:
                        data = json.load(f)
                        response = data.get('death_claim_payment')
                        convert_to_channel_response(
                            dispatcher, rasa_response=response, channel=channel)
                        return []
                except Exception as error:
                    print(error)
                return[]
            elif claim_type == "maturity":

                response = {
                    "type": "quick_reply",
                    "title":
                    "Following are the documents required for maturity claim payment:<br>1.Application of assured<br>2.Original policy bond<br>3.Last premium paid receipt<br>4.Copy of citizenship certificate"
                }
                convert_to_channel_response(
                    dispatcher, rasa_response=response, channel=channel)
                return[]

            else:
                dispatcher.utter_message(
                    text=f"Please select whether it is death claim or maturity claim.",
                    buttons=[{
                        "title": "Death Claim",
                        "payload": f"/documents_required{{\"insurance_info\":\"claim\",\"claim_type\":\"death\"}}"
                    },
                        {
                        "title": "Maturity Claim",
                        "payload": f"/documents_required{{\"insurance_info\":\"claim\",\"claim_type\":\"maturity\"}}"
                    }]
                )
                return[]
        if insurance_info == "survival benefit":
            response = {
                "type": "quick_reply",
                "title":
                "Following are the documents required to get the payment of survival benefit:<br>1.Application of assured<br>2.Copy of Citizenship Certificate<br>3.Bank Account No. of policyholder"
            }
            convert_to_channel_response(
                dispatcher, rasa_response=response, channel=channel)
            return[]

        if insurance_info == "loan":
            response = {
                "type": "quick_reply",
                "title":
                "Following are the documents required to get policy loan against policy bond:<br>1.Application of assured<br>2.Original Policy Bond<br>3.Last premium paid receipt<br>4.Copy of citizenship certificate"
            }
            convert_to_channel_response(
                dispatcher, rasa_response=response, channel=channel)
            return[]

        if insurance_info == "surrender":
            response = {
                "type": "quick_reply",
                "title":
                "Following are the documents required to get Surrender/Paid up value payment:<br>1.Application of assured<br>2.Original Policy bond<br>3.Last premium paid receipt<br>4.Copy of citizenship certificate"
            }
            convert_to_channel_response(
                dispatcher, rasa_response=response, channel=channel)
            return[]

        if insurance_info == "training":
            response = {
                "type": "quick_reply",
                "title":
                "Following are the documents required for agent training and appointment:<br>1.Copy of Citizenship certificate<br>2.Copy of Character Certificate of SLC/SEE<br>3.Copy of Marksheet of SLC/SEE<br>(All copy of documents must be notarized)<br>4.PP sized photograph"
            }
            convert_to_channel_response(
                dispatcher, rasa_response=response, channel=channel)
            return[]
        else:
            buttons = [
                {"title": "Purchase a policy",
                    "payload": f"/documents_required{{\"insurance_info\":\"purchase\"}}"},
                {"title": "Become Agent",
                    "payload": f"/documents_required{{\"user_type\":\"agent\"}}"},
                {"title": "Death Claim",
                    "payload": f"/documents_required{{\"insurance_info\":\"claim\",\"claim_type\":\"death\"}}"},
                {"title": "Maturity Claim",
                    "payload": f"/documents_required{{\"insurance_info\":\"claim\",\"claim_type\":\"maturity\"}}"},
                {"title": "Policy Loan",
                    "payload": f"/documents_required{{\"insurance_info\":\"loan\"}}"},
                {"title": "Agent Training",
                    "payload": f"/documents_required{{\"insurance_info\":\"training\"}}"},
                {"title": "Surrender Value Payment",
                    "payload": f"/documents_required{{\"insurance_info\":\"surrender\"}}"},
                {"title": "Revive Lapsed policy",
                    "payload": f"/documents_required{{\"category\":\"revive\"}}"}
            ]

            response = {
                "title": "Click the buttons below to know about the necessary documents for various purposes:",
                "type": "quick_reply",
                "multi": True,
                "data": buttons
            }
            convert_to_channel_response(
                dispatcher, rasa_response=response, channel=channel)
            return[]


class ResetDocumentsRequired(Action):
    def name(self):
        return "action_reset_documents_required"

    def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("insurance_info", None),
            SlotSet("claim_type", None),
            SlotSet("user_type", None),
            SlotSet("category", None)
        ]
