from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, FollowupAction
from rasa_sdk.executor import CollectingDispatcher
import json
from actions.facebook_response import convert_to_channel_response


class ActionPurchase(Action):

    def name(self) -> Text:
        return "action_purchase"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        insurance_info = tracker.get_slot("insurance_info")
        product_type = tracker.get_slot("product_type")
        document = tracker.get_slot("document")

        org_type = tracker.latest_message["metadata"].get("type")
        file_path = f'actions/responses/{org_type}/purchase.json'
        channel = tracker.get_latest_input_channel()

        if insurance_info:
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get(insurance_info)
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)


        if org_type == "himalayan":
            if document == "form":
                return [SlotSet("feedback_type", 'buy_policy'), FollowupAction("feedback_complaints_form")]
            
            if product_type:
                dispatcher.utter_message(text= f"Thank you for your interest in our products. Please provide your details below, and we will get back to you shortly.")
                return [SlotSet("product_type", product_type), SlotSet("feedback_type", "buy_policy"), FollowupAction("feedback_complaints_form")]
            
            else:
                dispatcher.utter_message(text= f"Thank you for your interest in our products. Please provide your details below, and we will get back to you shortly.")
                return [SlotSet("feedback_type", 'buy_policy'), FollowupAction("feedback_complaints_form")]
            


        elif org_type == "reliable":
            if channel == "rest":
                if document == "form":
                    try:
                        with open(file_path, 'r') as f:
                            data = json.load(f)
                            response = data.get('insurance_purchase')
                            dispatcher.utter_message(
                                json_message=response)
                    except Exception as error:
                        print(error)
                    return[]  

                else:
                    dispatcher.utter_message(text= f"Thank you for your interest in our products. In order to purchase insurance plan, please fill up the given form.",
                                            buttons = [
                                                {
                                                    "title": "Insurance Purchase Form",
                                                    "payload": f"/purchase{{\"document\":\"form\"}}"
                                                }
                                            ])      

            else:
                dispatcher.utter_message(text=f"Thank you for your interest in our products. In order to purchase insurance plan, please contact to our nearest branch.",
                                         buttons = [
                                             {
                                                 "title": "Branch",
                                                 "type": "web_url",
                                                 "url": "https://reliablelife.com.np/network-branch-sub-branch-upcoming/"
                                             }
                                         ])    



        elif org_type == "ime":
            if document == "form":
                try:
                    with open(file_path, 'r') as f:
                        data = json.load(f)
                        response = data.get('insurance_purchase')
                        dispatcher.utter_message(
                            json_message=response)
                except Exception as error:
                    print(error)
                return[]  
            
            else:
                dispatcher.utter_message(text= f"Thank you for your interest in our products. In order to purchase insurance plan, please fill up the given form.",
                                        buttons = [
                                            {
                                                "title": "Insurance Purchase Form",
                                                "payload": f"/purchase{{\"document\":\"form\"}}"
                                            }
                                        ]) 

class ResetPurchase(Action):
    def name(self):
        return "action_reset_purchase"

    def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("insurance_info", None),
            SlotSet("product_type", None),
            SlotSet("document", None),
            SlotSet("user_type", None)
        ]
