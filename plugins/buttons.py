from telethon import Button

from loader import CHANNEL_URL
from plugins.texts import langs, subscribe_buttons_messages, yes_messages, no_messages


def language_buttons():
    buttons = []
    for key in langs:
        buttons.append(Button.text(langs[key], resize=True))
    return [buttons]


def subscribe_buttons(lang):
    return [[
        Button.url(subscribe_buttons_messages[lang][0], url=CHANNEL_URL),
        Button.inline(subscribe_buttons_messages[lang][1], data='confirm'),
    ]]


def filename_buttons(lang):
    return [[
        Button.inline(yes_messages[lang], data='yes'),
        Button.inline(no_messages[lang], data='no')
    ]]
