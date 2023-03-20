import asyncio
from aiogram import Bot, Dispatcher, types, filters
import logging
from config import token
import emoji
from shazamio import Shazam


logging.basicConfig(level=logging.INFO)
bot = Bot(token)
dp = Dispatcher(bot)


async def recognize():
    shazam = Shazam()
    out = await shazam.recognize_song("music/file.mp3")
    track = out['track']
    singer = track['subtitle']
    name = track['title']
    cover = track['images']['coverart']
    return name, singer, cover


@dp.message_handler(commands="start")
async def start_send(message: types.Message):
    buttons = [
        [
            types.KeyboardButton(text=emoji.emojize("Голосовым сообщением:microphone:")), types.KeyboardButton(text=emoji.emojize("Файлом:file_folder:"))
            ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder=emoji.emojize(":glowing_star:")
    )
    await message.answer(emoji.emojize(":waving_hand:Привет, я бот для распознавания музыки!:woman_supervillain: "
                                       "Отправь мне в голосовом сообщении музыку, которую ты хочешь распознать, "
                                       "либо отправь ее файлом:headphone::musical_note:"), reply_markup=keyboard)


@dp.message_handler(filters.Text(emoji.emojize("Файлом:file_folder:")))
async def file_choose(message: types.Message):
    await message.answer(emoji.emojize("Хорошо, тогда отправь мне файл с треком, который ты хочешь узнать:winking_face:"))


@dp.message_handler(content_types=types.ContentType.AUDIO)
async def download_and_recognize(message: types.Message):
    await message.answer("Скачиваю файл...")
    await asyncio.wait_for(message.audio.download(destination_file="music/file.mp3"), timeout=30)
    name, singer, cover = await recognize()
    await message.answer_photo(cover, caption=emoji.emojize(f":musical_note:Трек: {name}\n:singer:Исполнитель: {singer}"))


@dp.message_handler(filters.Text(emoji.emojize("Голосовым сообщением:microphone:")))
async def voice_choose(message: types.Message):
    await message.answer(emoji.emojize("Хорошо, тогда отправь мне голосовое сообщение с треком, который ты хочешь узнать:winking_face:"))


@dp.message_handler(content_types=types.ContentType.VOICE)
async def download_and_recognize(message: types.Message):
    await message.answer("Скачиваю файл...")
    await asyncio.wait_for(message.voice.download(destination_file="music/file.mp3"), timeout=30)
    name, singer, cover = await recognize()
    await message.answer_photo(cover, caption=emoji.emojize(f":musical_note:Трек: {name}\n:singer:Исполнитель: {singer}"))


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
