from telethon.tl import functions
from telethon import types

from loader import ADMIN

commands = {
    'en': [
        ('start', 'Run the bot'), ('count', 'Number of users'),
        ('top', 'Top users'), ('change', 'Change the language'),
        ('post', 'Create a post'), ('statistics', 'Statistics')
    ],
    'ru': [
        ('start', 'Запустить бота'), ('count', 'Количество пользователей'),
        ('top', 'Лучшие пользователи'), ('change', 'Изменить язык'),
        ('post', 'Создать пост '), ('statistics', 'Статистика')
    ],
    'uz': [
        ('start', 'Botni ishga tushirish'), ('count', 'Foydalanuvchilar soni'),
        ('top', 'Eng faol foydalanuvchilar'), ('change', 'Tilni o‘zgartirish'),
        ('post', 'Post yaratish'), ('statistics', 'Statistika')
    ]
}


def set_botcommands(user, lang, lang_code):
    count = 6 if user.user_id == ADMIN else 4
    return functions.bots.SetBotCommandsRequest(
        commands=[types.BotCommand(command=command[0], description=command[1]) for command in commands[lang][:count]],
        scope=types.BotCommandScopePeer(user),
        lang_code=lang_code
    )
