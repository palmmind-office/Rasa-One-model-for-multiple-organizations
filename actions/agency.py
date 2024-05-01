from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json
from actions.facebook_response import convert_to_channel_response


class ActionAgency(Action):

    def name(self) -> Text:
        return "action_agency"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        insurance_info = tracker.get_slot("insurance_info")
        channel = tracker.get_latest_input_channel()
        

        org_type = tracker.latest_message["metadata"].get("type")
        file_path = f'actions/responses/{org_type}/agency.json'

        intent = tracker.latest_message.get("intent").get("name")
        try:

            full_intent = (
                tracker.latest_message.get("response_selector")
                .get(intent)
                .get("response")
                .get("intent_response_key")
            )
            print("testing for become agent")
        except:
            full_intent = "agency/general"

        if full_intent == "agency/commission_rate":
            
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('commission_rate')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]

        elif full_intent == "agency/qualification":
            if insurance_info == "training":
                try:
                    with open(file_path, 'r', encoding='utf8') as f:
                        data = json.load(f)
                        response = data.get('agent_training')
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
                        response = data.get('agent_qualifications')
                        convert_to_channel_response(
                            dispatcher, rasa_response=response, channel=channel)
                        return []
                except Exception as error:
                    print(error)
                return[]

        elif full_intent == "agency/general":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('agency_general')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]

class ResetAgency(Action):
    def name(self):
        return "action_reset_agency"

    def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("insurance_info", None),
            SlotSet("user_type", None)
        ]
