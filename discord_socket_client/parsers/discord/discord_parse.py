import discord
import json

MESSAGE_TOPIC = {
  "textMessage": "discordTextMessageIncoming"
}

def parse_discord_text_message(textMessage):
  retVal = {}
  retVal['author'] = parse_discord_object(textMessage.author)
  retVal['channel'] = parse_discord_object(textMessage.channel)
  retVal['guild'] = parse_discord_object(textMessage.guild)
  retVal['created_at'] = textMessage.created_at.isoformat()
  retVal['edited_at'] = textMessage.edited_at.isoformat() if textMessage.edited_at else None
  retVal['activity'] = textMessage.activity
  retVal['content'] = textMessage.content

  return retVal

def parse_discord_member(member):
  retVal = {}
  retVal['guild'] = parse_discord_guild(member.guild)
  retVal['guild_permissions'] = parse_discord_object(member.guild_permissions)
  retVal['display_name'] = member.display_name
  retVal['name'] = member.name
  retVal['joined_at'] = member.joined_at.isoformat() if member.joined_at else None
  retVal['nick'] = member.nick
  retVal['pending'] = member.pending
  retVal['premium_since'] = member.premium_since.isoformat() if member.premium_since else None
  retVal['raw_status'] = member.raw_status

  valUser = parse_discord_user(member)
  retVal = {**retVal, **valUser}

  return retVal

def parse_discord_user(user):
  retVal = {}
  retVal['id'] = user.id
  retVal['name'] = user.name
  retVal['system'] = user.system
  retVal['created_at'] = user.created_at.isoformat()
  retVal['discriminator'] = user.discriminator
  
  return retVal

def parse_discord_guild(guild):
  retVal = {}
  retVal['id'] = guild.id
  retVal['name'] = guild.name

  return retVal

def parse_discord_permissions(permissions):
  return None

def parse_discord_channel(channel):
  return None

def parse_discord_dmchannel(channel):
  return None

def parse_discord_groupchannel(channel):
  return None

def parse_discord_textchannel(channel):
  retVal = {}
  retVal['id'] = channel.id
  retVal['name'] = channel.name
  retVal['guild'] = parse_discord_object(channel.guild)

  return retVal

def parse_discord_object(discordObj):
  if isinstance(discordObj,discord.Message):
    return parse_discord_text_message(discordObj)
  elif isinstance(discordObj,discord.CallMessage):
    print(f'It is a CallMessage')
    return None
  elif isinstance(discordObj,discord.Member):
    return parse_discord_member(discordObj)
  elif isinstance(discordObj,discord.User):
    return parse_discord_user(discordObj)
  elif isinstance(discordObj,discord.Guild):
    return parse_discord_guild(discordObj)
  elif isinstance(discordObj,discord.DMChannel):
    return parse_discord_dmchannel(discordObj)
  elif isinstance(discordObj,discord.GroupChannel):
    return parse_discord_groupchannel(discordObj)
  elif isinstance(discordObj,discord.TextChannel):
    return parse_discord_textchannel(discordObj)
  elif isinstance(discordObj, discord.Permissions):
    return parse_discord_permissions(discordObj)
  else:
    print(type(discordObj))