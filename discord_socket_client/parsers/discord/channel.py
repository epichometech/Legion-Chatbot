import discord
from . import guild
from . import user

def parse(channel):
  retVal = {}
  retVal['id'] = channel.id
  retVal['created_at'] = channel.created_at.isoformat()
  retVal['type'] = channel.type

  if isinstance(channel, discord.TextChannel):
    retVal['name'] = channel.name
    retVal['guild'] = guild.parse(channel.guild)
    retVal['mention'] = channel.mention
  elif isinstance(channel, discord.DMChannel):
    retVal['recipient'] = user.parse(channel.recipient)
  
  return retVal

