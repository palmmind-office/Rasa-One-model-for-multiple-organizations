import inspect
from sanic import Sanic, Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse
from typing import Text, Dict, Any, Optional, Callable, Awaitable, NoReturn
from services.textConverter import http_translator_api

# services
# from services.spacyNlpClassifier import SpacyNlpClassifier

import rasa.utils.endpoints
from rasa.core.channels.channel import (
    InputChannel,
    CollectingOutputChannel,
    UserMessage,
)


class Restfacebook(InputChannel):
    def name(name) -> Text:
        return "facebook"

    def blueprint(
        self, on_new_message: Callable[[UserMessage], Awaitable[None]]
    ) -> Blueprint:

        custom_webhook = Blueprint(
            "custom_webhook_{}".format(type(self).__name__),
            inspect.getmodule(self).__name__,
        )

        @custom_webhook.route("/", methods=["GET"])
        async def health(request: Request) -> HTTPResponse:
            return response.json({"status": "facebookchannel working fine"})

        @custom_webhook.route("/webhook", methods=["POST"])
        async def receive(request: Request) -> HTTPResponse:
            sender_id = request.json.get("sender")
            usermessage = request.json.get("message")
            text = usermessage.lower().strip()
            input_channel = self.name()
            metadata = self.get_metadata(request)
            userdata = request.json.get("metadata")
            isFormActivated=userdata.get('isFormActivated')
            print("IS FORM ACTIVATEDDDDDD", isFormActivated)
            text = text if isFormActivated else http_translator_api(text)
            print("text===", text)
            collector = MyioOutput()
            await on_new_message(
                UserMessage(
                    text,
                    collector,
                    sender_id,
                    input_channel=input_channel,
                    metadata=userdata
                )
            )
            return response.json(collector.messages)

        return custom_webhook


class MyioOutput(CollectingOutputChannel):
    @classmethod
    def name(cls) -> Text:
        return "facebook"
