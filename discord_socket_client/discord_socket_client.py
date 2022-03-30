import discord
import json, sys, socket
import parsers.discord.discord_parse as discord_parse
from confluent_kafka import Producer

client = discord.Client()

conf = {
  'bootstrap.servers': "kafka:9092",
}

producer = Producer(conf)

'''This needs to be changed to a full config to include kafka topics'''
'''configuration file should be restructured to a yaml file located in the mounted volume'''
with open('secrets.json') as secrets:
  data = json.load(secrets)

def delivery_callback(err, msg):
  if err:
    sys.stderr.write('%% Message failed delivery: %s\n' % err)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

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

client.run(data['token'])