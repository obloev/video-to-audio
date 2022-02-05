from telethon import events
from telethon.errors import UserNotParticipantError
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.tl.types import PeerChannel

from database.models import User
from loader import client, CHANNEL
from plugins.texts import not_member_messages, start_messages
from plugins.utils import typing_action


async def check_membership(user_id):
    try:
        channel = await client.get_entity(PeerChannel(CHANNEL))
        sub = await client(GetParticipantRequest(channel, user_id))
        status = sub.stringify()
        if 'left' in status:
            return False
        return True
    except UserNotParticipantError:
        return False


@client.on(events.CallbackQuery(pattern='confirm'))
async def confirmation(event: events.callbackquery.CallbackQuery.Event):
    status = await check_membership(event.sender_id)
    lang = await User.get_lang(event.sender_id)
    if status:
        await event.delete()
        await client(typing_action(event.chat_id))
        await event.respond(start_messages[lang].format(event.sender_id, event.sender.first_name))
    else:
        await event.answer(not_member_messages[lang], alert=True)
