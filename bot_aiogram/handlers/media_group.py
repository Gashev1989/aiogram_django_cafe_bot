from aiogram import Bot
from aiogram.types import (
    Message, ReplyKeyboardRemove
)


async def get_media_group(message: Message, bot: Bot):
    """Сеты для оформления заказа."""
    media = [None]
    await message.answer_media_group(media)
    await message.answer(
        'Выберите сеты и закажите в формате:\n'
        '"номер сета - количество сетов", например,\n'
        '"1-1, 2-3" - означает, что выбраны\n'
        '"сет №1 - 1 шт. и сет № 2 - 3 шт."\n',
        reply_markup=ReplyKeyboardRemove()
    )


async def watch_media_group(message: Message, bot: Bot):
    """Сеты для просмотра перед бронированием стола."""
    media = [None]
    await message.answer_media_group(media)
