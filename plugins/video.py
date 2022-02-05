import os

from telethon import events
from telethon.tl import types

from database.models import User
from loader import client, ADMIN
from plugins.buttons import filename_buttons, language_buttons, subscribe_buttons
from plugins.subscribe import check_membership
from plugins.texts import subscribe_messages, downloading_messages, converting_messages, sending_messages, \
    preferred_name_messages, name_file_messages, file_too_large_messages, invite_messages
from plugins.utils import Progress, typing_action, ffmpegProgress, uploading_audio_action

video_filter = lambda e: e.video or e.media and 'video' in e.media.document.mime_type


@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and video_filter(e)))
async def video_handler(event: events.newmessage.NewMessage.Event):
    if await User.get_lang(event.sender_id) is None:
        await client(typing_action(event.chat_id))
        return await event.respond('Select the language', buttons=language_buttons())
    lang = await User.get_lang(event.sender_id)
    if not await check_membership(event.sender_id):
        return await event.respond(subscribe_messages[lang], buttons=subscribe_buttons(lang))
    document_size = event.document.size
    if document_size > 1.5 * 2 ** 30:
        await client(typing_action(event.chat_id))
        return await event.reply(file_too_large_messages[lang])
    elif document_size > 2 ** 28 and not event.sender_id == ADMIN:
        user_referrals = await User.get_referrals(event.sender_id)
        if user_referrals < 3:
            await event.reply(invite_messages[lang].format(user_referrals))
            await event.respond(f'https://t.me/VideoToAudioOKBot?start={event.sender_id}')
            return
    await client(typing_action(event.chat_id))
    message = await event.respond(downloading_messages[lang])
    progress = Progress(message, lang)
    attributes = event.media.document.attributes
    if len(attributes) > 1:
        file_name = attributes[1].file_name
    else:
        file_name = f"audio.{event.media.document.mime_type.split('/')[1]}"
    file = f'media/{event.sender_id}/{file_name}'
    mp3_file = file[::-1][file[::-1].index('.')+1:][::-1]
    await event.download_media(file=file, progress_callback=progress.progress_callback)
    await message.edit(converting_messages[lang])
    await User.add_conversion(event.sender_id)
    progress_file = f'media/{event.sender_id}/progress.txt'
    bash_code = f'ffmpeg -progress {progress_file} -i {file} -codec:a libmp3lame -q:a 0 {mp3_file}.mp3 -y'
    video_duration = attributes[0].duration
    progress = ffmpegProgress(bash_code, progress_file, message, video_duration, lang)
    await progress.run()
    await message.delete()
    os.remove(file)
    await client(typing_action(event.chat_id))
    await event.respond(name_file_messages[lang], buttons=filename_buttons(lang))


@client.on(events.CallbackQuery(pattern='no'))
async def send_audio_handler(event: events.callbackquery.CallbackQuery.Event):
    await event.delete()
    lang = await User.get_lang(event.sender_id)
    mp3_file = f"media/{event.sender_id}/{os.listdir(f'media/{event.sender_id}')[0]}"
    await client(typing_action(event.chat_id))
    message = await event.respond(sending_messages[lang])
    progress = Progress(message, lang)
    await client(uploading_audio_action(event.sender_id))
    bot = await client.get_me()
    await client.send_file(event.chat_id, mp3_file, progress_callback=progress.progress_callback,
                           force_document=False, caption=f'@{bot.username}')
    await message.delete()
    os.remove(mp3_file)


get_filename_users = set()


@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and e.sender_id in get_filename_users))
async def send_mp3_handler(event: events.newmessage.NewMessage.Event):
    lang = await User.get_lang(event.sender_id)
    mp3_file = f"media/{event.sender_id}/{os.listdir(f'media/{event.sender_id}')[0]}"
    new_filename = f'media/{event.sender_id}/{event.message.text}.mp3'
    os.rename(mp3_file, new_filename)
    await client(typing_action(event.chat_id))
    message = await event.respond(sending_messages[lang])
    print(type(message))
    progress = Progress(message, lang)
    await client(uploading_audio_action(event.sender_id))
    bot = await client.get_me()
    await client.send_file(event.chat_id, new_filename, progress_callback=progress.progress_callback,
                           force_document=False, caption=f'@{bot.username}')
    await message.delete()
    get_filename_users.remove(event.sender_id)
    os.remove(new_filename)


@client.on(events.CallbackQuery(pattern='yes'))
async def get_filename_handler(event: events.callbackquery.CallbackQuery.Event):
    await event.delete()
    lang = await User.get_lang(event.sender_id)
    await client(typing_action(event.chat_id))
    await event.respond(preferred_name_messages[lang])
    get_filename_users.add(event.sender_id)
