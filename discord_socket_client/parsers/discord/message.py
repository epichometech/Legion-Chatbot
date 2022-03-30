import discord
from . import user
from . import channel
from . import guild

def textMessage(message):
  retVal = {}
  retVal['author'] = user.parse(message.author)
  retVal['channel'] = channel.parse(message.channel)
  retVal['channel_type'] = message.channel.type
  retVal['guild'] = guild.parse(message.guild)
  retVal['created_at'] = message.created_at.isoformat()
  retVal['edited_at'] = message.edited_at.isoformat() if message.edited_at else None
  retVal['activity'] = message.activity
  retVal['content'] = message.content

  return retVal
