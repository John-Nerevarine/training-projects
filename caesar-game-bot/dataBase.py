import sqlite3 as sq

def sqlStart ():
    global base, cur
    base = sq.connect('mt.db')
    cur = base.cursor()
    if base:
        print('Data base connected.')
        base.execute('''CREATE TABLE IF NOT EXISTS best(
            id INTEGER NOT NULL,
            record INTEGER NOT NULL,
            userName TEXT,
            string_number INTEGER PRIMARY KEY)''')
        base.execute('''CREATE TABLE IF NOT EXISTS personal(
            id INTEGER NOT NULL,
            record INTEGER,
            score INTEGER,
            round INTEGER,
            step INTEGER,
            figures INTEGER,
            startPos TEXT,
            directions TEXT,
            positions TEXT )''')
    base.commit()

# Создание списка из строки, ранее полученной из списка
# Рекурсивная функция в оболочке.
def stringToIntList(string, i=0):
    tempString = ''
    retList = []
    while string[i] != ']':
        if string[i] == '[':
            i += 1
            tempList, i = stringToIntList(string, i)
            retList.append(tempList)
        elif string[i] == ',':
            if tempString != '':
                retList.append(int(tempString))
                tempString = ''
            i += 1
        elif string[i] == ' ':
            i += 1
            continue
        else:
            tempString += string[i]
            i += 1
    else:
        if tempString != '':
            retList.append(int(tempString))
        if i+1 < len(string):
            i += 1
        return retList, i
# Оболочка предыдущей функции
def getStringList(string):
    return stringToIntList(string)[0][0]

# Обработка ответа
def answerProcessing(answer):
    answer = answer.replace(',', ' ')
    answer = answer.replace(';', ' ')
    answer = answer.replace('.', ' ')
    answer = answer.replace('-', ' ')
    answer = list(answer)
    valueGot = False
    popIndexes = []
    for i in range(len(answer)):
        if answer[i] == ' ':
            if (not(valueGot) or (i+1 >= len(answer)) or (answer[i+1] == ' ')):
                popIndexes.append(i)
        else: valueGot = True
    for i in range(len(popIndexes)-1, -1, -1):
        answer.pop(popIndexes[i])
    answer = ''.join(answer)
    return answer.upper()


def addUser(userId):
    cur.execute('INSERT INTO personal VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', (userId,
        0, 0, 0, 0, 0, None, None, None))
    base.commit()

def isNew(searchingId):
    cur.execute('SELECT * FROM personal WHERE id LIKE '+str(searchingId))
    if (cur.fetchone()):
        return False
    else: return True

def getBestOfAll():
    cur.execute('SELECT * FROM best')
    return cur.fetchone()[1:]

def updateBestOfAll(userId, userRecord, name):
    values = (userId, userRecord, name)
    cur.execute('SELECT * FROM best')
    currentRecord =  cur.fetchone()
    if currentRecord:
        cur.execute('UPDATE best SET id = ?, record = ?, userName = ? WHERE string_number = 1', (values))
    else:
        cur.execute('INSERT INTO best VALUES(?, ?, ?, ?)', (userId, userRecord, name, 1))
    base.commit()


def getBestPersonal(userId):
    cur.execute('SELECT * FROM personal WHERE id LIKE '+str(userId))
    return cur.fetchone()[1]

def updateOnePersonal(userId, column, value):
    cur.execute('UPDATE personal SET ' + column + ' = ? WHERE id = ?', (value, userId))
    base.commit()

def updateManyPersonal(userId, columnList, valuesList):
    columnList = str([i+' = ?' for i in columnList])[2:-2]
    columnList = columnList.replace("'", "")
    valuesList.append(userId)
    valuesList = tuple(valuesList)
    cur.execute('UPDATE personal SET ' + columnList + ' WHERE id = ?', valuesList)
    base.commit()

#           0     1      2      3      4      5        6           7          8
#columns = id, record, score, round, step, figures, startPos, directions, positions
def getOnePersonal(userId, column):
    #params = tuple(userId,)
    cur.execute('SELECT * FROM personal WHERE id LIKE ?', (userId,))
    return cur.fetchone()[column]

def getManyPersonal(userId):
    cur.execute('SELECT * FROM personal WHERE id LIKE ?', (userId,))
    return list(cur.fetchone())