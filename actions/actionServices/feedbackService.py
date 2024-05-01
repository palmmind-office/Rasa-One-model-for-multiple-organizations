from actions.actionServices.httpApi import http_post
from actions.emailService import sendCustomEmail


import os

from actions.config import config


class FeedbackComplaintPost:
    def __init__(self, type_org):
     type_org=type_org if type_org else 'general';
     self.admin_token=config.get(type_org).get('admin_token')
     self.bot_token=config.get(type_org).get('bot_token')
     self.organization_id=config.get(type_org).get('organization_id')
     self.dashboard_host=config.get(type_org).get('dashboard_host')
     self.protocal=config.get(type_org).get('protocal')


    def DASHBOARD_POST_FEEDBACK(self, data, sender_id):
        url = f"{self.protocal}{self.dashboard_host}/rest/v1/visitors/{sender_id}/feedbacks/create"
        print(url, data, sender_id, "feedback post url")
        headers = {'content-type': 'application/json',
                'Authorization': self.admin_token}
        data = http_post(url, headers, data)
        print(data, "=========response========")


    def DASHBOARD_POST_COMPLAINTS(self,data, sender_id):
        url = f"{self.protocal}{self.dashboard_host}/rest/v1/visitors/{sender_id}/complaints/create"
        headers = {'content-type': 'application/json',
                'Authorization': self.admin_token}
        http_post(url, headers, data)


    def SENDEMAIL_COMPLAINTS(data):
        subject = "Complaints filed by user:"
        html = f"<div><ul style='list-style:none'><b>Customer/User:</b> {data['full_name']}</li><li><b>Phone No:</b> {data['mobile_number']}</li></li><li><b>Email:</b> {data['email_address']}</li><li><b>Problem:</b> {data['problem']}</li><li></ul> </div>"
        sendCustomEmail(html, subject)


    def SENDEMAIL_FEEDBACK(data):
        subject = "Suggestions provided by user:"
        html = f"<div><ul style='list-style:none'><b>Customer/User:</b> {data['full_name']}</li><li><b>Phone No:</b> {data['mobile_number']}</li></li><li><b>Email:</b> {data['email_address']}</li><li><b>Suggestions:</b> {data['suggestion']}</li><li></ul> </div>"
        sendCustomEmail(html, subject)
