from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json
from actions.facebook_response import convert_to_channel_response


class ActionProductInfo(Action):

    def name(self) -> Text:
        return "action_product_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        org_type = tracker.latest_message["metadata"].get("type")
        file_path = f'actions/responses/{org_type}/product_info.json'

        product_type = tracker.get_slot("product_type")
        insurance_info = tracker.get_slot("insurance_info")

        channel = tracker.get_latest_input_channel()

        not_himalayan = ["annual", "single premium", "foreign employment", "health"]
        not_reliable = ["whole life", "annual", "term", "retirement", "woman"]
        not_ime = ["retirement", "term", "woman", "single premium", "foreign employment", "health"]

        print(f"This is {product_type} plan. ooooooooo")
        
        if org_type == "himalayan":      
            if product_type in not_himalayan:
                print("AAA")
                product_type = None
                print(f"This is {product_type} from {org_type}")
               

        elif org_type == "reliable":
            if product_type in not_reliable:
                product_type = None

        elif org_type == "ime":
            if product_type in not_ime:
                product_type = None

        if insurance_info == "bonus":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('bonus_rates')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]

        if product_type:
            if channel == "viber":
                try:
                    with open(file_path, 'r', encoding='utf8') as f:
                        data = json.load(f)
                        print("Inside money back try block")
                        ans = data.get(f'{product_type}_plan_{channel}').get("elements")
                        response = {
                            "title": f"We have different {product_type} plans available. Please find the one that best suits your needs from the given options.",
                            "type": "detailDrawer",
                            "multi": True,
                            "data": ans
                        }
                        convert_to_channel_response(
                            dispatcher, rasa_response=response, channel=channel)
                    
                except Exception as error:
                    print("Excepton",error)

            if channel == "whatsapp":
                try:
                    with open(file_path, 'r', encoding='utf8') as f:
                        data = json.load(f)
                        response = data.get(f'{product_type}_plan_{channel}')
                        dispatcher.utter_message(
                            text=f"We have different {product_type} plans available. Please find the one that best suits your needs from the given options.")
                        for item in response["elements"]:
                            whatsapp_response = {
                                "type": "image",
                                "imageUrl": item.get("image_url"),
                                "caption": item.get("title")
                            }
                            base_url = item["buttons"][0]["url"]
                            whatsapp_response[
                                'caption'] += f"\n*Please click on the link ⬇️ for detailed information* \n\n{base_url}"
                            dispatcher.utter_message(
                                json_message=whatsapp_response)

                except Exception as error:
                    print(error)
                return[]

            else:
                try:
                    with open(file_path, 'r', encoding='utf8') as f: 
                        data = json.load(f)
                        response = data.get(f'{product_type}_plan_{channel}')
                        dispatcher.utter_message(json_message = response)
                        return []
                except Exception as error:
                    print("Excepton",error)
                return[]
        
        else:
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('product_else_part')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]
        
class ResetProductInfo(Action):
    def name(self):
        return "action_reset_product_info"

    def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("product_type", None),
            SlotSet("insurance_info", None)
        ]
