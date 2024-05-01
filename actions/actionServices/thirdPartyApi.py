import os
from actions.actionServices.httpApi import http_get
from actions.config import config

import requests

# Api credetials
headers = {"content-type": "application/json"}




def GetOffer(channel="rest", org_type = None):
    print("Ths is org type:", org_type)
    # environmental varialbles
    admin_token = config.get(org_type).get("admin_token")
    bot_token = config.get(org_type).get("bot_token")
    organization_id = config.get(org_type).get("organization_id")
    base_url = config.get(org_type).get("base_url")
    protocal = config.get(org_type).get("protocal")
    dashboard_host = config.get(org_type).get("dashboard_host") or "localhost"
    org_url=config.get(org_type).get('org_url')



    headers = {"content-type": "application/json", "Authorization": admin_token}
    url = f"{protocal}{dashboard_host}/rest/v1/Offers/bot?filter[organizationId]={organization_id}"
    responseData = http_get(url, headers)
    print(responseData, url)
    if responseData and "offer" in responseData:
        if len(responseData["offer"])>0:
            if channel == "facebook":
                response = {
                        "type": "template",
                        "elements": [],
                    
                }
                for offer in responseData["offer"]:
                    buttonType = {}
                    if "http" in offer.get("link", ''):
                        buttonType["type"] = "web_url"
                        buttonType["url"] = offer["link"]
                        buttonType["title"] = "Visit website"
                    else:
                        buttonType["type"] = "web_url"
                        buttonType["title"] = "View more"
                        buttonType["url"] = org_url

                    imageurl = offer["image"].replace(" ", "%20")
                    baseimage = f"{protocal}{dashboard_host}/{imageurl}"
                    print("IMAGE", baseimage)
                    # if len(buttonType) > 0:
                    response["elements"].append(
                        {
                            "title": offer["title"],
                            "image_url": baseimage,
                            "subtitle": offer.get("subTitle") or offer.get("title"),
                            "buttons": [buttonType],
                        }
                    )
                    # else:
                    #     response["elements"].append(
                    #         {
                    #             "title": offer["title"],
                    #             "image_url": baseimage,
                    #             "subtitle": offer.get("subTitle") or offer.get("title"),
                    #             "buttons": org_url
                    #         }
                    #     )
                return response
            elif channel == "rest":
                offerModule = {
                    "type": "detailDrawer",
                    "title": "We have the following offers available at our insurance at the moment.",
                    "data": [],
                }
                response = responseData["offer"]
                for offer in response:
                    imageurl = offer["image"].replace(" ", "%20")
                    baseimage = f"{protocal}{dashboard_host}/{imageurl}"
                    offerModule["data"].append(
                        {
                            "img": baseimage,
                            "title": offer.get("title"),
                            # 'OfferTitile':offer['description'],
                            # 'descriptions':offer['description'],
                            "subtitle": offer.get("subTitle"),
                            "button": {
                                "contents": [
                                    {
                                        "title": "View Details",
                                        "id": "btn1",
                                        "Details": {
                                            # "interest": "IME Annual Cash Back Plan(5%)",
                                            "title": offer.get("title"),
                                            "subtitle": offer.get("subTitle"),
                                            "img": [{"img": baseimage}],
                                            "paragraph": offer.get("description"),
                                            "button": {
                                                "contents": [
                                                    {
                                                        "title": "Click Here",
                                                        "link": offer.get("link"),
                                                    }
                                                ]
                                            },
                                        },
                                    }
                                ]
                            },
                            # 'btnDesc': 'Do it now',
                            # 'btnLink':offer['link']
                        }
                    )
                return offerModule

    else:
        print("insude else")
        # return {
        #     "text": "There are no offers available at the moment. For more information please contact our head office.",
        # }
        response = {
            "title": "There are no offers available at the moment. For more information please contact our head office.",
            "type": "quick_reply",
            "data": [
                {
                    "title":"Head Office",
                    "payload": "/contact{\"office_type\":\"main office\"}"
                }
            ]
        }
        return response



# GetOffer("rest")get