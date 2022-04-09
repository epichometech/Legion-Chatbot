import json, sys, time, signal
from json.decoder import JSONDecodeError
from kafka import KafkaConsumer

class KafkaPush2Rasa:
  def __init__(self, conf=None):
    self.consumer = KafkaConsumer(
      'discordMessagesIncoming',
      bootstrap_servers = ["redpanda-1:9092"],
      group_id = "rasa",
      value_deserializer=lambda m: json.loads(m.decode('ascii'))
    )
  
  def graceful_exit(self, *args, **kwargs):
    raise SystemExit

  def run(self):
    for msg in self.consumer:
      try:
        print(msg.value['content'])
      except SystemExit:
        break

def shutdown(*args, **kwargs):
  pusher.graceful_exit()

if __name__ == "__main__":
  pusher = KafkaPush2Rasa()
  signal.signal(signal.SIGINT, shutdown)
  signal.signal(signal.SIGTERM, shutdown)
  pusher.run()