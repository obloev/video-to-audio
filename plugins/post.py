import time

from telethon import events
from telethon.errors import InputUserDeactivatedError, UserIsBlockedError

from database.models import User
from loader import client, ADMIN
from plugins.buttons import language_buttons
from plugins.texts import please_wait_messages, send_post_messages, cancel_posting_messages, complete_messages, \
    get_post_messages
from plugins.utils import typing_action, time_f

get_post = set()
posting = set()


@client.on(events.NewMessage(incoming=True, from_users=[ADMIN], pattern='/cancel'))
async def cancel_operation(event):
    posting.remove(event.sender_id)
    await client(typing_action(event.chat_id))
    await event.reply('Canceled')


get_post_filter = lambda e: e.is_private and e.sender_id in get_post


@client.on(events.NewMessage(incoming=True, from_users=[ADMIN], func=get_post_filter))
async def get_post_handler(event):
    lang = await User.get_lang(event.sender_id)
    await client(typing_action(event.sender_id))
    message = await event.respond(please_wait_messages[lang])
    post = event.message
    all_users = await User.get_users()
    sent = 0
    deactivated = 0
    blocked = 0
    text = send_post_messages[lang]
    await client(typing_action(event.chat_id))
    cancel_message = await event.respond(cancel_posting_messages[lang])
    start_time = time.time()
    for user in all_users:
        if event.sender_id in posting:
            user_id = user.user_id
            try:
                await client.send_message(user_id, post)
                sent += 1
            except InputUserDeactivatedError:
                deactivated += 1
                await User.delete_user(user_id)
            except UserIsBlockedError:
                blocked += 1
            if (sent + deactivated + blocked) % 10 == 0:
                await message.edit(text.format(sent, deactivated, blocked))
        else:
            break
    else:
        posting.remove(event.sender_id)
    end_time = time.time()
    get_post.remove(event.sender_id)
    await message.delete()
    await cancel_message.delete()
    await client(typing_action(event.chat_id))
    await event.respond(f"<b>{complete_messages[lang][0]}</b>\n\n{text.format(sent, deactivated, blocked)}\n"
                        f"<b>{complete_messages[lang][1]}:</b> {time_f(round(end_time - start_time))}")


@client.on(events.NewMessage(incoming=True, from_users=[ADMIN], pattern='/post'))
async def post_to_users(event):
    if await User.get_lang(event.sender_id) is None:
        await client(typing_action(event.chat_id))
        return await event.respond('Select the language', buttons=language_buttons())
    lang = await User.get_lang(event.sender_id)
    await client(typing_action(event.chat_id))
    await event.respond(get_post_messages[lang])
    get_post.add(event.sender_id)
    posting.add(event.sender_id)
