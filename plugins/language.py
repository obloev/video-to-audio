from telethon import events, Button

from database.models import User
from loader import client
from plugins.botcommands import set_botcommands
from plugins.buttons import subscribe_buttons
from plugins.subscribe import check_membership
from plugins.texts import langs, subscribe_messages, start_messages
from plugins.utils import typing_action


@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and e.message.text in langs.values()))
async def language_handler(event: events.newmessage.NewMessage.Event):
    user = await event.get_sender()
    lang = list(langs.keys())[list(langs.values()).index(event.message.text)]
    await User.set_lang(event.sender_id, lang)
    await client(typing_action(event.chat_id))
    await event.respond(event.message.text, buttons=Button.clear())
    await client(set_botcommands(event.input_chat, lang, user.lang_code))
    if not await check_membership(event.sender_id):
        await client(typing_action(event.chat_id))
        return await event.respond(subscribe_messages[lang], buttons=subscribe_buttons(lang))
    await client(typing_action(event.chat_id))
    await event.respond(start_messages[lang].format(event.sender_id, event.sender.first_name), buttons=None)
