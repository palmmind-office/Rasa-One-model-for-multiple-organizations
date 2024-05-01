from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
from actions.config import config


class ActionFaq(Action):

    def name(self) -> Text:
        return "action_faq"

    def run(self, 
            dispatcher: CollectingDispatcher, 
            tracker: Tracker, 
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            # getting user query
            user_query = tracker.latest_message.get("text")
            org_type = tracker.latest_message["metadata"].get("type")
            org = org_type #take this from .env


            # Calling langchain API, passing user query also
            org_type = tracker.latest_message["metadata"].get("type")
            langchain_base_url = config[org_type]["langchain_base_url"]
            
            print(langchain_base_url)
            print(user_query)
            print(org)
            response = requests.post(langchain_base_url, json={"user_query": user_query,"org": org})
            print("The response is:", response)

            if response.status_code == 200:
                answer = response.json().get("answer")
                dispatcher.utter_message(text=answer)
                print("This is langchain-:", answer)
            else:
                dispatcher.utter_message(text="Sorry, I couldn't find an answer to your question.")

            return[]

        except Exception as e:
            print("exception", e)

             
