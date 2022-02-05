langs = {
    'en': '🇺🇸 english',
    'ru': '🇷🇺 русский',
    'uz': '🇺🇿 o‘zbekcha'
}

start_messages = {
    'en': 'Hi <a href="tg://user?id={}">{}</a>. This bot will convert the video you sent to audio format',
    'ru': 'Привет <a href="tg://user?id={}">{}</a>. Этот бот конвертирует видео, которое вы отправляете, в аудиоформат',
    'uz': 'Salom <a href="tg://user?id={}">{}</a>. Bu bot siz yuborgan videoni audio formatga o‘tkazib beradi',
}

subscribe_messages = {
    'en': 'Please subscribe to the channel below to use the bot and click the confirm button',
    'ru': 'Пожалуйста, подпишитесь на канал ниже, чтобы использовать бота, и нажмите кнопку подтверждения.',
    'uz': "Iltimos, botdan foydalanish uchun quyidagi kanalga a'zo bo‘ling va tasdiqlash tugmasini bosing"
}

subscribe_buttons_messages = {
    'en': ('Channel', 'Confirm'),
    'ru': ('Канал', 'Подтверждение'),
    'uz': ('Kanal', 'Tasdiqlash'),
}

please_wait_messages = {
    'uz': 'Iltimos biroz kuting ...',
    'ru': 'Пожалуйста подождите ...',
    'en': 'Please wait ...'
}

count_messages = {
    'en': 'Number of users {}',
    'ru': 'Количество пользователей {}',
    'uz': 'Foydalanuvchilar soni {} ta'
}

not_member_messages = {
    'en': "You aren't a member of the channel",
    'ru': "Вы не являетесь участником канала",
    'uz': "Siz kanalga a'zo bo‘lmagansiz",
}

top_users_messages = {
    'en': '<b>{}.</b> <a href="tg://user?id={}">{}</a> - {} times\n',
    'ru': '<b>{}.</b> <a href="tg://user?id={}">{}</a> - {} раз\n',
    'uz': '<b>{}.</b> <a href="tg://user?id={}">{}</a> - {} marta\n'
}

statistics_messages = {
    'en': ('<b>Conversions:</b> {}\n\n', '<b>{}:</b> {} ({}%)\n'),
    'ru': ('<b>Конверсии:</b> {}\n\n', '<b>{}:</b> {} ({}%)\n'),
    'uz': ('<b>O‘girishlar:</b> {}\n\n', '<b>{}:</b> {} ({}%)\n'),
}

send_post_messages = {
    'en': '<b>Sent:</b> {}\n<b>Blocked users:</b> {}\n<b>Deactivated users:</b> {}',
    'ru': '<b>Отправил:</b> {}\n<b>Заблокированные пользователи:</b> {}\n<b>Деактивированные пользователи:</b> {}</b>',
    'uz': "<b>Yuborildi:</b> {}\n<b>Bloklangan foydalanuvchilar:</b> {}\n<b>Mavjud bo'lmagan foydalanuvchilar:</b> {}",
}

cancel_posting_messages = {
    'en': 'Click /cancel to cancel posting',
    'ru': 'Нажмите /cancel, чтобы отменить публикацию',
    'uz': "Post yuborish jarayonini bekor qilish uchun /cancel tugmasini bosing",
}

complete_messages = {
    'en': ('Complete!', 'Time'),
    'ru': ('Сделанный!', 'Время'),
    'uz': ("Bajarildi!", 'Vaqt')
}

get_post_messages = {
    'en': 'OK, send me the post',
    'ru': 'Хорошо, пришлите мне пост',
    'uz': "Yaxshi, menga postni jo'nating"
}

downloading_messages = {
    'en': 'Downloading ...',
    'ru': 'Скачивание ...',
    'uz': "Yuklab olinyapti ..."
}

converting_messages = {
    'en': 'Converting ...',
    'ru': 'Преобразование ...',
    'uz': "O‘girilmoqda ..."
}

sending_messages = {
    'en': 'Sending ...',
    'ru': 'Отправка ...',
    'uz': "Yuborilmoqda ..."
}

name_file_messages = {
    'en': 'Do you name the created file?',
    'ru': 'Вы называете созданный файл?',
    'uz': "Yaratilgan faylga nom qo‘yasizmi?"
}

preferred_name_messages = {
    'en': 'Type your preferred name',
    'ru': 'Введите имя, которое вам нравится',
    'uz': "Ma'qul ko‘rgan nomingizni yozing"
}

yes_messages = {
    'en': 'Yes',
    'ru': 'Да',
    'uz': 'Ha',
}

no_messages = {
    'en': 'No',
    'ru': 'Нет',
    'uz': "Yo‘q",
}

down_up_messages = {
    'en': '{}\n\n<b>{} ({}%)</b>\n<b>Progress:</b> {} of {}\n<b>Speed:</b> {}/s\n<b>Time:</b> {}',
    'ru': '{}\n\n<b>{} ({}%)</b>\n<b>Процесс:</b> {} / {}\n<b>Скорость:</b> {}/s\n<b>Время:</b> {}',
    'uz': '{}\n\n<b>{} ({}%)</b>\n<b>Jarayon:</b> {} / {}\n<b>Tezlik:</b> {}/s\n<b>Vaqt:</b> {}'
}

converting_progress_messages = {
    'en': '{}\n\n<b>{} ({}%)</b>\n<b>Time left:</b> {}',
    'ru': '{}\n\n<b>{} ({}%)</b>\n<b>Осталось времени:</b> {}',
    'uz': '{}\n\n<b>{} ({}%)</b>\n<b>Qolgan vaqt:</b> {}'
}

file_too_large_messages = {
    'en': 'The file size is too large.\n<b>Limit:</b> 1.5 GB',
    'ru': 'Размер файла слишком велик.\n<b>Ограничение:</b> 1.5 ГБ',
    'uz': 'Fayl hajmi juda katta.\n<b>Limit:</b> 1.5 GB'
}

invite_messages = {
    'en': 'To convert videos larger than <b>256 MB</b> to audio format, you need to invite 3 friends to the bot. '
          'The invitation is sent below.\n\n<b>Number of friends you have invited:</b> {}',
    'ru': 'Чтобы конвертировать видео размером более <b>256 МБ</b> в аудио формат, вам нужно пригласить в бота 3 '
          'друзей. Приглашение отправлено ниже.\n\n<b>Количество приглашенных вами друзей:</b> {}',
    'uz': '256 MB dan katta videolarni audio formatga o‘tkazish uchun 3 ta do‘stingizni botga taklif qilishingiz '
          'kerak. Taklif qilish uchun havolda quyida yuborilgan.\n\n<b>Taklif qilgan do‘stlaringiz soni:</b> {} ta'
}
