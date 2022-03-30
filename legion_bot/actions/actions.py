# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import urllib.request, json

class ActionDadJoke(Action):
  def name(self) -> Text:
    return "action_dad_joke"

  def run(self,
          dispatcher: CollectingDispatcher,
          tracker: Tracker,
          domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

    req = urllib.request.Request(
      url = 'https://icanhazdadjoke.com/',
      headers = {
        'Accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:77.0) Gecko/20100101 Firefox/77.0'
        },
      method='GET')

    with urllib.request.urlopen(req) as response:
      html = json.loads(response.read())
    dispatcher.utter_message(text=f'{html["joke"]}')
    return []