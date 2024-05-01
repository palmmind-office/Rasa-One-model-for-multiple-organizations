from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json
from actions.facebook_response import convert_to_channel_response


class ActionContact(Action):

    def name(self) -> Text:
        return "action_contact"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        office_type = tracker.get_slot("office_type")
        social_media = tracker.get_slot("social_media")
        user_type = tracker.get_slot("user_type")
        branch_type = tracker.get_slot("branch_type")
        channel = tracker.get_latest_input_channel()

        org_type = tracker.latest_message["metadata"].get("type")
        file_path = f'actions/responses/{org_type}/contact.json'

        except_web = ["viber", "facebook", "instagram", "whatsapp"]

        if org_type:
            if org_type == 'ime' or org_type == "himalayan":
                branch_type = None

            if org_type == "himalayan":
                if social_media == "instagram":
                    social_media = 'social media'

            if org_type == "reliable":
                if social_media == "twitter" or social_media == "linkedin":
                    social_media = 'social media'

            if org_type == "himalayan" or org_type == "ime":
                if social_media == "viber":
                    social_media = 'social media'

            if org_type == "reliable":
                if user_type == 'agent':
                    user_type = None

        if office_type == "main office" or office_type == "customer support":
            if channel == "rest":
                try:
                    with open(file_path, 'r', encoding='utf8') as f:
                        data = json.load(f)
                        response = data.get('main_office')
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
                        response = data.get('main_office_fb')
                        dispatcher.utter_message(text=f"Dear customer,following is the contact details for our head office.")
                        convert_to_channel_response(
                            dispatcher, rasa_response=response, channel=channel)
                        return []
                except Exception as error:
                    print(error)
                return[]
        
        elif office_type == "branch office":
            
            if channel == "rest":
                if branch_type:
                    try:
                        with open(file_path, 'r', encoding='utf8') as f:
                            data = json.load(f)
                            response = data.get(f'branch_{branch_type}')
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
                            response = data.get('branch_office')
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
                        response = data.get('branch_office_fb')
                        convert_to_channel_response(
                            dispatcher, rasa_response=response, channel=channel)
                        return []
                except Exception as error:
                    print(error)
                return[]

               

        if social_media:
            try:
                print("inside 1")
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get(social_media)
                    print("inside res:", response)
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
                    response = data.get('agent_contact')
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
                    response = data.get('else_part_contact')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[] 


class ResetContact(Action):
    def name(self):
        return "action_reset_contact"

    def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("office_type", None),
            SlotSet("social_media", None),
            SlotSet("user_type", None),
            SlotSet("branch_type", None)
        ]
