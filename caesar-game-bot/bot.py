#!venv/bin/python

#v1.00.00 by 01.02.2022 @John_Nerevarine

from aiogram.utils import executor
import systemHandlers, mainMenuHandlers, gameHandlers, caesarHandlers
import dataBase as db
from createBot import dp


def on_startup( ):
    db.sqlStart()

systemHandlers.registerHandlersSystem(dp)
mainMenuHandlers.registerHandlersMainMenu(dp)
caesarHandlers.registerHandlersCaesar(dp)
gameHandlers.registerHandlersGame(dp)



# STARTING
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup())
