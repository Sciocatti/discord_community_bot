# * The users to keep track of translations
import json
import os
from deep_translator import GoogleTranslator, exceptions

# * Valid translation languages
valid_translation_languages = [
    "english",
    "afrikaans",
    "spanish"
]

def create_json_users():
    if os.path.exists('src/text_translator/members.json'):
        return
    save_json_users({})

def load_json_users():
    users = {}
    with open('src/text_translator/members.json', 'r') as f:
        users = json.load(f)
    return users

def save_json_users(users):
    with open('src/text_translator/members.json', 'w') as f:
        f.write(json.dumps(users, indent=4))

def save_translation_users(guild, member, translation_language):
    translation_users = load_json_users()
    guild_id = str(guild.id)
    member_id = str(member.id)
    guild_data = translation_users.get(guild_id, {})
    if member_id not in guild_data:
        guild_data[member_id] = []

    if translation_language not in guild_data[member_id]:
        guild_data[member_id].append(translation_language)
    else:
        guild_data[member_id][member_id].remove(translation_language)
    translation_users[guild_id] = guild_data
    save_json_users(translation_users)

async def check_for_translation(message) -> bool:
    translation_users = load_json_users()
    guild = str(message.guild.id)
    member = str(message.author.id)
    if guild not in translation_users:
        return
    if member not in translation_users[guild]:
        return
    await handle_translation(message, translation_users[guild][member])

async def handle_translation(message, languages):
    for language in languages:
        try:
            translation = GoogleTranslator(source='auto', target=language).translate(message.content)
            await message.reply(translation)
        except exceptions.NotValidPayload:
            await message.add_reaction('\N{CROSS MARK}')
