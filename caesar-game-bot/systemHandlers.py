from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

import dataBase as db
import keyboards as kb
from createBot import bot
from createBot import Menu, Game, Caesar, System
from createBot import startFirstTime, startNotFirstTime, difficultyText, answerText

# Start
#@dp.message_handler(commands=['start'], state='*')
async def command_start(message: types.Message, state: FSMContext):
    if db.isNew(message.from_user.id):
        await bot.send_message(message.from_user.id, "Приветствую, "+ message.from_user.first_name +\
        '! ' + startFirstTime, reply_markup=kb.mainKeyboard)
        db.addUser(message.from_user.id)
        await state.finish()
        await Menu.mainMenu.set()
    else:
        await bot.send_message(message.from_user.id, "Приветствую, "+ message.from_user.first_name +\
        '! ' + startNotFirstTime, reply_markup=kb.mainKeyboard)
        await state.finish()
        await Menu.mainMenu.set()


# Back
async def callback_records_back(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, "Приветствую, "+ callback_query.from_user.first_name +\
    '! ' + startNotFirstTime, reply_markup=kb.mainKeyboard)
    await state.finish()
    await Menu.mainMenu.set()

# Restart
async def callback_restart(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    if db.isNew(callback_query.from_user.id):
        await bot.send_message(callback_query.from_user.id, "Приветствую, "+ callback_query.from_user.first_name +\
        '! ' + startFirstTime, reply_markup=kb.mainKeyboard)
        db.addUser(callback_query.from_user.id)
        await state.finish()
        await Menu.mainMenu.set()
    else:
        await bot.send_message(callback_query.from_user.id, "Приветствую, "+ callback_query.from_user.first_name +\
        '! ' + startNotFirstTime, reply_markup=kb.mainKeyboard)
        await state.finish()
        await Menu.mainMenu.set()

#help
#@dp.message_handler(commands=['help'], state='*')
async def command_help_difficulty(message: types.Message):
    await bot.send_message(message.from_user.id,
        '-=ПАУЗА=-\n\n' + difficultyText + '\n\n-=ПАУЗА=-', reply_markup=kb.continueKeyboard)
    await System.helpDiff.set()

async def callback_back_difficulty(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await Game.difficulty.set()

async def command_help_answer_game(message: types.Message):
    await bot.send_message(message.from_user.id,
        '-=ПАУЗА=-\n\n' + answerText + '\n\n-=ПАУЗА=-', reply_markup=kb.continueKeyboard)
    await System.helpAnswerGame.set()

async def command_help_answer_caesar(message: types.Message):
    await bot.send_message(message.from_user.id,
        '-=ПАУЗА=-\n\n' + answerText + '\n\n-=ПАУЗА=-', reply_markup=kb.continueKeyboard)
    await System.helpAnswerCaesar.set()

async def callback_backHelp_game(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await Game.answer.set()

async def callback_backHelp_caesar(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await Caesar.answer.set()

def registerHandlersSystem(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start'], state='*')
    dp.register_callback_query_handler(callback_records_back, lambda c: c.data == 'back', state=Menu.records)
    dp.register_callback_query_handler(callback_records_back, lambda c: c.data == 'back', state=Menu.rules)
    dp.register_callback_query_handler(callback_records_back, lambda c: c.data == 'back', state=Game.difficulty)
    dp.register_callback_query_handler(callback_restart, lambda c: c.data == 'restart', state='*')
    dp.register_callback_query_handler(callback_backHelp_game, lambda c: c.data == 'continue', state=System.helpAnswerGame)
    dp.register_callback_query_handler(callback_backHelp_caesar, lambda c: c.data == 'continue', state=System.helpAnswerCaesar)
    dp.register_callback_query_handler(callback_back_difficulty, lambda c: c.data == 'continue', state=System.helpDiff)
    dp.register_message_handler(command_help_difficulty, commands=['help'], state=Game.difficulty)
    dp.register_message_handler(command_help_answer_game, commands=['help'], state=Game.answer)
    dp.register_message_handler(command_help_answer_caesar, commands=['help'], state=Caesar.answer)

    #dp.register_callback_query_handler(process_callback_restart, lambda c: c.data == 'restart', state='*')
