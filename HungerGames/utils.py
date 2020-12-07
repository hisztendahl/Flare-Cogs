import discord
import re

def strip_mentions(message: discord.Message, text):
    members = message.mentions
    channels = message.channel_mentions
    roles = message.role_mentions

    for m in members:
        name = m.nick if m.nick is not None else m.name
        text = re.sub(m.mention, name, text)

    for c in channels:
        text = re.sub(c.mention, c.name, text)

    for r in roles:
        text = re.sub(r.mention, r.name, text)

    return text


def sanitize_here_everyone(text):
    text = re.sub('@here', '@\u180Ehere', text)
    text = re.sub('@everyone', '@\u180Eeveryone', text)
    return text


def sanitize_special_chars(text):
    text = re.sub('@', '\\@', text)
    text = re.sub('~~', '\\~\\~', text)
    text = re.sub('\*', '\\*', text)
    text = re.sub('`', '\\`', text)
    text = re.sub('_', '\\_', text)
    return text.strip()