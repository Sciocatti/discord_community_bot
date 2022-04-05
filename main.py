import os
import uuid
import discord
import traceback
from discord.ext import tasks
from dotenv import load_dotenv

import src
from src.file_logger import logger

load_dotenv(dotenv_path='secret.env')
TOKEN = os.getenv('DISCORD_TOKEN')

if not TOKEN:
    logger.error("secrets not loaded. Quitting")
    raise SystemExit("secrets not loaded. Quitting")

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

src.text_translator.create_json_users()

# ! Function Routers
# ! --------------------
async def social_channel_handler(message):
    """
        All commands sent from the social channel.
    """
    command = message.content.split(" ")[0]
    if command not in src.commands.social.command_map:
        return

    await src.commands.social.command_map[command](message)

async def handle_regular_message(message):
    await src.text_translator.check_for_translation(message)
    return

@tasks.loop(seconds=1)
async def looped_function_handler():
    # This loop will be called every second.
    # Simply call your functions here and check whether the
    # time for action is correct.
    pass

# ! Discord Event Handlers
# ! ---------------------------

@client.event
async def on_ready():
    """
        The bot has successfully logged in to Discord
    """
    logger.info(f'{client.user} has connected to Discord.')

@client.event
async def on_member_join(member):
    """
        A new member has joined this server. Lets send them a welcome message.
    """
    await member.create_dm()
    await member.dm_channel.send(
        (
            f"Hi {member.name}, welcome to the FastCommunity!\r\n"
            "We have a social coffee every workday from 8.30 to 9.00 SAST. We would love to see you there! The team will guide you from there.\r\n"
            "\r\n"
            "Some stuff if you are new to Discord:\r\n"
            "- During the social coffee, simply click on the speaker icon on a voice-channel where people are gathered to join that channel.\r\n"
            "- If you cannot hear anybody, or nobody can hear you: change your input/output devices at `User Settings` (gear icon bottom left) -> `Voice & Video`.\r\n"
            "- You can mute an overactive text-channel by right-clicking on the channel -> `Mute Channel` -> `Until I turn it back on`\r\n"
            "\r\n"
            "Finally, if you have any issues contact Victor at victor.sciocatti@fastcomm.com to help you out!"
        )
    )

@client.event
async def on_message(message):
    """
        Someone sent a message. Handle it.

        NOTE: Most messages are not for us, so we just ignore them.
    """
    if message.author == client.user:
        # * The message got sent from the bot itself. Ignore our own stuff.
        return

    # * Link the name of a text channel to a function router.
    # If a command (message starting with !) comes in from this text channel then that function
    # will handle it.
    message_handlers = {
        "social": social_channel_handler
    }
    is_command = True if (len(message.content) > 0) and (message.content[0] == '!') else False
    if is_command and (message.channel.name in message_handlers):
        # We do have a router for that channel, so process it.
        await message_handlers[message.channel.name](message)
        return

    # * Now we are facing a regular message. We might want to parse it for some
    # * stuff, such as translation
    await handle_regular_message(message)


@client.event
async def on_error(event, *args, **kwargs):
    """
        If something broke while handling a message, log an unique ID for the
        error and report that to the user. They can contact you with that ID,
        and you can look it up in the logs in output.log
    """
    if event != 'on_message':
        raise

    message = args[0]
    crash_code = str(uuid.uuid4())
    logger.error(f"Code {crash_code}: Exception handling message: {message}")
    logger.error(traceback.format_exc().replace("\n", "\r\n\t"))
    await message.clear_reactions()
    await message.add_reaction('\N{CROSS MARK}')
    await message.reply(f"Something crashed, but it has been logged. Look for '{crash_code}' in the logs.")

@looped_function_handler.before_loop
async def looped_function_handler_before():
    await client.wait_until_ready()

looped_function_handler.start()
client.run(TOKEN)
