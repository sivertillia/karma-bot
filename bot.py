from aiogram.dispatcher import FSMContext
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from function import karmic_triggers, karmic_admin

import config
import logging

from fsm import DataInput, AdminInput
from sqlighter import SQLighter
from function import karmic_func

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
db = SQLighter('db/database.db')


@dp.message_handler(commands=['top'])
async def top(message: types.Message):
    if message.chat.type in ('group', 'supergroup'):
        result = db.get_info_group(message.chat.id)
        results = sorted(result, key=lambda student: student[-1], reverse=True)
        num = 0
        msg = 'Список самых почётных пользователей чата:\n'
        for i in results:
            num += 1
            msg += f'{num}. {i[3]} <b>{i[-1]}</b>\n'
        await message.answer(msg, parse_mode='html')

@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if (message.chat.type in ('private')) and (message.from_user.id in (855796186, 1101905490)):
        # await AdminInput.state_group.set()
        groups = db.get_group()
        inline_kb_full = InlineKeyboardMarkup(row_width=2)
        ins = []
        for i in groups:
            inline_temp = InlineKeyboardButton(i[2], callback_data=f"{i[1]}|groups")
            inline_kb_full.add()
            ins.append(inline_temp)
            if len(ins) == 2:
                inline_kb_full.row(*ins)
                ins = []
        inline_kb_full.row(*ins)
        await message.answer(f"Вот все группы в которых состоит бот", reply_markup=inline_kb_full)

@dp.message_handler(commands=['save-all'], state="*")
async def save(message: types.Message, state: FSMContext):
    db.save()
    await state.finish()
    await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler()
async def karma_trrigers(message: types.Message):
    if message.chat.type in ('group', 'supergroup'):
        if (not message.reply_to_message == None) and (not message.reply_to_message.from_user.is_bot) and (message.reply_to_message.from_user.id != message.from_user.id):
            if not db.user_exists(message.chat.id, message.from_user.id):
                db.add_user_in_chat(message.chat.id, message.from_user.id, message.from_user.full_name, karmic_triggers.STANDART_KARMA)
                print('Add User DataBase')
            if not db.user_exists(message.chat.id, message.reply_to_message.from_user.id):
                db.add_user_in_chat(message.chat.id, message.reply_to_message.from_user.id, message.reply_to_message.from_user.full_name, karmic_triggers.STANDART_KARMA)
                print('Add ReplyUser DataBase')
            if not db.group_exists(message.chat.id):
                db.add_group(message.chat.id, message.chat.full_name)
                print('Add Group DataBase')
            message_list = message.text.split(' ')
            cleared_text = karmic_func.clear_text(message_list[0])
            await karmic_func.plus_or_minus(message, cleared_text)

"""Callbacks"""

@dp.callback_query_handler()
async def send_random_value(callback_query: types.CallbackQuery, state: FSMContext):
    # state = Dispatcher.get_current().current_state()
    message_list = callback_query.data.split('|')
    if message_list[1] == 'groups':
        await bot.send_message(callback_query.from_user.id, f"Хорошо вы вибрали {message_list[0]}")
        await karmic_admin.what_user(bot, callback_query, message_list[0])
        await state.update_data(group_id=message_list[0])
    if message_list[1] == 'users':
        await bot.send_message(callback_query.from_user.id, f"Хорошо вы вибрали {message_list[0]}")
        await state.update_data(user_id=message_list[0])
        await AdminInput.state_settings.set()
        await bot.send_message(callback_query.from_user.id, f"Введите настройку:\nKarma 50")

"""FSM"""
@dp.message_handler(state=AdminInput.state_settings)
async def admin_setting(message: types.Message, state: FSMContext):
    message_list = message.text.split(' ')
    user_info = await state.get_data()
    if message_list[0].lower() == 'karma':
        try:
            karma = int(message_list[1])
            db.update_user_karma(user_info['group_id'], user_info['user_id'], karma)
        except:
            pass
    


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)