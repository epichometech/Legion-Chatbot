import json
from json.decoder import JSONDecodeError
from http import HTTPStatus
from typing import Any, Awaitable, Callable, Dict, List, Optional, Text

from rasa.core.channels import InputChannel, OutputChannel, UserMessage
from rasa.core.channels.channel import UserMessage

from sanic import Blueprint, response
from sanic.request import Request
from sanic.response import HTTPResponse

class DiscordOutput(OutputChannel):
  @classmethod
  def name() -> Text:
    return "DiscordOutput"

  def __init__(
    self,
    textchannel: Text
  ) -> None:
    self.textchannel = textchannel
    super().__init__()

  async def post_message(self,message):
    """Post the message to the self.textchannel"""
    pass

class DiscordInput(InputChannel):
  @classmethod
  def name() -> Text:
    """Discord Connector"""
    return "DiscordInput"

  def __init__(
    self,
    ) -> None:
    """The only required value to get messages back is channel_id"""
    self.

  def blueprint(
    self, on_new_message: Callable[[UserMessage], Awaitable[Any]]
  ) -> Blueprint:
    discord_webhook = Blueprint('discord_webhook', __name__)

    @discord_webhook.route("/", methods=["GET"])
    async def health(_: Request) -> HTTPResponse:
      return response.json({"status": "ok"})

    @discord_webhook.route("/webhook", methods=["GET","POST"])
    async def webhook(request: Request) -> HTTPResponse:
      content_type = request.headers.get("content-type")

      return await self.process_message(
        self,
        on_new_message,
        json.loads(request.json)
      )
    
    return discord_webhook
  
  async def process_message(
    self,
    on_new_message: Callable[[UserMessage], Awaitable[Any]],
    message: Dict
  ) -> Any:
    pass

  def get_output_channel() -> OutputChannel:
    pass