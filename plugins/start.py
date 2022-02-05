from telethon import events

from app import client
from database.models import User
from loader import GROUP
from plugins.buttons import language_buttons, subscribe_buttons
from plugins.subscribe import check_membership
from plugins.texts import subscribe_messages, start_messages
from plugins.utils import typing_action


@client.on(events.NewMessage(incoming=True, pattern="/start", func=lambda e: e.is_private))
async def start_handler(event: events.newmessage.NewMessage.Event):
    if len(event.message.message.split()) == 2:
        referral_id = int(event.message.message.split()[1])
        if await User.user_exist(referral_id) and not await User.user_exist(event.sender_id):
            user = await client.get_entity(referral_id)
            await client.send_message(GROUP, f'<a href="tg://user?id={user.id}">{user.first_name}</a> '
                                             f'invited <a href="tg://user?id={event.sender_id}">'
                                             f'{event.sender.first_name}</a> to the bot')
            await User.add_referrals(referral_id)
    if not await User.user_exist(event.sender_id):
        await User.create_user(event.sender_id)
        await client.send_message(GROUP, f'<a href="tg://user?id={event.sender_id}">{event.sender.first_name}</a>'
                                         f'joined the bot')
    if await User.get_lang(event.sender_id) is None:
        await client(typing_action(event.chat_id))
        return await event.respond('Select the language', buttons=language_buttons())
    lang = await User.get_lang(event.sender_id)
    if not await check_membership(event.sender_id):
        return await event.respond(subscribe_messages[lang], buttons=subscribe_buttons(lang))
    await client(typing_action(event.chat_id))
    await event.respond(start_messages[lang].format(event.sender_id, event.sender.first_name), buttons=None)
