from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup
from sqlighter import SQLighter

db = SQLighter('db/database.db')

async def what_user(bot, callback_query, group_id):
    results = db.get_info_group(group_id)
    inline_kb_full = InlineKeyboardMarkup(row_width=2)
    ins = []
    for i in results:
        inline_temp = InlineKeyboardButton(i[3], callback_data=f"{i[2]}|users")
        inline_kb_full.add()
        ins.append(inline_temp)
        if len(ins) == 2:
            inline_kb_full.row(*ins)
            ins = []
    inline_kb_full.row(*ins)
    await bot.send_message(callback_query.from_user.id, f"Вот все учасники: ", reply_markup=inline_kb_full)