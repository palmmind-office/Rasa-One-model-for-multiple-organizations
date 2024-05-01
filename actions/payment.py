from typing import Any, Dict, List, Optional, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
from rasa_sdk.events import SlotSet
from actions.facebook_response import convert_to_channel_response


class Payment(Action):
    def name(self) -> Text:
        return "action_payment"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:

        payment_option = tracker.get_slot("payment_option")
        wallet_name = tracker.get_slot("wallet_name")
        action = tracker.get_slot("action")
        channel = tracker.get_latest_input_channel()

        org_type = tracker.latest_message["metadata"].get("type")
        file_path = f'actions/responses/{org_type}/payment.json'

        if org_type:
            if org_type == 'himalayan':
                if wallet_name == 'imepay':
                    wallet_name = None
        


        if wallet_name:
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get(wallet_name)
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]
        
        if payment_option == "wallet":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('digital_wallets')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]
        
        elif payment_option == "bank":
            if channel == "rest":
                try:
                    with open(file_path, 'r', encoding='utf8') as f:
                        data = json.load(f)
                        response = data.get('banking_partners')
                        convert_to_channel_response(
                            dispatcher, rasa_response=response, channel=channel)
                        return []
                except Exception as error:
                    print(error)
                return[]     

            else:
                try:
                    with open(file_path, 'r', encoding='utf8') as f:
                        data = json.load(f)
                        response = data.get('banking_partners_fb')
                        convert_to_channel_response(
                            dispatcher, rasa_response=response, channel=channel)
                        return []
                except Exception as error:
                    print(error)
                return[]                      
        
        elif payment_option == "office":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('payment_office')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]   


        else:
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('else_part_payment')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]         

class ResetPayment(Action):
    def name(self):
        return "action_reset_payment"

    def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("payment_option", None),
            SlotSet("wallet_name", None),
        ]
