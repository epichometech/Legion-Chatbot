import json, sys, socket, os
import parsers.discord.discord_parse as discord_parse
import redis

from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic

import discord
from discord.ext.commands import Bot



KAFKA_SERVER = os.getenv('KAFKA_SERVER',default='kafka')
KAFKA_PORT = os.getenv('KAFKA_PORT',default='9092')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN',default=None)
TOPICS= [
  'discordMessagesIncoming'
]
REDIS_SERVER = os.getenv('REDIS_SERVER',default='redis')
REDIS_PORT = os.getenv('REDIS_PORT',default=6379)
REDIS_ENABLE = os.getenv('REDIS_ENABLE', default=0)

client = discord.Client()

def on_errback(err):
  sys.stderr.write(f'%% Message failed delivery: {err}\n')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        pass
        #return
    try:
      parsedMessage = discord_parse.parse_discord_object(message)
      if redisClient:
        if redisClient.zadd('discordIncomingMessages', {message.id:message.created_at.timestamp()}, nx=True) > 0:
          F = producer.send('discordMessagesIncoming',parsedMessage)
          F.add_errback(on_errback)
        else:
          return
      F = producer.send('discordMessagesIncoming',parsedMessage)
      F.add_errback(on_errback)
    except Exception as e:
      raise e
    producer.flush()
    print(f'Message sent')

if __name__ == "__main__":
  if DISCORD_TOKEN:
    producer = KafkaProducer(
      bootstrap_servers=[f'{KAFKA_SERVER}:{KAFKA_PORT}'],
      value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
    admin = KafkaAdminClient(bootstrap_servers=[f'{KAFKA_SERVER}:{KAFKA_PORT}'])
    for item in TOPICS:
      try:
        topic = NewTopic(name=item, num_partitions=1, replication_factor=1)
        admin.create_topics([topic])
      except Exception:
        print(f'Topic {item} is already created')
    admin.close()
    admin = None
    if REDIS_ENABLE:
      redisClient = redis.Redis(
        host=REDIS_SERVER,
        port=REDIS_PORT
      )
    else:
      redisClient = None
    client.run(DISCORD_TOKEN)
  else:
    print('No discord token set. Set DISCORD_TOKEN and restart.')
    sys.exit(1)