from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

import dataBase as db
import keyboards as kb
from createBot import bot, Menu, rulesText
from config import CHESS_BOARD_ID

# Records
async def callback_records(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    bestOfAll = db.getBestOfAll()
    bestPersonal = db.getBestPersonal(callback_query.from_user.id)
    text =f'''На данный момент мировой рекорд принадлежит {('пользователю "' + bestOfAll[1] + '"') if bestOfAll[1]
    else 'неизвестному пользователю'} и составляет {bestOfAll[0]}.
Ваш личный рекорд {('составляет ' + str(bestPersonal) + '.') if bestPersonal else 'пока не установлен.'}''' 

    await bot.send_message(callback_query.from_user.id, text,
                           reply_markup=kb.backKeyboard)

    await Menu.records.set()

# Rules
async def callback_rules(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_photo(chat_id=callback_query.from_user.id, photo=CHESS_BOARD_ID)
    await bot.send_message(callback_query.from_user.id, rulesText,
                           reply_markup=kb.backKeyboard)
    await Menu.rules.set()

#Получение id фото
async def scan_message(msg: types.Message):
    document_id = msg.photo[0].file_id
    file_info = await bot.get_file(document_id)
    print(f'file_id: {file_info.file_id}')

def registerHandlersMainMenu(dp : Dispatcher):
    dp.register_callback_query_handler(callback_records, lambda c: c.data == 'records', state=Menu.mainMenu)
    dp.register_callback_query_handler(callback_rules, lambda c: c.data == 'rules', state=Menu.mainMenu)
    dp.register_message_handler(scan_message, content_types=['photo'], state='*')