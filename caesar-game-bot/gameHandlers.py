from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

import dataBase as db
import keyboards as kb
import figures as fg
from createBot import bot
from createBot import Menu, Game, Caesar
from createBot import horizontalAxis
# Difficulty
async def callback_start(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, 'Выберите сложность. Для справки используйте команду /help.',
                           reply_markup=kb.difficultyKeyboard)
    await Game.difficulty.set()

async def callback_game(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    data = callback_query.data
    if data=='easy':
        figs = 1
        diff = "MS-DOS"
    elif data=='medium':
        figs = 2
        diff = "Хамелеон"
    elif data == 'hard':
        figs = 3
        diff = "Третья рука"

    startPos, direction, finalPos = fg.figureSteps(figs, 1)
    db.updateManyPersonal(callback_query.from_user.id, ['score', 'round', 'step', 'figures', 'startPos',
        'directions', 'positions'], [0, 1, 1, figs, str(startPos), str(direction), str(finalPos)])
    startText = ''
    for i in range(len(startPos)):
        startText += f'Фигура {i+1} находится на позиции {horizontalAxis[startPos[i][0]]}{startPos[i][1]+1}.\n'
    text = f'Выбрана сложность {diff}. Количество фигур: {figs}.\n{startText}Начинаем?'
    await bot.send_message(callback_query.from_user.id, text, reply_markup=kb.goKeyboard)
    await Game.step.set()

async def callback_step_again(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    figs = db.getOnePersonal(callback_query.from_user.id, 5)
    currentRound = db.getOnePersonal(callback_query.from_user.id, 3) + 1
    startPos, direction, finalPos = fg.figureSteps(figs, currentRound)
    db.updateManyPersonal(callback_query.from_user.id, ['round', 'step', 'figures', 'startPos',
        'directions', 'positions'], [currentRound, 1, figs, str(startPos), str(direction), str(finalPos)])
    startText = ''
    for i in range(len(startPos)):
        startText += f'Фигура {i+1} находится на позиции {horizontalAxis[startPos[i][0]]}{startPos[i][1]+1}.\n'
    text = f'Количество фигур: {figs}.\n{startText}Начинаем?'
    await bot.send_message(callback_query.from_user.id, text, reply_markup=kb.goKeyboard)
    await Game.step.set()

async def callback_step(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(callback_query.from_user.id, callback_query.message.message_id)
    stepData = db.getManyPersonal(callback_query.from_user.id)
    if stepData[4]<=stepData[3]:
        stepData[7] = db.getStringList(stepData[7])
        textFigures = ''
        for i in range(stepData[5]):
            textFigures += f'Фигура {i+1} ходит {fg.moveName[stepData[7][i][stepData[4]-1]]}.\n'
        text = f'Уровень {stepData[3]}, шаг {stepData[4]}.\n{textFigures}'
        await bot.send_message(callback_query.from_user.id, text, reply_markup=kb.nextKeyboard)
        db.updateOnePersonal(callback_query.from_user.id, 'step', stepData[4]+1)
    else:
        text = 'Все фигуры сделали свои ходы. Введите позиции, на' + \
        ' которых фигуры находятся в данный момент. (/help для помощи.)'
        await bot.send_message(callback_query.from_user.id, text)
        await Game.answer.set()

async def command_answer(message: types.Message, state: FSMContext):
    userAnswer = db.answerProcessing(message.text)
    rightAnswerList = db.getStringList(db.getOnePersonal(message.from_user.id, 8))
    rightAnswer = ''
    for i in rightAnswerList:
        rightAnswer += f'{horizontalAxis[i[0]]}{i[1]+1} '
    rightAnswer = rightAnswer[:-1]
    rightAnswer = rightAnswer.upper()
    stepData = db.getManyPersonal(message.from_user.id)
    if rightAnswer == userAnswer:
        worldRecord = db.getBestOfAll()[0]
        stepData[2] += stepData[3]*(stepData[5]**2)
        if stepData[2] > stepData[1]:
            stepData[1] = stepData[2]
            textRecord = "\nВы установили новый личный рекорд!"
        else: textRecord = ''
        if stepData[2] > worldRecord:
            db.updateBestOfAll(message.from_user.id, stepData[2], message.from_user.full_name)
            textRecord  = "\nВы установили новый мировой рекорд!"
        db.updateManyPersonal(message.from_user.id, ['record', 'score'], [stepData[1], stepData[2]])
        await message.answer(f'''Верно! Набрано очков: {stepData[2]}.{textRecord}
Продолжаем игру?''', reply_markup=kb.nextKeyboard)
        await Game.finish.set()
    else:
        await message.answer(f'''Не верно! Правильный ответ: {rightAnswer}. Твой ответ: {userAnswer}.
Ты проиграл. Очков набрано: {stepData[2]}. Попробуешь ещё раз?''', reply_markup=kb.restartKeyboard)
        await Game.finish.set()


def registerHandlersGame(dp : Dispatcher):
    dp.register_callback_query_handler(callback_start, lambda c: c.data == 'start', state=Menu.mainMenu)
    dp.register_callback_query_handler(callback_start, lambda c: c.data == 'again', state=Caesar.finish)
    dp.register_callback_query_handler(callback_start, lambda c: c.data == 'again', state=Game.finish)
    dp.register_callback_query_handler(callback_step, lambda c: c.data == 'go', state=Game.step)
    dp.register_callback_query_handler(callback_game, state=Game.difficulty)
    dp.register_callback_query_handler(callback_step_again, lambda c: c.data == 'go', state=Game.finish)
    dp.register_message_handler(command_answer, state=Game.answer)