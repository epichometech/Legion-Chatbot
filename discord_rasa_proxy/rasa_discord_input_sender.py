import json, sys, time, signal
from json.decoder import JSONDecodeError
from kafka import KafkaConsumer

class KafkaPush2Rasa:
  def __init__(self, conf=None):
    self.consumer = KafkaConsumer(
      'discordMessagesIncoming',
      bootstrap_servers = ["kafka:9092"],
      group_id = "rasa"
    )

  def print_assignment(self, consumer, partitions):
    print(f'Assignment: {partitions}')

  def delivery_callback(self, err, msg):
    if err:
      sys.stderr.write('%% Message failed delivery: %s\n' % err)
  
  def graceful_exit(self, *args, **kwargs):
    self.is_shutting_down = True

  def run(self):
    try:
        for msg in self.consumer:
          try:
            message = json.loads(str(msg.value().decode("utf-8")))
            print(f'Message received')
          except JSONDecodeError as e:
            print('Failed to decode json value in kafka message')
            print(e)
            print(str(msg.value().decode("utf-8")))
    except KeyboardInterrupt:
      print('%% Aborted by user\n')
    except Exception as e:
      raise e

def shutdown(*args, **kwargs):
  pusher.graceful_exit()

if __name__ == "__main__":
  pusher = KafkaPush2Rasa()
  signal.signal(signal.SIGINT, shutdown)
  signal.signal(signal.SIGTERM, shutdown)
  pusher.run()