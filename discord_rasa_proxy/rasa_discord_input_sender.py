import json, sys, time
from json.decoder import JSONDecodeError
from confluent_kafka import Consumer, KafkaException

conf = {
  'bootstrap.servers': "kafka:9092",
  'group.id': 'rasa',
  'session.timeout.ms': 6000,
  'auto.offset.reset': 'earliest'
}

class KafkaPush2Rasa:
  def __init__(self, conf):
    self.consumer = Consumer(conf)

  def print_assignment(self, consumer, partitions):
    print(f'Assignment: {partitions}')

  def delivery_callback(self, err, msg):
    if err:
      sys.stderr.write('%% Message failed delivery: %s\n' % err)

  def run(self):
    self.consumer.subscribe(['discordMessagesIncoming'], on_assign=self.print_assignment)

    try:
      while True:
        msg = self.consumer.poll(timeout=1.0)
        if msg is None:
          continue
        if msg.error():
          raise KafkaException(msg.error())
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

if __name__ == "__main__":
  pusher = KafkaPush2Rasa(conf)
  pusher.run()