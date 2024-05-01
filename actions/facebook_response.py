import os
import json
import html2text


def convert_to_channel_response(dispatcher, rasa_response, channel):
    if channel == "instagram":
        print("last part of convert_to_channel_response jsdaskhdgfahsdgf")
        if rasa_response:
            if rasa_response["type"] == 'quick_reply':
                text = rasa_response.get("title").replace("<br>", "\n")
                buttons = rasa_response.get("data")
                if buttons:
                    if len(buttons) <= 10:
                        elements = []
                        button_list = []

                        for item in buttons:
                            if "link" in item:
                                button_list.append({
                                    "type": "web_url",
                                    "title": item["title"],
                                    "url": item["link"]
                                })
                            else:
                                button_list.append({
                                    "title": item["title"],
                                    "payload": item["payload"]
                                })

                        if button_list:
                            elements.append({
                                "title": "Please click the button:",
                                "buttons": button_list
                            })

                            message = {
                                "text": text,
                                "elements": elements
                            }

                            dispatcher.utter_message(json_message=message)

                    else:
                        elements = []
                        while len(buttons) > 0:
                            current_buttons = buttons[:3]
                            buttons = buttons[3:]

                            element_buttons = []
                            for button in current_buttons:
                                if "payload" in button:
                                    element_buttons.append({
                                        "type": "postback",
                                        "title": button["title"],
                                        "payload": button["payload"]
                                    })
                                elif "link" in button:
                                    element_buttons.append({
                                        "type": "web_url",
                                        "title": button["title"],
                                        "url": button["link"]
                                    })
                            element = {
                                "title": "Please select an option",
                                "buttons": element_buttons
                            }
                            elements.append(element)
                        message = {
                            "text": text,
                            "elements": elements
                        }
                        dispatcher.utter_message(json_message=message)

                else:
                    dispatcher.utter_message(text=text)

                print("i need something to go to the nlu fallback")

            elif rasa_response["type"] == "multiple-title":
                print("facebook response for menu")
                text = rasa_response["title"][0]
                quick_replies = []
                for item in rasa_response["submenu"]["contents"]:
                    quick_replies.append({
                        "content_type": "text",
                        "title": item["title"],
                        "payload": item["payload"],
                        "image_url": item["icon"]
                    })
                    print("facebook response for menu1")
                dispatcher.utter_message(
                    text=text, quick_replies=quick_replies)

            elif rasa_response["type"] == 'ListItem':
                text = rasa_response.get("title").replace("<br>", "\n")
                text += "\n"
                elements = []
                string = ""

                print("THIS IS RASA RESPONSE", rasa_response)
                for item in rasa_response["data"]:
                    string += "\n"
                    string += (item["subtitle"]).replace("●", "●")

                message = text + string
                dispatcher.utter_message(json_message=message)

            elif rasa_response["type"] == 'contact':
                text = rasa_response.get("title")
                dct = "\n\n"
                dct += rasa_response["data"]["Name"]
                dct += "\n"
                dct += rasa_response["data"]["subtitle"]
                for item in rasa_response["data"]['info']:
                    dct += ("\n")
                    dct += (item['key'] + " : " + item['value'])
                  

                message = text+dct
                dispatcher.utter_message(json_message=message)

            elif rasa_response["type"] == 'detailDrawer':
                elements = rasa_response.get("data")
                text = rasa_response.get("title")
                for element in elements:
                    element['title'] = element.get('title')
                    element["image_url"] = element.get('img')

                message = {
                    "text": text,
                    "elements": elements
                }
                dispatcher.utter_message(json_message=message)

    if channel == "facebook" or channel == "fb":
        if rasa_response:
            if rasa_response["type"] == 'quick_reply':
                text = rasa_response.get("title").replace("<br>", "\n")
                buttons = rasa_response.get("data")
                if buttons:
                    if len(buttons) <= 10:
                        response_buttons = []
                        for item in buttons:
                            if "link" in item:
                                response_buttons.append({
                                    "type": "web_url",
                                    "title": item["title"],
                                    "url": item["link"]
                                })
                            else:
                                response_buttons.append({
                                    "title": item["title"],
                                    "payload": item["payload"]
                                })
                        print("quick reply with buttons")
                        dispatcher.utter_message(
                            text=text, buttons=response_buttons)
                    else:
                        elements = []
                        while len(buttons) > 0:
                            current_buttons = buttons[:3]
                            buttons = buttons[3:]

                            element_buttons = []
                            for button in current_buttons:
                                if "payload" in button:
                                    element_buttons.append({
                                        "type": "postback",
                                        "title": button["title"],
                                        "payload": button["payload"]
                                    })
                                elif "link" in button:
                                    element_buttons.append({
                                        "type": "web_url",
                                        "title": button["title"],
                                        "url": button["link"]
                                    })
                            element = {
                                "title": "Please select an option",
                                "buttons": element_buttons
                            }
                            elements.append(element)
                        message = {
                            "text": text,
                            "elements": elements
                        }
                        dispatcher.utter_message(json_message=message)

                else:
                    dispatcher.utter_message(text=text)

                print("i need something to go to the nlu fallback")

            elif rasa_response["type"] == "multiple-title":
                print("facebook response for menu")
                text = rasa_response["title"][0]
                quick_replies = []
                for item in rasa_response["submenu"]["contents"]:
                    quick_replies.append({
                        "content_type": "text",
                        "title": item["title"],
                        "payload": item["payload"],
                        "image_url": item["icon"]
                    })
                    print("facebook response for menu1")
                dispatcher.utter_message(
                    text=text, quick_replies=quick_replies)

            elif rasa_response["type"] == 'ListItem':
                text = rasa_response.get("title").replace("<br>", "\n")
                text += "\n"
                elements = []
                string = ""

                print("THIS IS RASA RESPONSE", rasa_response)
                for item in rasa_response["data"]:
                    string += "\n"
                    string += (item["subtitle"]).replace("●", "●")

                message = text + string
                dispatcher.utter_message(json_message=message)

            elif rasa_response["type"] == 'contact':
                text = rasa_response.get("title")
                dct = "\n\n"
                dct += rasa_response["data"]["Name"]
                dct += "\n"
                dct += rasa_response["data"]["subtitle"]
                for item in rasa_response["data"]['info']:
                    dct += ("\n")
                    dct += (item['key'] + " : " + item['value'])

                message = text+dct
                dispatcher.utter_message(json_message=message)

            elif rasa_response["type"] == 'detailDrawer':
                elements = rasa_response.get("data")
                text = rasa_response.get("title")
                for element in elements:
                    element['title'] = element.get('title')
                    element["image_url"] = element.get('img')

                message = {
                    "text": text,
                    "elements": elements
                }
                dispatcher.utter_message(json_message=message)

    if channel == "whatsapp":
        print("I am in the WhatsApp channel")

        if rasa_response["type"] == 'quick_reply':
            text = rasa_response.get("title")


            h = html2text.HTML2Text()
            h.ignore_links = False  # Ignore links during conversion

            plain_text_response = h.handle(text)
            text = plain_text_response

            buttons = rasa_response.get("data")

            link_buttons = []  # Store buttons with links
            payload_buttons = []  # Store buttons with payloads

            if buttons:
                for item in buttons:
                    if "link" in item and "title" in item:
                        link_buttons.append(item)  # Add buttons with links
                    elif "payload" in item and "title" in item:
                        # Add buttons with payloads
                        payload_buttons.append(item)

                if link_buttons and not payload_buttons:
                    # Display the original text message from rasa_response
                    dispatcher.utter_message(text=text)

                    # Iterate through all buttons with links
                    for link_button in link_buttons:
                        # Add the message with the link (no need to display title)
                        link_message = f"For *{link_button['title']}*, please click the given link: {link_button['link']}"
                        dispatcher.utter_message(text=link_message)

                if payload_buttons and not link_buttons:
                    # Check if there are 3 or fewer payload buttons
                    if len(payload_buttons) <= 3:
                        response_buttons = []

                        for item in payload_buttons:
                            response_buttons.append({
                                "title": item["title"],
                                "payload": item["payload"]
                            })

                        # Display buttons directly
                        dispatcher.utter_message(
                            text=text, buttons=response_buttons)
                    elif len(payload_buttons) > 3 and len(payload_buttons) <= 10:
                        response_buttons = []

                        for item in payload_buttons:
                            response_buttons.append({
                                "id": item["payload"],
                                "title": item["title"],
                            })

                        message = {"type": "list", "buttonName": "Options", "bodyText": f"{text} \n ", "sections": {
                            "": response_buttons}, "options": {"footerText": f""}}
                        dispatcher.utter_message(json_message=message)

                if link_buttons and payload_buttons:
                    if len(payload_buttons) <= 3:
                        response_buttons = []

                        for item in payload_buttons:
                            response_buttons.append({
                                "title": item["title"],
                                "payload": item["payload"]
                            })

                        # Display buttons directly
                        dispatcher.utter_message(
                            text=text, buttons=response_buttons)
                    elif len(payload_buttons) > 3 and len(payload_buttons) <= 10:
                        response_buttons = []

                        for item in payload_buttons:
                            response_buttons.append({
                                "id": item["payload"],
                                "title": item["title"],
                            })

                        message = {"type": "list", "buttonName": "Options", "bodyText": f"{text} \n ", "sections": {
                            "": response_buttons}, "options": {"footerText": f""}}
                        dispatcher.utter_message(json_message=message)

                    for link_button in link_buttons:
                        link_message = f"For *{link_button['title']}*, please click the given link: {link_button['link']}"
                        dispatcher.utter_message(text=link_message)

            else:
                dispatcher.utter_message(text=text)

        elif rasa_response["type"] == 'ListItem':
            print("checking whatsapp listitem")

            response = rasa_response["data"]
            response_text = '\n'.join(item["subtitle"] for item in response)
            dispatcher.utter_message(text=rasa_response["title"])
            dispatcher.utter_message(
                text=f"{response_text}")

        else:
            dispatcher.utter_message(json_message=rasa_response)
        return[]

    if channel == "viber":
        print("channels:", channel)
        if rasa_response["type"] == 'quick_reply':
          
            text = rasa_response.get("title")
           # To remove the HTML Tags used in the text
            h = html2text.HTML2Text()
            h.ignore_links = False  # Ignore links during conversion

            plain_text_response = h.handle(text)

            text = plain_text_response

            buttons = rasa_response.get("data")
            print("last part of convert_to_channel_response quick reply", buttons)
            # Create the response message with both text and buttons

            if buttons:

                Buttons = []
                for item in buttons:
                    if "link" in item:                     
                        link = item.get("link")                      
                        button = {
                            "Columns": 3,
                            "Rows": 1,
                            "Text": "<br><font color=\"#ffffff\"><b>{}</b></font>".format(item["title"]),
                            "TextSize": "large",
                            "TextHAlign": "center",
                            "TextVAlign": "middle",
                            "ActionType": "open-url",
                            "ActionBody": f"{link}",
                            "BgColor": "#296E90",
                            "Image": "https://s18.postimg.org/9tncn0r85/sushi.png",
                            "Frame": {
                                "Frame.BorderWidth": 3,
                                "Frame.BorderColor": "#FF0000",
                                "Frame.CornerRadius": 8
                            }
                        }

                    else:
                        payload = item.get("payload")
                        button = {
                            "Columns": 3,
                            "Rows": 1,

                            "Text": "<br><font color=\"#ffffff\"><b>{}</b></font>".format(item["title"]),
                            "TextSize": "large",
                            "TextHAlign": "center",
                            "TextVAlign": "middle",
                            "ActionType": "reply",
                            "ActionBody": f"{payload}",
                            "BgColor": "#296E90",
                            "Image": "https://s18.postimg.org/9tncn0r85/sushi.png",
                            "Frame": {
                                "Frame.BorderWidth": 3,
                                "Frame.BorderColor": "#FF0000",
                                "Frame.CornerRadius": 8
                            }
                        }

                    Buttons.append(button)
                message = {
                    "Type": "keyboard",
                    "Buttons": Buttons
                }

                dispatcher.utter_message(text=text)
                dispatcher.utter_message(json_message=message)

            else:
                dispatcher.utter_message(text=text)
                return[]
        elif rasa_response["type"] == 'detailDrawer':
            text = "Please find the details below."
            items = rasa_response["data"]

            buttons = []

            for index, item in enumerate(items):
                print("inside the for loop", len(items))
                image = item.get("image_url")

                url_button = {
                    "Columns": 6,
                    "Rows": 2,
                    "Text": item.get("title"),
                    "ActionType": "reply",
                    "ActionBody": "https://www.google.com",
                    "TextSize": "medium",
                    "TextVAlign": "middle",
                    "TextHAlign": "left"
                }

                details_button = {
                    "Columns": 6,
                    "Rows": 1,
                    "ActionType": "open-url",
                    "ActionBody": item["buttons"][0]["url"],
                    "Text": f"<font color=\"#ffffff\"><b>More Details</b></font>",
                    "TextSize": "large",
                    "TextVAlign": "middle",
                    "TextHAlign": "middle",
                    "BgColor": "#0171b6",
                    "Image": "https://s14.postimg.org/4mmt4rw1t/Button.png"
                }

                premium_calculator = {
                    "Columns": 6,
                    "Rows": 1,
                    "ActionType": "open-url",
                    "ActionBody": "https://himalayanlife.com.np/Premium-Calculator.aspx",
                    "Text": "<font color=#8367db>PREMIUM CALCULATOR</font>",
                    "TextSize": "small",
                    "TextVAlign": "middle",
                    "TextHAlign": "middle"
                }

                images = {
                    "Columns": 6,
                    "Rows": 3,
                    "ActionType": "reply",
                    "ActionBody": "https://www.google.com",
                    "Image": image
                }

                buttons.extend(
                    [images, url_button, details_button, premium_calculator])

            message = {
                "Type": "rich_media",
                "ButtonsGroupColumns": 6,
                "ButtonsGroupRows": 7,
                "BgColor": "#FFFFFF",
                "Buttons": buttons,
            }
            print("This is messsage", message)
            dispatcher.utter_message(json_message=message)

            return[]

        elif rasa_response["type"] == 'ListItem':
            print("inside listitem viber")
            text = rasa_response["title"].replace("<br>", "\n")
            print("the text is==", text)
            text += "\n"
            elements = []
            string = ""
            msg = str(rasa_response["data"])

            print("THIS IS RASA RESPONSE", rasa_response)
            for item in rasa_response["data"]:
                string += "\n"
                string += item.get("subtitle")

            message = str(text) + string
            dispatcher.utter_message(text=message)

            return[]

        else:
            dispatcher.utter_message(json_message=rasa_response)

    else:
        dispatcher.utter_message(json_message=rasa_response)
        return None
