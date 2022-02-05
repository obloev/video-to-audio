from database.models import User
from loader import client, ADMIN
from telethon import events

from plugins.buttons import language_buttons
from plugins.texts import count_messages, top_users_messages, please_wait_messages, statistics_messages
from plugins.utils import typing_action


@client.on(events.NewMessage(incoming=True, pattern="/count", func=lambda e: e.is_private))
async def count_handler(event: events.newmessage.NewMessage.Event):
    if await User.get_lang(event.sender_id) is None:
        await client(typing_action(event.chat_id))
        return await event.respond('Select language', buttons=language_buttons())
    lang = await User.get_lang(event.sender_id)
    await client(typing_action(event.chat_id))
    message = await event.respond(please_wait_messages[lang])
    count = await User.users_count()
    return await message.edit(count_messages[lang].format(count))


@client.on(events.NewMessage(incoming=True, pattern="/top", func=lambda e: e.is_private))
async def top_users_handler(event: events.newmessage.NewMessage.Event):
    if await User.get_lang(event.sender_id) is None:
        await client(typing_action(event.chat_id))
        return await event.respond('Select language', buttons=language_buttons())
    lang = await User.get_lang(event.sender_id)
    await client(typing_action(event.chat_id))
    message = await event.respond(please_wait_messages[lang])
    top_users = await User.get_top_users(5)
    text = ''
    for n, user in enumerate(top_users, start=1):
        user_info = await client.get_entity(user.user_id)
        text += top_users_messages[lang].format(n, user_info.first_name, user.conversions)
    return await message.edit(text)


@client.on(events.NewMessage(incoming=True, pattern="/change", func=lambda e: e.is_private))
async def change_lang_handler(event: events.newmessage.NewMessage.Event):
    return await event.respond('Select language', buttons=language_buttons())


@client.on(events.NewMessage(incoming=True, pattern="/statistics", from_users=[ADMIN], func=lambda e: e.is_private))
async def statistics_handler(event: events.newmessage.NewMessage.Event):
    if await User.get_lang(event.sender_id) is None:
        await client(typing_action(event.chat_id))
        return await event.respond('Select language', buttons=language_buttons())
    lang = await User.get_lang(event.sender_id)
    await client(typing_action(event.chat_id))
    message = await event.respond(please_wait_messages[lang])
    converions = await User.get_conversions()
    text = statistics_messages[lang][0].format(converions)
    langs = {}
    users = await User.get_users()
    for user in users:
        if user.lang not in langs:
            langs[user.lang] = 1
        else:
            langs[user.lang] += 1
    all_langs = sum(langs.values())
    for lang in langs:
        text += statistics_messages[lang][1].format(lang, langs[lang], round(langs[lang] * 100 / all_langs))
    return await message.edit(text)
