import os
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import re
from datetime import datetime
from actions.actionServices.httpApi import http_post
from actions.config import config


class resetAgentLoginForm(Action):
    def name(self):
        return "action_reset_agent_login_slot"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("agent_id", None), SlotSet("last_name", None), SlotSet("form_asked_counter", None), SlotSet("dob", None)]


class ValidateAgentLoginForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_agent_login_form"

    def validate_agent_id(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:
        agent_id = tracker.get_slot("agent_id")

        return {"agent_id": agent_id}

    def validate_last_name(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:

        last_name = tracker.get_slot("last_name")
        if last_name.isalpha() == False:
            dispatcher.utter_message(text=f"Please provide a valid last name")
            return {"last_name": None}
        return {"last_name": last_name}

    def validate_dob(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:

        dob = tracker.get_slot("dob")
        try:
            valid_dob = datetime.strptime(dob, "%Y-%m-%d")
        except ValueError:
            dispatcher.utter_message(text="Please provide a valid dob.")
            return {"dob": None}

        return {"dob": dob}


class ActionAgentFormSubmit(Action):
    def name(self) -> Text:
        return "action_agent_form_submit"

    def LoginResponse(self, type, response):
        botResponse = {}

        if type == "personal":
            botResponse = {
                "type": "ListItem",
                "title": "You can get your details from below.",
                "subtitle": "Agency Details",
                "data": []
            }

            item = response.get('properties')
            botResponse['data'] = [
                {
                    "subtitle": f"""Agent Name: {item['agentName']}""",
                },
                {
                    "subtitle": f"""Started On: {item["startedON"]}""",
                },
                {
                    "subtitle": f"""License Issued On: {item["licIssuedOn"]}""",
                },
                {
                    "subtitle": f"""Bank Name: {item['bankName']}""",
                },
                {
                    "subtitle": f"""Account Name: {item["accountName"]}""",
                },
                {
                    "subtitle": f"""Account No: {item["accountNo"]}""",
                },
                {
                    "subtitle": f"""Email: {item['email']}""",
                },
                {
                    "subtitle": f"""Pan Number: {item["panNumber"]}""",
                },
                {
                    "subtitle": f"""Agency Type: {item["agencyType"]}""",
                },
                {
                    "subtitle": f"""Reporting Agent: {item['reportingAgent']}""",
                },
                {
                    "subtitle": f"""Status: {item["status"]}""",
                },
                {
                    "subtitle": f"""Expiry Date: {item["expiryDate"]}""",
                }
            ]
        return botResponse

    def downlineResponse(self, type, response):
        botResponse = {}
        if type == "downline":
            botResponse = {
                "type": "detailpolicy",
                "tableData": []
            }
            tableDataPaid = {
                "subtitle": "Agency Downline",
                "for": "bank detil",
                "data": []
            }

            for item in (response.get('agentDownlineProperties')):

                tableDataPaid['data'].append({
                    "S.N.": item.get('sNo'),
                    "Agent ID": item.get("agentId"),
                    "Agent Name": item.get("agentName"),
                    "Superior Code": item.get("superiorCode"),
                    "Branch Code": item.get("branchCode"),
                    "Status": item.get("status"),
                    "Contact No": item.get("contactNo"),
                    "License Issue Date": item.get("licenseIssueDate"),
                    "License Expiry Date": item.get("licenseExpiryDate")
                })
            botResponse['tableData'].append(tableDataPaid)
        return botResponse

    def PremiumDueResponse(self, response):
        botResponse = {
            "type": "detailpolicy",
            "tableData": []
        }
        tableDataPaid = {
            "subtitle": "Agency Premium Due",
            "for": "bank detil",
            "data": []
        }
        for item in (response.get('properties')):
            tableDataPaid['data'].append({
                "Policy No": item.get('policyNo'),
                "Assured": item.get("assured"),
                "Date of Birth": item.get("dob"),

                "Product": item.get("productId"),
                "Policy Term": item.get("policyTerm"),
                "Sum Assured": item.get("sumAssured"),
                "Mobile No": item.get("mobileNo"),
                "Due Date": item.get("dueDate"),
                "Premium": item.get("premium"),
                "Late Fee": item.get("lateFee"),
                "Total Premium": item.get("totalPremium"),
                "Status": item.get("status")
            })
        botResponse['tableData'].append(tableDataPaid)
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

            agent_details = {
                "agentId":  tracker.get_slot("agent_id"),
                "lastName":  tracker.get_slot("last_name"),
                "DOB": tracker.get_slot("dob")
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

            if category == "premium due":
                url = API_BASE_URL+"/agencyPremiumDue"
                response = http_post(url, headers, agent_details)

                if response.get("properties"):
                    data = self.PremiumDueResponse(response)
                    data['is_form']=True
                    ans = data.get("tableData")            
                    if ans[0]['data']:
                        dispatcher.utter_message(json_message=data)
                    else:
                        dispatcher.utter_message(
                            text=f"There is no due premium of any policyholders.")
                else:
                    response = {
                    "title": "There is no any details with the provided data. Please re-enter and try again.",
                    "type": "quick_reply",
                    "multi": True,
                    "is_form": True
                    }
                    dispatcher.utter_message(json_message = response)

            elif category == "downline":
                url = API_BASE_URL+"/agencyDownline"
                response = http_post(url, headers, agent_details)
                if response != None:
                    info = self.downlineResponse(category, response)
                    ans = info.get("tableData")
                    info['is_form']=True
                    if not ans[0]['data']:
                        dispatcher.utter_message(
                            text=f"There is no downline.")
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

            elif category == "personal":
               
                url = API_BASE_URL+"/agencyLogon"
                response = http_post(url, headers, agent_details)
                if response['properties'].get("agentName"):
                    data = self.LoginResponse(category, response)
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

        except Exception as e:
            print("Exception:", e)