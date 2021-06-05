from fsm import DataInput
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

from fsm import DataInput
from sqlighter import SQLighter
from function import karmic_func

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = SQLighter('db/database.db')


@dp.message_handler(commands=['top'])
async def start(message: types.Message):
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        await message.answer("Тут типа ТОП")

@dp.message_handler()
async def karma_trrigers(message: types.Message):
    if message.chat.type == 'group' or message.chat.type == 'supergroup':
        if not message.reply_to_message == None:
            if not message.reply_to_message.from_user.is_bot:
                message_list = message.text.split(' ')
                cleared_text = karmic_func.clear_text(message_list[0])
                await karmic_func.plus_or_minus(message, cleared_text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)