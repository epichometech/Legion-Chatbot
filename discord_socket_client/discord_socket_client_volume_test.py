import json, sys, socket, os, threading, time
import asyncio
import parsers.discord.discord_parse as discord_parse
import redis

from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic

import discord
from discord.ext.commands import Bot

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN',default=None)
MAXMESSAGES = 20

client = discord.Client(intents=discord.Intents(guilds=True))

async def start():
  await client.start(DISCORD_TOKEN)

def run_it_forever(loop):
  loop.run_forever()

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
      return
    print('Message received')

@client.event
async def on_send_msg(channel, message):
    await channel.send(message)

if __name__ == "__main__":
  if DISCORD_TOKEN:
    asyncio.get_child_watcher()
    loop = asyncio.get_event_loop()
    loop.create_task(start())

    thread = threading.Thread(target=run_it_forever, args=(loop,))
    thread.start()

    client.wait_until_ready()

    print('Waiting to begin volume test')
    time.sleep(10)
    print('Beginning volume test')
    channel = client.get_channel(957213945947635742)
    for i in range(MAXMESSAGES):
      client.dispatch('send_msg', channel, f'Message {i+1} of {MAXMESSAGES}')
    print('Volume test complete')
  else:
    print('No discord token set. Set DISCORD_TOKEN and restart.')
    sys.exit(1)