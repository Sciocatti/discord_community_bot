import math
import json
import random
import traceback

from src.file_logger import logger
from src import text_translator

# * How long to wait before deleting messages. We don't want to litter.
DELETE_DELAY = 300.0

# * Valid translation languages
valid_translation_languages = [
    "english",
    "afrikaans",
    "spanish"
]

async def tell_joke(message):
    # * !joke
    """
        Sends a random joke to the channel `message` came from.
    """
    jokes = []
    try:
        with open("src/commands/social/jokes.json") as f:
            jokes = json.load(f)
            await message.add_reaction('\N{WHITE HEAVY CHECK MARK}')

    except Exception as e:
        jokes = [
            {
                "setup": "Why did the chicken cross the road?",
                "punchline": "To find where you placed the jokes."
            }
        ]
        logger.error(f"Could not open jokes.json, reason: {e}")
        logger.error(traceback.format_exc().replace("\n", "\r\n\t"))
        await message.add_reaction('\N{CROSS MARK}')

    joke = random.choice(jokes)
    reply = await message.reply(f"{joke['setup']}\r\n\r\n||{joke['punchline']}||  _(Click to reveal)_")
    await message.delete(delay=DELETE_DELAY)
    await reply.delete(delay=DELETE_DELAY)

async def log_help(message):
    member = message.author
    await member.create_dm()
    await member.dm_channel.send(
        (
            f"Hello {member.name}!\r\n\r\n"
            f"You have requested help regarding the commands for the channel `{message.channel.name}`. The following commands are available:\r\n"
            "`!help` -> Send help to the user DM for using commands on this channel.\r\n"
            "`!joke` -> Send a random joke. The joke will be deleted after 5 minutes.\r\n"
            "`!shuffle` -> Randomly distributes all users on the voice channels into groups.\r\n"
            "\r\n"
            "Please note that command messages _you_ send on this channel will get deleted after 5 minutes. This is to keep the chat clean."
        )
    )
    await message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await message.delete(delay=DELETE_DELAY)

async def shuffle_members(message):
    """ We are aiming for groups of 3 people. If needed, groups can be 4 as well"""
    guild = message.guild
    afk_channel = guild.afk_channel
    voice_channels = guild.voice_channels
    members = []
    channels = []
    lone_member = None

    for channel in voice_channels:
        if channel != afk_channel:
            members += channel.members
            channels.append(channel)

    random.shuffle(members)
    if len(members) % 3 == 1:
        # We will end up with one person alone, so simply add them to the first channel
        lone_member = members[-1]
        members = members[:-1]
    ideal_amount_of_channels = min(math.ceil(len(members) / 3), len(channels))

    for i in range(len(members)):
        await members[i].move_to(channels[i%ideal_amount_of_channels])

    if lone_member:
        await lone_member.move_to(channels[0])
  
    await message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await message.delete(delay=DELETE_DELAY)
    
async def regroup_members(message):
    guild = message.guild
    afk_channel = guild.afk_channel
    voice_channels = guild.voice_channels
    members = []
    channels = []

    for channel in voice_channels:
        if channel != afk_channel:
            members += channel.members
            channels.append(channel)

    for member in members:
        await member.move_to(channels[0])
        
    await message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await message.delete(delay=DELETE_DELAY)

async def add_member_translation(message):
    content = message.content.split(" ")[-1]
    if content not in valid_translation_languages:
        await message.add_reaction('\N{CROSS MARK}')
        reply = await message.reply(f"You must specify the language to translate to out of {valid_translation_languages}")
        await message.delete(delay=DELETE_DELAY)
        await reply.delete(delay=DELETE_DELAY)
        return

    member = message.author
    guild = message.guild
    text_translator.save_translation_users(guild, member, content)
    await message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
    await message.delete(delay=DELETE_DELAY)

command_map = {
    "!help": log_help,
    "!joke": tell_joke,
    "!shuffle": shuffle_members,
    "!regroup": regroup_members,
    "!translation": add_member_translation
}