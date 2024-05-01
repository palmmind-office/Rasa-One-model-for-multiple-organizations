from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re
from datetime import datetime
from actions.actionServices.httpApi import http_post
from actions.config import config


class resetPolicyForm(Action):
    def name(self):
        return "action_reset_policy_slot"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("policyNo", None), SlotSet("lastName", None), SlotSet("form_asked_counter", None), SlotSet("birthYear", None)]


class ValidatePolicyForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_policy_form"

    def validate_policyNo(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:
        policyNo = tracker.get_slot("policyNo")

        return {"policyNo": policyNo}

    def validate_lastName(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:

        lastName = tracker.get_slot("lastName")
        if lastName.isalpha() == False:
            dispatcher.utter_message(text=f"Please provide a valid last name")
            return {"lastName": None}
        return {"lastName": lastName}

    def validate_birthYear(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:

        birthYear = tracker.get_slot("birthYear")
        try:
            valid_dob = datetime.strptime(birthYear, "%Y")
        except ValueError:
            dispatcher.utter_message(text="Please provide a valid birth year.")
            return {"birthYear": None}

        return {"birthYear": birthYear}


class ActionPolicyFormSubmit(Action):
    def name(self) -> Text:
        return "action_policy_form_submit"

    def premiumResponse(self, type, response):
        botResponse = {}
        if type == "premium":
            botResponse = {
                "type": "detailpolicy",
                "tableData": []
            }
            tableDataPaid = {
                "subtitle": "Paid Installments",
                "for": "bank detil",
                "data": []
            }

            tableDataDue = {
                "subtitle": "Due Installments",
                "for": "bank detil",
                "data": []
            }

            for item in (response.get('paidInstallments')):
                print(len(item))
                print(len(response.get('paidInstallments')))
                tableDataPaid['data'].append({
                    "S.N.": item.get('installmentNo'),
                    "Installment Due Date": item.get("dueDate"),

                    "Basic Premium": item.get("basicPremium"),
                    "Rider Premium": item.get("riderPremium"),
                    "Late Fee": item.get("lateFee"),
                    "Premium": item.get("premium"),
                    "Paid Amount": item.get("paidAmount")

                })
            botResponse['tableData'].append(tableDataPaid)

            for itemm in (response.get('dueInstallments')):
                print(len(itemm))

                tableDataDue['data'].append({
                    "S.N.": itemm.get('installmentNo'),
                    "Installment Due Date": itemm.get("dueDate"),
                    "Basic Premium": itemm.get("basicPremium"),
                    "Rider Premium": itemm.get("riderPremium"),
                    "Late Fee": itemm.get("lateFee"),
                    "Premium": itemm.get("premium"),
                    "Total Due Premium": itemm.get("totalDuePremium")

                })
            botResponse['tableData'].append(tableDataDue)
        return botResponse

    def policyResponse(self, type, response):
        botResponse = {}

        if type == "policy":
            botResponse = {
                "type": "ListItem",
                "title": "You can get your policy details from below.",
                "subtitle": "Policy Details",
                "data": []
            }

            for item in (response.get('policyData')):
                botResponse['data'] = [
                    {
                        "subtitle": f"""Product Name: {item.get('productName')}""",
                    },
                    {
                        "subtitle": f"""Maturity Date: {item.get("maturityDate")}"""
                    },
                    {
                        "subtitle": f"""Sum Assured: {item.get("sumAssured")}"""
                    },
                    {
                        "subtitle": f"""Rider Assured: {item.get("riderAssured")}"""
                    },
                    {
                        "subtitle": f"""Policy Term: {item.get("policyTerm")}"""
                    },
                    {
                        "subtitle": f"""Rider Term: {item.get("riderTerm")}"""
                    },
                    {
                        "subtitle": f"""Paying Term: {item.get('payingTerm')}""",
                    },
                    {
                        "subtitle": f"""Payment Frequency: {item.get("paymentFrequency")}"""
                    },
                    {
                        "subtitle": f"""Last Paid Date: {item.get("lastPaidDate")}"""
                    },
                    {
                        "subtitle": f"""Next Due Date: {item.get("nextDueDate")}"""
                    },
                    {
                        "subtitle": f"""Premium Amount: {item.get("premiumAmount")}"""
                    },
                    {
                        "subtitle": f"""Installment Paid: {item.get("installmentPaid")}"""
                    }
                ]
            return botResponse

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
            
        try:
        
            org_type = tracker.latest_message["metadata"].get("type")
            API_BASE_URL = config[org_type]["api_base_url"]


            category = tracker.get_slot("category")

            policy_details = {
                "policyNo": tracker.get_slot("policyNo"),
                "lastName": tracker.get_slot("lastName"),
                "birthyear": tracker.get_slot("birthYear")
            }

            # call login api
            isAuthorised = http_post("http://202.166.217.166:7878/api/auth/token",
                                    {'content-type': 'application/json'},
                                    {
                                        "username": "primelife",
                                        "password": "testprimelife",
                                        "userType": "string"
                                    })

            token = isAuthorised.get("tokenString")
            headers = {'content-type': 'application/json',
                    'Authorization': f"Bearer {token}"}

            if category == "policy":
                url = API_BASE_URL+"/findPolicy"
                response = http_post(url, headers, policy_details)
                if response != None:
                    data = self.policyResponse(category, response)
                    data['is_form']=True
                    dispatcher.utter_message(json_message=data)
                else:
                    response = {
                    "title": "There is no any details with the provided data. Please re-enter and try again.",
                    "type": "quick_reply",
                    "multi": True,
                    "is_form": True
                    }
                    dispatcher.utter_message(json_message = response)

            elif category == "premium":
                url = API_BASE_URL+"/premiumDetails"
                response = http_post(url, headers, policy_details)
                if response != None:
                    info = self.premiumResponse(category, response)
                    ans = info.get("tableData")
                    info['is_form']=True
                    if not ans[0]['data']:
                        dispatcher.utter_message(
                            text=f"There is no premium details.")
                    else:
                        dispatcher.utter_message(json_message=info)
                else:
                    response = {
                    "title": "There is no any details with the provided data. Please re-enter and try again.",
                    "type": "quick_reply",
                    "multi": True,
                    "is_form": True
                    }
                    dispatcher.utter_message(json_message = response)
                    
        except Exception as e:
            print("Exception: ", e)
