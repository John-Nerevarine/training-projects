# Импорты
from tkinter import *
from tkinter import ttk
from random import randint, choice
from time import sleep

# Переменные
back = '#012835'
fore = '#00C9CC'
inactive='#aaaaaa'
fontSize=14

record = [0,0]
wins = 0
loses = 0
level = 0
step = 0
currentMove = True
state = True
log = False
winsText = 'Побед: '
losesText = 'Поражений: '
winsText = 'Побед первого игрока: '
losesText = 'Побед второго игрока: '
diff = 7
dynamicOrder = True

playGame = False
enemyAI = True

# Функции
def AI():
    if step > 3:
        oneStep, x, y = oneStepWinCheck_AI()
        if oneStep and randint(1, 100) <= 50 + diff*5:
            step_AI(x, y)
            return
        oneStep, x, y = oneStepLoseCheck_AI()
        if oneStep and randint(1, 100) <= 70 + diff*3:
            step_AI(x, y)
            return
        
    chance = randint(1, 10)
    x, y = randomStep_AI()
    if (step == 1):
        if chance <= (diff * 0.6):
            s = [0, 2]
            x, y = choice(s), choice(s)
        elif (diff * 0.6) < chance <= diff:
            x = y = 1
            
    elif (step == 2):
        if dataImage[1][1] == 0:
            if chance <= diff:
                x = y = 1
        else:
            if chance <= diff: 
                s = [0, 2]
                x, y = choice(s), choice(s)
                
    elif (step == 3):
        if dataImage[1][1] == 1:
            if chance <= diff:
                if dataImage[0][0] == -1:
                    x = y = 2
                elif dataImage[0][2] == -1:
                    x, y = 2, 0
                elif dataImage[2][0] == -1:
                    x, y = 0, 2
                elif dataImage[2][2] == -1:
                    x = y = 0
        elif dataImage[1][1] == 0:
            if chance <= diff:
                x = y = 1
                
    elif (step == 4) and chance <= diff:
        if ((dataImage[0][0] == 1 and
        dataImage[1][1] == -1 and
        dataImage[2][2] == 1) or
        (dataImage[2][0] == 1 and
        dataImage[1][1] == -1 and
        dataImage[0][2] == 1)):
            s = [[0, 1], [1, 0], [1, 2], [2, 1]]
            x, y = choice(s)
    step_AI(x, y)

def randomStep_AI():
    freeCells = []
    for i in range(3):
        for j in range(3):
            if dataImage[i][j] == 0:
                freeCells.append([i, j])
    return choice(freeCells)
    
def oneStepWinCheck_AI():
    i = 0
    flag = True
    while flag and i < 3:
        if (dataImage[0][i] + dataImage[1][i] + dataImage[2][i]) == -2:
            flag = False
            return analyzeWinString_AI('-', i)
        i += 1
        
    i = 0
    while flag and i < 3:
        if (dataImage[i][0] + dataImage[i][1] + dataImage[i][2]) == -2:
            flag = False
            return analyzeWinString_AI('|', i)
        i += 1
        
    if flag and (dataImage[0][0] + dataImage[1][1] + dataImage[2][2]) == -2:
        flag = False
        return analyzeWinString_AI('\'', 0)
    
    if flag and (dataImage[0][2] + dataImage[1][1] + dataImage[2][0]) == -2:
        return analyzeWinString_AI('/', i)
    return (False, None, None)

def analyzeWinString_AI(direction, axis):
    i = 0
    if direction == '-':
        while dataImage[i][axis] == -1:
            i += 1
        else:
            return (True, i, axis)
    elif direction == '|':
        while dataImage[axis][i] == -1:
            i += 1
        else:
            return (True, axis, i)
    elif direction == '\'':
        while dataImage[i][i] == -1:
            i += 1
        else:
            return (True, i, i)
    else:
        while dataImage[0+i][2-i] == -1:
            i += 1
        else:
            return (True, 0+i, 2-i)

def oneStepLoseCheck_AI():
    i = 0
    flag = True
    while flag and i < 3:
        if (dataImage[0][i] + dataImage[1][i] + dataImage[2][i]) == 2:
            flag = False
            return analyzeLoseString_AI('-', i)
        i += 1
        
    i = 0
    while flag and i < 3:
        if (dataImage[i][0] + dataImage[i][1] + dataImage[i][2]) == 2:
            flag = False
            return analyzeLoseString_AI('|', i)
        i += 1
        
    if flag and (dataImage[0][0] + dataImage[1][1] + dataImage[2][2]) == 2:
        flag = False
        return analyzeLoseString_AI('\'', 0)
    
    if flag and (dataImage[0][2] + dataImage[1][1] + dataImage[2][0]) == 2:
        return analyzeLoseString_AI('/', i)
    return (False, None, None) 

def analyzeLoseString_AI(direction, axis):
    i = 0
    if direction == '-':
        while dataImage[i][axis] == 1:
            i += 1
        else:
            return (True, i, axis)
    elif direction == '|':
        while dataImage[axis][i] == 1:
            i += 1
        else:
            return (True, axis, i)
    elif direction == '\'':
        while dataImage[i][i] == 1:
            i += 1
        else:
            return (True, i, i)
    else:
        while dataImage[0+i][2-i] == 1:
            i += 1
        else:
            return (True, 0+i, 2-i)
    
def step_AI(x, y):
    global step, currentMove
    root.update()
    sleep(randint(1,2)//1)
    dataImage[x][y] = -1
    labelImage[x][y]['image'] = playerImage[1]
    logInsert(log, 'Ваш ход.')
    step += 1
    if endGameCheck(x, y):
        victory()
    elif fairCheck():
        fair()
    currentMove = True

def fairCheck():
    i = 0
    j = 0
    while i<3:
        if dataImage[i][j] == 0:
            return False
        else:
            i = i + ((j+1) // 3)
            j = (j+1) % 3
    return True

def endGameCheck(x, y):
    if x == y:
        m = dataImage[0][0]
        i = 1
        while (i < 3 and dataImage[i][i] == m):
            i += 1
        else:
            if i == 3:
                coloringVictory('\'', None)
                return True
        
    if (x + y) == 2:
        m = dataImage[0][2]
        i = 1
        while (i < 3 and dataImage[0+i][2-i] == m):
            i += 1
        else:
            if i == 3:
                coloringVictory('/', None)
                return True

    m = dataImage[0][y]
    i = 1
    while (i < 3 and dataImage[i][y] == m):
        i += 1
    else:
        if i == 3:
            coloringVictory('-', y)
            return True

    m = dataImage[x][0]
    i = 1
    while (i < 3 and dataImage[x][i] == m):
        i += 1
    else:
        if i == 3:
            coloringVictory('|', x)
            return True
                
    return False

def fair():
    global playGame, wins, loses, record
    playGame = False
    startButton['state']='normal'
    startButton['text']='Ещё раунд'
    startButton['bg']=fore
    logInsert(state, 'Ничья!')
    wins += 1
    loses += 1
    saveRecord()
    updateText()
    
def victory():
    global playGame, wins, loses, record
    playGame = False
    startButton['state']='normal'
    startButton['text']='Ещё раунд'
    startButton['bg']=fore
    if enemyAI:
        if currentMove:
            logInsert(state, 'Вы выиграли!')
            wins += 1
            saveRecord()
            updateText()
        else:
            logInsert(state, 'Вы проиграли!')
            loses += 1
            updateText()
    else:
        if currentMove:
            logInsert(state, 'Выиграл первый игрок!')
            wins += 1
        else:
            loses += 1
            logInsert(state,'Выиграл второй игрок!')
    updateText()

def coloringVictory(direction, axis):
    if direction == '\'':
        for i in range(3):
            labelImage[i][i]['bg'] = fore
    elif direction == '/':
        for i in range(3):
            labelImage[0+i][2-i]['bg'] = fore
    elif direction == '-':
        for i in range(3):
            labelImage[i][axis]['bg'] = fore
    else:
        for i in range(3):
            labelImage[axis][i]['bg'] = fore

def move(x, y):
    global currentMove, step
    
    if playGame:
        if enemyAI:
            if currentMove:
                if dataImage[x][y] == 0:
                    dataImage[x][y] = 1
                    labelImage[x][y]['image'] = playerImage[0]
                    if endGameCheck(x, y):
                        victory()
                    elif fairCheck():
                        fair()
                    else:
                        currentMove = False
                        logInsert(log, 'Ход компьютера.')
                        step += 1
                        AI()
                elif dataImage[x][x] == 1:
                    logInsert(log, 'Это ваша фигура.')
                else:
                    logInsert(log, 'Это фигура компьютера.')
            else:
                logInsert(log, 'Ход компьютера.')
        else:
            if dataImage[x][y] == 0:
                if currentMove:
                    dataImage[x][y] = 1
                    labelImage[x][y]['image'] = playerImage[0]
                    if endGameCheck(x, y):
                        victory()
                    elif fairCheck():
                        fair()
                    else:
                        currentMove = False
                        logInsert(log, 'Ход второго игрока.')
                else:
                    dataImage[x][y] = 2
                    labelImage[x][y]['image'] = playerImage[1]
                    if endGameCheck(x, y):
                        victory()
                    elif fairCheck():
                        fair()
                    else:
                        currentMove = True
                        logInsert(log, 'Ход первого игрока.')
            elif dataImage[x][y] == 1:
                logInsert(log, 'Это фигура первого игрока.')
            else:
                logInsert(log, 'Это фигура второго игрока.')
    else:
        logInsert(log, 'Нажмите "Старт".')

def startGame():
    global playGame, enemyAI, currentMove, level, step, dynamicOrder, diff

    step = 1
    playGame = True
    enemyAI = True if enemy.get() == 'Компьютер' else False
    
    # распределение фигур и цветов
    if player1Shape.get() == 'Крестик':
        if player1Color.get() == 'Жёлтый':
            playerImage[0] = images[0][0]
        else:
            playerImage[0] = images[0][1]
            
        if player2Color.get() == 'Жёлтый':
            playerImage[1] = images[1][0]
        else:
            playerImage[1] = images[1][1]
    else:
        if player1Color.get() == 'Жёлтый':
            playerImage[0] = images[1][0]
        else:
            playerImage[0] = images[1][1]
            
        if player2Color.get() == 'Жёлтый':
            playerImage[1] = images[0][0]
        else:
            playerImage[1] = images[0][1]
            
                        

    # deactivation settings
    enemyLabel['fg'] = inactive
    moveOrderLabel['fg'] = inactive
    diffLabel['fg'] = inactive
    colorLabel01['fg'] = inactive
    colorLabel02['fg'] = inactive
    shapeLabel01['fg'] = inactive
    shapeLabel02['fg'] = inactive
    enemyBox['state'] = 'disabled'
    moveOrderBox['state'] = 'disabled'
    difficultyBox['state'] = 'disabled'
    player1ColorBox['state'] = 'disabled'
    player2ColorBox['state'] = 'disabled'
    player1ShapeBox['state'] = 'disabled'
    player2ShapeBox['state'] = 'disabled'
    startButton['state']='disable'
    startButton['bg'] = inactive
    resetButton['state']='normal'
    resetButton['bg'] = fore 

    for i in range(3):
        for j in range(3):
            labelImage[i][j]['image'] = images[2]
            labelImage[i][j]['bg'] = back
            dataImage[i][j] = 0

    logInsert(state, 'Раунд '+str(level := level+1))

    updateText()
    
    # очередность хода и сложность
    if enemyAI:
        diff = difficulty.get()
        winsText = 'Побед: '
        losesText = 'Поражений: '
        recordLabel['fg'] = fore
        if moveOrder.get() == 'Первым' :
            currentMove = True
            logInsert(log, 'Ваш ход.')
        elif moveOrder.get() == 'Вторым':
            currentMove = False
            logInsert(log, 'Ход компьютера.')
            AI()
        else:
            if dynamicOrder:
                dynamicOrder = False
                currentMove = True
                logInsert(log, 'Ваш ход.')
            else:
                dynamicOrder = True
                currentMove = False
                logInsert(log, 'Ход компьютера.')
                AI()
            
    else:
        winsText = 'Побед первого игрока: '
        losesText = 'Побед второго игрока: '
        recordLabel['fg'] = inactive
        currentMove = True
        logInsert(log, 'Ходит первый игрок.')
        
def resetGame():
    global playGame, wins, loses, dynamicOrder
    playGame = False
    dynamicOrder = True

    wins = 0
    loses = 0
    updateText()
    
    for i in range(3):
        for j in range(3):
            labelImage[i][j]["image"] = images[i%2][(i+j)%2]
            labelImage[i][j]["bg"] = back

    # activation settings
    enemyLabel['fg'] = fore
    moveOrderLabel['fg'] = fore
    diffLabel['fg'] = fore
    colorLabel01['fg'] = fore
    colorLabel02['fg'] = fore
    shapeLabel01['fg'] = fore
    shapeLabel02['fg'] = fore
    enemyBox['state'] = 'readonly'
    moveOrderBox['state'] = 'readonly'
    difficultyBox['state'] = 'readonly'
    player1ColorBox['state'] = 'readonly'
    player2ColorBox['state'] = 'readonly'
    player1ShapeBox['state'] = 'readonly'
    player2ShapeBox['state'] = 'readonly'
    startButton['state']='normal'
    startButton['bg'] = fore
    startButton['text']='Старт'
    resetButton['state']='disabled'
    resetButton['bg'] = inactive

    logInsert(log, 'Игра сброшена.')
    logInsert(state, 'Главное меню')

def getRecord():
    m = []
    try:
        f = open('record.dat', 'r', encoding='utf-8')
        for line in f.readlines():
            m.append(int(line))
        f.close()
        updateText()
        return m
    except:
        logInsert(log, 'Ошибка чтения рекорда.')
        return [0,0]
        
def saveRecord():
    global record
    
    if ((wins - loses) > (record[0] - record[1])):
        record[0], record[1] = wins, loses
        updateText()
        logInsert(log, 'Установлен новый рекорд!')
        try:
            f = open('record.dat', 'w', encoding='utf-8')
            f.write(str(record[0]) +'\n')
            f.write(str(record[1]))
            f.close
        except:
            logInsert(log, 'Ошибка записи рекорда!')
     
def updateText():
    win1Label['text'] = f'{winsText}{wins}'
    win2Label['text'] = f'{losesText}{loses}'
    recordLabel['text'] = f'Рекордная серия: {record[0]}/{record[1]}'

# Меню - True, остальное False
def logInsert(action, text):
    logPanel['state'] = 'normal'
    if action:
        l = len(text)
        if (l % 2 == 1):
            text = '-'*((33-l)//2) + text + '-'*((33-l)//2) + '\n'
            logPanel.insert(INSERT, text)
            logPanel.see(END)
        else:
            text =  '-'*((32-l)//2) + text + '-'*((32-l)//2) + '-' + '\n'
            logPanel.insert(INSERT, text)
            logPanel.see(END)
    else:
        logPanel.insert(INSERT, text+'\n')
        logPanel.see(END)
    logPanel['state'] = 'disabled'

def deactMoveOrderLabel(event):
    if enemy.get() == 'Человек':
        moveOrderLabel['fg'] = inactive
        diffLabel['fg'] = inactive
        difficultyBox['state'] = 'disable'
        moveOrderBox['state'] = 'disable'
    else:
        moveOrderLabel['fg'] = fore
        diffLabel['fg'] = fore
        moveOrderBox['state'] = 'readonly'
        difficultyBox['state'] = 'readonly'

def shapeChange(box):
    if box == 0:
        if player1Shape.get() == 'Крестик':
            player2ShapeBox.current(1)
        else:
            player2ShapeBox.current(0)
    else:
        if player2Shape.get() == 'Крестик':
            player1ShapeBox.current(1)
        else:
            player1ShapeBox.current(0)


root = Tk()
root.resizable(False, False)
root.title("Tic-tac toe")
root.iconbitmap("ttt_icon.ico")


WIDTH = 900
HEIGHT = 600
POS_X = root.winfo_screenwidth() // 2 - WIDTH // 2
POS_Y = root.winfo_screenheight() // 2 - HEIGHT // 2 - 20
root.geometry(f"{WIDTH}x{HEIGHT}+{POS_X}+{POS_Y}")
root["bg"] = back

bg_image = PhotoImage(file="bg_image.png")
backgroundLabel = Label(root, bg = back, bd = 0, image=bg_image)
backgroundLabel.place(x=0, y=0)

images = [[PhotoImage(file="y_cross.png"),
           PhotoImage(file="p_cross.png")],
          [PhotoImage(file="y_round.png"),
           PhotoImage(file="p_round.png")],
          PhotoImage(file="empty.png")
          ]

playerImage = [images[1][1], images[0][0]]

dataImage = []
labelImage = []

for i in range(3):
    dataImage.append([])
    labelImage.append([])
    for j in range(3):
        dataImage[i].append(0)
        dataImage[i][j] = 0
        labelImage[i].append(Label(root, bg = back, bd = 0))
        labelImage[i][j].place(x=i*194+i*9, y=j*194 + j*9)
        labelImage[i][j].bind("<Button-1>", lambda e, x=i, y=j: move(x, y))
        labelImage[i][j]["image"] = images[i%2][(i+j)%2]

# Текстовые метки
enemyLabel = Label(root, text='Противник:', bg=back, fg=fore,
      font=('Garamond', fontSize))
enemyLabel.place(x=610, y=10)

moveOrderLabel = Label(root, text='Ходить:', bg=back, fg=fore,
      font=('Garamond', fontSize))
moveOrderLabel.place(x=610, y=40)

diffLabel = Label(root, text='Сложность:', bg=back, fg=fore,
      font=('Garamond', fontSize))
diffLabel.place(x=610, y=70)

colorLabel01 = Label(root, text='Цвет игрока 1:', bg=back, fg=fore,
      font=('Garamond', fontSize))
colorLabel01.place(x=610, y=100)

colorLabel02 = Label(root, text='Цвет игрока 2:', bg=back, fg=fore,
      font=('Garamond', fontSize))
colorLabel02.place(x=610, y=130)

shapeLabel01 = Label(root, text='Фигура игрока 1:', bg=back, fg=fore,
      font=('Garamond', fontSize))
shapeLabel01.place(x=610, y=160)

shapeLabel02 = Label(root, text='Фигура игрока 2:', bg=back, fg=fore,
      font=('Garamond', fontSize))
shapeLabel02.place(x=610, y=190)

# Настройки
enemy = StringVar()
enemyBox = ttk.Combobox(root, width = 13, state='readonly',
           textvariable = enemy, values = ['Компьютер', 'Человек'],
           font=('Garamond', fontSize-1))
enemyBox.place(x=762, y=10)
enemyBox.current(0)
enemyBox.bind("<<ComboboxSelected>>", deactMoveOrderLabel)

moveOrder = StringVar()
moveOrderBox = ttk.Combobox(root, width = 13, state='readonly',
                  textvariable = moveOrder, values = ['Первым',
                                                      'Вторым', 'По очереди'],
                  font=('Garamond', fontSize-1))
moveOrderBox.place(x=762, y=40)
moveOrderBox.current(2)

difficulty = IntVar()
difficultyBox = ttk.Combobox(root, width = 13, state='readonly',
                  textvariable = difficulty, values = [1, 2, 3, 4, 5, 6,
                                                      7, 8, 9, 10],
                  font=('Garamond', fontSize-1))
difficultyBox.place(x=762, y=70)
difficultyBox.current(6)


player1Color = StringVar()
player1ColorBox = ttk.Combobox(root, width = 13, state='readonly',
                  textvariable = player1Color, values = ['Жёлтый', 'Розовый'],
                  font=('Garamond', fontSize-1))
player1ColorBox.place(x=762, y=100)
player1ColorBox.current(0)

player2Color = StringVar()
player2ColorBox = ttk.Combobox(root, width = 13, state='readonly',
                  textvariable = player2Color, values = ['Жёлтый', 'Розовый'],
                  font=('Garamond', fontSize-1))
player2ColorBox.place(x=762, y=130)
player2ColorBox.current(1)

player1Shape = StringVar()
player1ShapeBox = ttk.Combobox(root, width = 13, state='readonly',
                  textvariable = player1Shape, values = ['Крестик', 'Нолик'],
                  font=('Garamond', fontSize-1))
player1ShapeBox.place(x=762, y=160)
player1ShapeBox.current(0)
player1ShapeBox.bind("<<ComboboxSelected>>", lambda e: shapeChange(0))

player2Shape = StringVar()
player2ShapeBox = ttk.Combobox(root, width = 13, state='readonly',
                  textvariable = player2Shape, values = ['Крестик', 'Нолик'],
                  font=('Garamond', fontSize-1))
player2ShapeBox.place(x=762, y=190)
player2ShapeBox.current(1)
player2ShapeBox.bind("<<ComboboxSelected>>", lambda e: shapeChange(1))

# кнопки
startButton = Button(root, text = 'Старт', font=('Garamond', fontSize),
                     bg =fore, width = 27)
startButton.place(x=610, y=230)
startButton['command']=startGame

resetButton = Button(root, text = 'Сброс', font=('Garamond', fontSize),
                     bg = inactive, width = 27, state='disabled')
resetButton.place(x=610, y=270)
resetButton['command']=resetGame

# очки
win1Label = Label(root, text='Побед: 0', bg=back, fg=fore,
      font=('Garamond', fontSize))
win1Label.place(x=610, y = 310)

win2Label = Label(root, text='Поражений: 0', bg=back, fg=fore,
      font=('Garamond', fontSize))
win2Label.place(x=610, y = 330)

recordLabel = Label(root, text='Рекордная серия: 0/0', bg=back, fg=fore,
      font=('Garamond', fontSize))
recordLabel.place(x=610, y=350)

# панель состояния
logPanel = Text(width=33, height=13, wrap=WORD, state='disabled',
                fg=fore, bg=back)
logPanel.place(x=613, y=378)

scroll = Scrollbar(command=logPanel.yview, width=20)
scroll.place(x=880, y=378, height=212)
logPanel["yscrollcommand"] = scroll.set

# Меню - True, остальное False
record = getRecord()
logInsert(state, 'Главное меню')
getRecord()

root.mainloop()
