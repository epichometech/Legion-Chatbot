import discord
from . import guild

def parse(user):
  retVal = {}
  retVal['id'] = user.id
  retVal['name'] = user.name
  retVal['display_name'] = user.display_name
  retVal['bot'] = user.bot

  if isinstance(user, discord.Member):
    retVal['guild'] = guild.parse(user.guild)
    retVal['nick'] = user.nick

  return retVal

