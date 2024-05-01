from typing import Any, Dict, List, Optional, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import json
from rasa_sdk.events import SlotSet
from actions.facebook_response import convert_to_channel_response


class FileAClaim(Action):
    def name(self) -> Text:
        return "action_file_a_claim"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        insurance_info = tracker.get_slot("insurance_info")
        channel = tracker.get_latest_input_channel()
        claim_type = tracker.get_slot("claim_type")
        print('claimtpe???????', claim_type)

        org_type = tracker.latest_message["metadata"].get("type")
        file_path = f'actions/responses/{org_type}/file_a_claim.json'

        if org_type == 'ime':
            claim_type = None


        if claim_type == "death":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    print("death claimmmm")
                    response = data.get('death_claim_process')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]

        elif claim_type == "non death":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    print("non death claimmmmmmmmm")
                    response = data.get('non_death_claim_process')
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
                    response = data.get('claim_process')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]            


class AboutClaim(Action):
    def name(self) -> Text:
        return "action_about_claim"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:

        channel = tracker.get_latest_input_channel()

        org_type = tracker.latest_message["metadata"].get("type")
        file_path = f'actions/responses/{org_type}/about_claim.json'
       
        try:
            with open(file_path, 'r', encoding='utf8') as f:
                data = json.load(f)
                response = data.get('about_claim')
                convert_to_channel_response(
                    dispatcher, rasa_response=response, channel=channel)
                return []
        except Exception as error:
            print(error)
        return[]


class ResetFileAClaim(Action):
    def name(self):
        return "action_reset_file_a_claim"

    def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("insurance_info", None),
            SlotSet("user_type", None)
        ]