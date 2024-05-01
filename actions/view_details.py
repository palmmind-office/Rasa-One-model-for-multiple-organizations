from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
import json
from rasa_sdk.events import AllSlotsReset, FollowupAction
from actions.facebook_response import convert_to_channel_response


class ActionViewDetails(Action):

    def name(self) -> Text:
        return "action_view_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        category = tracker.get_slot("category")
        user_type = tracker.get_slot("user_type")

        channel = tracker.get_latest_input_channel()

        org_type = tracker.latest_message["metadata"].get("type")
        file_path = f'actions/responses/{org_type}/view_details.json'

        if org_type:
            if org_type == "reliable":
                if category == "revive" or category == "tax certificate":
                    category = None

            # if org_type == "ime":
            #     if category == "policy":
            #         category = None

            if org_type == 'reliable':
                if category == "downline":
                    category == None


        if org_type == "himalayan":
            if channel == "rest":

                if category == "premium due":
                    print("this is category-", category)
                    dispatcher.utter_message(
                        text=f"To view your agency premium due, kindly provide the requested information."
                    )
                    return [SlotSet("category", "premium due"), FollowupAction("agent_login_form")]

                elif category == "business":
                    dispatcher.utter_message(
                        text=f"To view your agency business, kindly provide the requested information."
                    )
                    return [FollowupAction("agency_business_form")]

                elif category == "downline":
                    dispatcher.utter_message(
                        text=f"To view your agency downline, kindly provide the requested information."
                    )
                    return [SlotSet("category", "downline"), FollowupAction("agent_login_form")]

                elif category == "personal":
                    if user_type == "agent":
                        dispatcher.utter_message(
                            text=f"To check your personal details, kindly provide the requested information."
                        )
                        return [SlotSet("category", "personal"), FollowupAction("agent_login_form")] #convert login to personal
                    
                    elif user_type == "policy holder":
                        dispatcher.utter_message(
                            text=f"To view your policy details, kindly provide the requested information."
                        )
                        return [SlotSet("category", "policy"), FollowupAction("policy_form")]            

                elif category == "policy":
                    dispatcher.utter_message(
                        text=f"To view your policy details, kindly provide the requested information."
                    )
                    return [SlotSet("category", "policy"), FollowupAction("policy_form")]

                elif category == "premium":
                    dispatcher.utter_message(
                        text=f"To view your premium details, kindly provide the requested information."
                    )
                    return [SlotSet("category", "premium"), FollowupAction("policy_form")]

                else:  #check if else part needs modification
                    if user_type == "agent":
                        dispatcher.utter_message(
                            text=f"Click the buttons below to view your details.",
                            buttons=[
                                {
                                    "title": "Premium Due",
                                    "payload": f"/view_details{{\"category\":\"premium due\"}}"
                                },
                                {
                                    "title": "Agency Business",
                                    "payload": f"/view_details{{\"category\":\"business\"}}"
                                },
                                {
                                    "title": "Agency Downline",
                                    "payload": f"/view_details{{\"category\":\"downline\"}}"
                                },
                                {
                                    "title": "Personal Details",
                                    "payload": f"/view_details{{\"category\":\"personal\", \"user_type\":\"agent\"}}"
                                }
                            ]
                        )
                        return[]
                    elif user_type == "policy holder":
                        dispatcher.utter_message(
                            text=f"Click the buttons below to view your details.",
                            buttons=[
                                {
                                    "title": "Policy Details",
                                    "payload": f"/view_details{{\"category\":\"policy\"}}"
                                },
                                {
                                    "title": "Premium Details",
                                    "payload": f"/view_details{{\"category\":\"premium\"}}"
                                }
                            ]
                        )
                        return[]
                    else:
                        dispatcher.utter_message(
                            text=f"Are you an agent or a policyholder?",
                            buttons=[
                                {
                                    "title": "Agent",
                                    "payload": f"/view_details{{\"user_type\":\"agent\"}}"
                                },
                                {
                                    "title": "Policy Holder",
                                    "payload": f"/view_details{{\"user_type\":\"policy holder\"}}"
                                }
                            ]
                        )
                        return[]

            else:
                response = {
                     "title" : f"Please click the button below to login and view your details.<br>Note:<br> - For Prime life, use PLI before policy number and agent code.<br> - For Union life, use ULI before policy number and agent code.<br> - For Gurans life, use GLI before policy number and agent code.",
                    "type" : "quick_reply",
                     "data" : [
                        {
                            "title": "View Details",
                            "link": "https://himalayanlife.com.np/Login.aspx"
                        }
                  ]   
                }
                convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)

        
        if org_type == "reliable":
            if channel == "facebook":
                try:
                    with open(file_path, 'r', encoding='utf8') as f:
                        data = json.load(f)
                        response = data.get('view_details_fb')
                        convert_to_channel_response(
                            dispatcher, rasa_response=response, channel=channel)
                        return []
                except Exception as error:
                    print(error)
                return[]

        if org_type == "ime":
            if channel == "facebook":
                return [FollowupAction("feedback_complaints_form")]
        
        if category == "business":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('agency_business')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]
            
        elif category == "downline":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('agency_downline')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]
            
        elif category == "issued policies":
            if user_type == "agent":
                try:
                    with open(file_path, 'r', encoding='utf8') as f:
                        data = json.load(f)
                        response = data.get('agent_issued_policies')
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
                        response = data.get('policyholder_issued_policies')
                        convert_to_channel_response(
                            dispatcher, rasa_response=response, channel=channel)
                        return []
                except Exception as error:
                    print(error)
                return[]
                
            else:
                dispatcher.utter_message(
                    text=f"Are you an agent or a policyholder?",
                    buttons=[
                        {
                            "title": "Agent",
                            "payload": f"/view_details{{\"category\":\"issued policies\",\"user_type\":\"agent\"}}"
                        },
                        {
                            "title": "Policy Holder",
                            "payload": f"/view_details{{\"category\":\"issued policies\", \"user_type\":\"policy holder\"}}"
                        }
                    ]
                )
                return[]
                
        elif category == "policy":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('policy_details')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]
            
        elif category == "transaction history":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('transaction_history')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]
        
        elif category == "tax certificate":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('tax_certificate')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]
        
        elif category == "premium due":
            if user_type == "agent":
                try:
                    with open(file_path, 'r', encoding='utf8') as f:
                        data = json.load(f)
                        response = data.get('agent_premium_due')
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
                        response = data.get('policyholder_premium_due')
                        convert_to_channel_response(
                            dispatcher, rasa_response=response, channel=channel)
                        return []
                except Exception as error:
                    print(error)
                return[]  

            else:
                dispatcher.utter_message(
                    text=f"Are you an agent or a policyholder?",
                    buttons=[
                        {
                            "title": "Agent",
                            "payload": f"/view_details{{\"category\":\"premium due\",\"user_type\":\"agent\"}}"
                        },
                        {
                            "title": "Policy Holder",
                            "payload": f"/view_details{{\"category\":\"premium due\", \"user_type\":\"policy holder\"}}"
                        }
                    ]
                )
                return[]                                     

        elif category == "personal":
            if user_type == "agent":
                try:
                    with open(file_path, 'r', encoding='utf8') as f:
                        data = json.load(f)
                        response = data.get('agent_personal_details')
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
                        response = data.get('policyholder_personal_details')
                        convert_to_channel_response(
                            dispatcher, rasa_response=response, channel=channel)
                        return []
                except Exception as error:
                    print(error)
                return[] 
            
            else:
                dispatcher.utter_message(
                    text=f"Are you an agent or a policyholder?",
                    buttons=[
                        {
                            "title": "Agent",
                            "payload": f"/view_details{{\"category\":\"personal\",\"user_type\":\"agent\"}}"
                        },
                        {
                            "title": "Policy Holder",
                            "payload": f"/view_details{{\"category\":\"personal\", \"user_type\":\"policy holder\"}}"
                        }
                    ]
                )
                return[]                                    

        elif category == "premium":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('premium_details')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]

        elif category == "commission":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('agency_commission')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]   

        elif category == "lapsed policy":
            try:
                with open(file_path, 'r', encoding='utf8') as f:
                    data = json.load(f)
                    response = data.get('lapsed_policy')
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
                    response = data.get('policy_revive')
                    convert_to_channel_response(
                        dispatcher, rasa_response=response, channel=channel)
                    return []
            except Exception as error:
                print(error)
            return[]    

        else:
            #agent or policyholder?
            # separate options so separate jsons for different org
            # call json from here
            if user_type == "agent":
                try:
                    with open(file_path, 'r', encoding='utf8') as f:
                        data = json.load(f)
                        response = data.get('agent_view_details')
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
                        response = data.get('policyholder_view_details')
                        convert_to_channel_response(
                            dispatcher, rasa_response=response, channel=channel)
                        return []
                except Exception as error:
                    print(error)
                return[]  
            
            else:
                dispatcher.utter_message(
                    text=f"Are you an agent or a policyholder?",
                    buttons=[
                        {
                            "title": "Agent",
                            "payload": f"/view_details{{\"user_type\":\"agent\"}}"
                        },
                        {
                            "title": "Policy Holder",
                            "payload": f"/view_details{{\"user_type\":\"policy holder\"}}"
                        }
                    ]
                )
                return[]   


class ResetViewDetails(Action):
    def name(self):
        return "action_reset_view_details"

    def run(self, dispatcher, tracker, domain):
        return [
            SlotSet("user_type", None),
            SlotSet("category", None)
        ]
