import json, sys, socket, os
import parsers.discord.discord_parse as discord_parse
from confluent_kafka import Producer

import discord
from discord.ext.commands import Bot

client = discord.Client()

KAFKA_SERVER = os.getenv('KAFKA_SERVER',default='kafka')
KAFKA_PORT = os.getenv('KAFKA_PORT',default='9092')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN',default=None)

conf = {
  'bootstrap.servers': f'{KAFKA_SERVER}:{KAFKA_PORT}',
}

producer = Producer(conf)

def delivery_callback(err, msg):
  if err:
    sys.stderr.write(f'%% Message failed delivery: {err}\n')

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    try:
      parsedMessage = discord_parse.parse_discord_object(message)
      '''This topic needs to be a configuration variable'''
      producer.produce('discordMessagesIncoming',json.dumps(parsedMessage), callback=delivery_callback)
    except BufferError:
      sys.stderr.write('%% Local producer queue is full (%d messages awaiting delivery): try again\n' %
        len(producer))
    except Exception as e:
      raise e
    producer.flush()
    print(f'Message sent')

if DISCORD_TOKEN:
  client.run(DISCORD_TOKEN)
else:
  print('No discord token set. Set DISCORD_TOKEN and restart.')
  sys.exit(1)