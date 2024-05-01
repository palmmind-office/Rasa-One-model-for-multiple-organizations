from typing import Any, Dict, List, Optional, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
from rasa_sdk.events import SlotSet
from actions.facebook_response import convert_to_channel_response


class ActionUpdateProfile1(Action):
    def name(self) -> Text:
        return "action_update_profile"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        user_type = tracker.get_slot("user_type")
        category = tracker.get_slot("category")
        channel = tracker.get_latest_input_channel()

        org_type = tracker.latest_message["metadata"].get("type")
        file_path = f'actions/responses/{org_type}/update_profile.json'


        if org_type:
            if org_type == "reliable":
                if category == "revive":
                    category = None

            if org_type == "himalayan" or org_type =="ime":
                if category == "address":
                    category = None

        if org_type == "reliable":
            if channel == "facebook":
                try:
                    with open(file_path, 'r', encoding='utf8') as f:
                        data = json.load(f)
                        response = data.get('update_profile_fb')
                        convert_to_channel_response(
                            dispatcher, rasa_response=response, channel=channel)
                        return []
                except Exception as error:
                    print(error)
                return[]

        
        if category == "pan number":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('pan_number')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]
        
        elif category == "account number":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('account_number')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]
        
        elif category == "payment mode":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('payment_mode')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]
        
        elif category == "occupation":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('occupation')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]
        
        elif category == "nominee":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('nominee')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]
        
        elif category == "mobile number":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('mobile_number')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]

        elif category == "address":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('address')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]
        
        elif category == "revive":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('revive_policy')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]

        elif category == "dob" or category == "sum assured" or category == "plan" or category == "term" or category == "proposer details":
            dispatcher.utter_message(text="After policy has been issued,  Date of Birth, Sum Assured, Plan, Term, Proposer Details, and Insurance Name cannot be changed.")
            return[]
      
        
             
        if user_type == "agent":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('update_agent')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]
            
        elif user_type == "policy holder":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('update_policyholder')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]

        else:
            dispatcher.utter_message(
                text= f"Are you an agent or a policyholder?",
                buttons = [
                            {
                                "title": "Agent",
                                "payload": f"/update_profile{{\"user_type\":\"agent\"}}"
                            },
                            {
                                "title": "Policyholder",
                                "payload": f"/update_profile{{\"user_type\":\"policy holder\"}}"
                            }
                        ])
           

class ResetUpdateProfile(Action):
    def name(self):
        return "action_reset_update_profile"

    def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("category", None),
            SlotSet("user_type", None)
        ]
