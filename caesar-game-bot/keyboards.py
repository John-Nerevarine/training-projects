from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# MAIN MENU
buttonPlay = InlineKeyboardButton('Начать', callback_data='start')
buttonRules = InlineKeyboardButton('Правила', callback_data='rules')
buttonRecords = InlineKeyboardButton('Рекорды', callback_data='records')
mainKeyboard = InlineKeyboardMarkup()
mainKeyboard.add(buttonPlay, buttonRules, buttonRecords)

# COMMON
# Restart
buttonRestart = InlineKeyboardButton('Выйти в главное меню', callback_data='restart')
buttonDifficulty = InlineKeyboardButton('Начать снова', callback_data='again')
restartKeyboard = InlineKeyboardMarkup().add(buttonDifficulty)
restartKeyboard.add(buttonRestart)

# Back
buttonBack = InlineKeyboardButton('Назад', callback_data='back')
backKeyboard = InlineKeyboardMarkup().add(buttonBack)

# continue
buttonContinue = InlineKeyboardButton('Продолжить', callback_data='continue')
continueKeyboard = InlineKeyboardMarkup().add(buttonContinue)

# GAME
# Difficulty
buttonEasy = InlineKeyboardButton('MS-DOS (легко)', callback_data='easy')
buttonMedium = InlineKeyboardButton('Хамелеон (нормально)', callback_data='medium')
buttonHard = InlineKeyboardButton('Третья рука (сложно)', callback_data='hard')
buttonCaesar = InlineKeyboardButton('Цезарь (слишком)', callback_data='caesar')
difficultyKeyboard = InlineKeyboardMarkup()
difficultyKeyboard.add(buttonEasy)
difficultyKeyboard.add(buttonMedium)
difficultyKeyboard.add(buttonHard)
difficultyKeyboard.add(buttonCaesar)
difficultyKeyboard.add(buttonBack)

# let's go
buttonGo = InlineKeyboardButton('Погнали!', callback_data='go')
goKeyboard = InlineKeyboardMarkup().add(buttonGo)
goKeyboard.add(buttonRestart)

# next
buttonNext = InlineKeyboardButton('Далее', callback_data='go')
nextKeyboard = InlineKeyboardMarkup()
nextKeyboard.add(buttonNext)
nextKeyboard.add(buttonRestart)