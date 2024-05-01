
from actions.actionServices.httpApi import http_post, http_get
from actions.emailService import sendCustomEmail
from actions.config import config
from rasa_sdk.events import SlotSet,FollowupAction
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class DashboardPost:
  def __init__(self, type_org):
     type_org=type_org if type_org else 'general';
     self.admin_token=config.get(type_org).get('admin_token')
     self.bot_token=config.get(type_org).get('bot_token')
     self.organization_id=config.get(type_org).get('organization_id')
     self.dashboard_host=config.get(type_org).get('dashboard_host')
     self.protocal=config.get(type_org).get('protocal')

  def DASHBOARD_POST_LEAD(self,data):
        print("DASHBOARDDD",data, self.dashboard_host,self.bot_token)
        url = f"{self.protocal}{self.dashboard_host}/rest/v1/Organizations/{self.organization_id}/leads";
        headers = {'content-type': 'application/json', 'Authorization': self.bot_token };
        http_post(url,headers,data);
        
        
  def SENDEMAIL(self,data):
          subject="Customer with following details wants to interact with you:"
          html=f"<div><ul style='list-style:none'></li><li>Customer/User:</b> {data.get('fullname')}</li><li>Phone No/Email:</b> {data.get('mobile_email')}</li></ul> </div>"  
          sendCustomEmail(html,subject)


class SetDashboardData(Action):
    def name(self):
        return "action_set_dashboard_data"

    def run(self, dispatcher, tracker, domain):
        full_name= tracker.get_slot("feedback_complaints_full_name") or tracker.latest_message["metadata"].get("name")
        phone_number= tracker.get_slot("feedback_complaints_phone_number") or tracker.latest_message["metadata"].get("phoneNumber");
        org_type = tracker.latest_message["metadata"].get("type");
        protocal = config.get(org_type).get('protocal')
        organization_id=config.get(org_type).get('organization_id')
        dashboard_host=config.get(org_type).get('dashboard_host')
        admin_token=config.get(org_type).get('admin_token')
        bot_token=config.get(org_type).get('bot_token')
        userdetails = None
        print("full name1=====================", full_name, "phone number=====================", phone_number)

        if full_name:
                if phone_number:
                        print("full name=====================", full_name, "phone number=====================", phone_number)
                        return [SlotSet("feedback_complaints_full_name", full_name), SlotSet("feedback_complaints_phone_number", phone_number)]
                else:
                       return [SlotSet("feedback_complaints_full_name", full_name)]           
        else:
                headers = {'content-type': 'application/json', 'Authorization': bot_token };
                user_id = tracker.sender_id
                url = f'{protocal}{dashboard_host}/rest/v1/visitors/userId?organizationId={organization_id}&userId={user_id}&access_token={admin_token}'
                response = http_get(url, headers)
                print(response,"response from dashboard")

                try:
                        if response and response.get("data"):
                                userdetails = response.get("data").get("clientDetails")
                                full_name = userdetails.get('name', None)
                                phone_number = userdetails.get('mobile', None)
                                print("mobile  number=====================", phone_number, "full name=====================", full_name)
                                print(userdetails, "userdetails")

                        if userdetails:
                                return [SlotSet("feedback_complaints_full_name", full_name), SlotSet("feedback_complaints_phone_number", phone_number)]
                        else:
                                intent=tracker.latest_message["intent"].get("name")
                                print(intent, "intent")
                                if intent=="menu":
                                        return[SlotSet("dynamic_slot", "menu"),FollowupAction("user_details_form")]
                                else:
                                      return[FollowupAction("user_details_form")] 
                except Exception as e:
                        print('exception', e)