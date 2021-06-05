from function import karmic_triggers
from sqlighter import SQLighter

db = SQLighter('db/database.db')

def clear_text(message_list):
    cleared_text = message_list
    for i in karmic_triggers.PUNCTUATIONS:
        text = cleared_text.split(i)
        cleared_text = text[0].replace(i, '')
    return cleared_text

async def plus_or_minus(message, cleared_text):
    if not db.user_exists(message.chat.id, message.from_user.id):
        db.add_user_in_chat(message.chat.id, message.from_user.id, message.chat.full_name, message.from_user.full_name, karmic_triggers.STANDART_KARMA)
        print('Add User DataBase')
    if not db.user_exists(message.chat.id, message.reply_to_message.from_user.id):
        db.add_user_in_chat(message.chat.id, message.reply_to_message.from_user.id, message.chat.full_name, message.reply_to_message.from_user.full_name, karmic_triggers.STANDART_KARMA)
        print('Add User DataBase')
    if karmic_triggers.PLUS == cleared_text:
        await has_plus_karma(message)
    elif karmic_triggers.PLUS == cleared_text[0]:
        await has_plus_karma(message, cleared_text[1:])
    elif cleared_text in karmic_triggers.PLUS_WORDS:
        await has_plus_karma(message)
    elif karmic_triggers.MINUS in cleared_text:
        await has_minus_karma(message)
    elif cleared_text in karmic_triggers.MINUS_WORDS:
        await has_minus_karma(message)
    else:
        print('Nit')
    
    
async def has_plus_karma(message, interger=0):
    if interger != 0:
        try:
            interger = int(interger)
            result = db.get_karma_user(message.chat.id, message.from_user.id)
            sqrt = formula_karma(result)
            if interger < sqrt:
                user_karma = db.get_karma_user(message.chat.id, message.reply_to_message.from_user.id)
                new_user_karma = user_karma + interger
                new_clear_user_karma = float('%.2f' % new_user_karma)
                db.update_user_karma(message.chat.id, message.reply_to_message.from_user.id, new_clear_user_karma)
                await message.reply(f'Вы увеличили карму <b>{message.reply_to_message.from_user.full_name}</b> до <b>{new_clear_user_karma}</b> (+{interger}.00)', parse_mode='html')
            else:
                await has_plus_karma(message)
        except:
            pass
    else:
        result = db.get_karma_user(message.chat.id, message.from_user.id)
        sqrt = formula_karma(result)
        user_karma = db.get_karma_user(message.chat.id, message.reply_to_message.from_user.id)
        new_user_karma = user_karma + sqrt
        new_clear_user_karma = float('%.2f' % new_user_karma)
        db.update_user_karma(message.chat.id, message.reply_to_message.from_user.id, new_clear_user_karma)
        await message.reply(f'Вы увеличили карму <b>{message.reply_to_message.from_user.full_name}</b> до <b>{new_clear_user_karma}</b> (+{sqrt})', parse_mode='html')

async def has_minus_karma(message, interger=0):
    if interger != 0:
        try:
            interger = int(interger)
            result = db.get_karma_user(message.chat.id, message.from_user.id)
            sqrt = formula_karma(result)
            if interger < sqrt:
                user_karma = db.get_karma_user(message.chat.id, message.reply_to_message.from_user.id)
                new_user_karma = user_karma - interger
                new_clear_user_karma = float('%.2f' % new_user_karma)
                db.update_user_karma(message.chat.id, message.reply_to_message.from_user.id, new_clear_user_karma)
                await message.reply(f'Вы уменьшили карму <b>{message.reply_to_message.from_user.full_name}</b> до <b>{new_clear_user_karma}</b> (-{interger}.00)', parse_mode='html')
            else:
                await has_minus_karma(message)
        except:
            pass
    else:
        result = db.get_karma_user(message.chat.id, message.from_user.id)
        sqrt = formula_karma(result)
        user_karma = db.get_karma_user(message.chat.id, message.reply_to_message.from_user.id)
        new_user_karma = user_karma - sqrt
        new_clear_user_karma = float('%.2f' % new_user_karma)
        db.update_user_karma(message.chat.id, message.reply_to_message.from_user.id, new_clear_user_karma)
        await message.reply(f'Вы уменьшили карму <b>{message.reply_to_message.from_user.full_name}</b> до <b>{new_clear_user_karma}</b> (-{sqrt})', parse_mode='html')

def formula_karma(karma):
    int_karma = karma ** (0.5)
    sqrt = float('%.2f' % int_karma)
    return sqrt
