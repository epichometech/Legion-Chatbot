import discord

def parse(guild):
  retVal = {}
  retVal['id'] = guild.id
  retVal['name'] = guild.name

  return retVal