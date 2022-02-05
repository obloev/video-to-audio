import asyncio
import os
import re
import time

from telethon import types, functions

from loader import client
from plugins.texts import down_up_messages, converting_progress_messages, converting_messages


def size(byte: int) -> str:
    raised_to_pow = 0
    dict_power_n = {0: "B", 1: "K", 2: "M", 3: "G", 4: "T", 5: "P"}
    while byte > 2 ** 10:
        byte /= 2 ** 10
        raised_to_pow += 1
    if raised_to_pow < 2:
        return str(round(byte)) + " " + dict_power_n[raised_to_pow] + "B"
    return str(round(byte, 1)) + " " + dict_power_n[raised_to_pow] + "B"


def time_f(seconds: int) -> str:
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        (f"{str(hours).zfill(2)}:" if hours else "00:")
        + (f"{str(minutes).zfill(2)}:" if minutes else "00:")
        + (f"{str(seconds).zfill(2)}" if seconds else "00")
    )
    return tmp


def progress_bar(percent: int) -> str:
    count = 3 * percent // 20
    return '{}{}'.format('⬛' * count, '⬜' * (15 - count))


class Progress:
    def __init__(self, message, lang, sending=False):
        self.message = message
        self.lang = lang
        self.sending = sending
        self.last_size = 0
        self.last_time = time.time()
        self.count = 0

    async def progress_callback(self, current, total):
        now = time.time()
        percent = int((current / total) * 100)
        speed = round((current - self.last_size) / (now - self.last_time))
        etime = (total - current) // speed
        self.last_size = current
        self.last_time = now
        if self.count % 6 == 0:
            if self.sending:
                await client(uploading_audio_action(self.message.from_id))
            await self.message.edit(
                down_up_messages[self.lang].format(
                    progress_bar(percent), self.message.text, percent, size(current),
                    size(total), size(speed), time_f(etime)
                ))
        self.count += 1


def typing_action(chat_id):
    return functions.messages.SetTypingRequest(chat_id, types.SendMessageTypingAction())


def uploading_audio_action(chat_id):
    return functions.messages.SetTypingRequest(chat_id, types.SendMessageUploadAudioAction(600))


class ffmpegProgress:
    def __init__(self, bash, progress, message, duration, lang):
        self.time = time.time()
        self.bash = bash
        self.progress = progress
        self.message = message
        self.duration = duration
        self.lang = lang

    async def run(self):
        open(self.progress, "w")
        proce = await asyncio.create_subprocess_shell(
            self.bash, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        while proce.returncode != 0:
            await asyncio.sleep(1.5)
            progress_file = open(self.progress, "r+")
            text = progress_file.read()
            us = re.findall("out_time_ms=(\\d+)", text)
            if us:
                seconds = round(int(re.findall("out_time_ms=(\\d+)", text)[-1]) / 10**6)
                percent = round(seconds * 100 / self.duration)
                now = time.time()
                time_delta = round(now - self.time)
                if percent:
                    etime = round(100 * time_delta / percent) - time_delta
                else:
                    etime = 0
                await self.message.edit(converting_progress_messages[self.lang].format(
                    progress_bar(percent), converting_messages[self.lang], percent, time_f(etime)
                ))
            progress_file.close()
        return os.remove(self.progress)
