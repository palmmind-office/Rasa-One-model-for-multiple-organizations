from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.types import DomainDict
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import os
from datetime import datetime
from actions.actionServices.httpApi import http_post


from actions.config import config


class resetAgencyBusinessForm(Action):
    def name(self):
        return "action_reset_agency_business_slot"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("agentId", None), SlotSet("form_asked_counter", None), SlotSet("from_date", None), SlotSet("to_date", None)]


class ValidateAgencyBusinessForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_agency_business_form"

    def validate_agentId(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:
        agentId = tracker.get_slot("agentId")
        return {"agentId": agentId}

    def validate_from_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:

        from_date = tracker.get_slot("from_date")
        try:
            valid_from_date = datetime.strptime(from_date, "%Y-%m-%d")
        except ValueError:
            dispatcher.utter_message(
                text="Please provide a valid date of format: YYYY-MM-DD")
            return {"from_date": None}
        return {"from_date": from_date}

    def validate_to_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict
    ) -> Dict[Text, Any]:

        to_date = tracker.get_slot("to_date")
        try:
            valid_to_date = datetime.strptime(to_date, "%Y-%m-%d")
        except ValueError:
            dispatcher.utter_message(
                text="Please provide a valid date of format: YYYY-MM-DD")
            return {"to_date": None}
        return {"to_date": to_date}

# commenting now, will uncomment later if needed
    # def validate_business_type(
    #     self,
    #     slot_value: Any,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: DomainDict
    # ) -> Dict[Text, Any]:

    #     business_type = tracker.get_slot("business_type")
    #     return {"business_type": business_type}


class ActionAgencyBusinessFormSubmit(Action):
    def name(self) -> Text:
        return "action_agency_business_form_submit"

    def businessResponse(self, response):
        botResponse = {
            "type": "detailpolicy",
            "tableData": []
        }
        tableDataPaid = {
            "subtitle": "Agency Business",
            "for": "bank detil",
            "data": []
        }

        for item in (response.get('agentBusinessProperties')):

            tableDataPaid['data'].append({
                "Policy No": item.get('policyNo'),
                "Assured": item.get("assured"),
                "Contact No": item.get("contactNo"),
                "Product": item.get("product"),
                "Sum Assured": item.get("sumAssured"),
                "Policy Term": item.get("policyTerm"),
                "Paying Term": item.get("payingTerm"),
                "Payment Frequency": item.get("paymentFrequency"),
                "Premium": item.get("premium"),
                "Next Due Date": item.get("nextDueDate")
            })
        botResponse['tableData'].append(tableDataPaid)
        print(str(botResponse))
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

            agent_details = {
                "agentId": tracker.get_slot("agentId"),
                "fromDate": tracker.get_slot("from_date"),
                "toDate": tracker.get_slot("to_date"),
                "businessType": "F"
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

            url = API_BASE_URL + "/agencyBusiness"
            response = http_post(url, headers, agent_details)
            if response.get("agentBusinessProperties"):
                data = self.businessResponse(response)
                data['is_form']=True
                ans = data.get("tableData")
                if ans:
                    dispatcher.utter_message(json_message=data)
                else:
                    dispatcher.utter_message(
                        text=f"There is no any business in the given date range."
                    )
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
