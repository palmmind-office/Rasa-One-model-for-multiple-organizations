from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json
from actions.facebook_response import convert_to_channel_response
from actions.actionServices.thirdPartyApi import GetOffer 


class ActionOffers(Action):

    def name(self) -> Text:
        return "action_offers"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        org_type = tracker.latest_message["metadata"].get("type")
        channel = tracker.get_latest_input_channel()        
       
        res=GetOffer(channel, org_type=org_type)
        convert_to_channel_response(
                    dispatcher, rasa_response=res, channel=channel)
        return[]
