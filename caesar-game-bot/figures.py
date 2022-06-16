from random import randint, choices

horizontalAxis = ["A", "B", "C", "D", "E", "F", "G", "H"]
moveName = ["вверх", "вправо", "вниз", "влево"]

def figureSteps(figure=1, rounds=1):
    position = []
    direction = []
    startPosition = []
    for i in range(figure):
        position.append([randint(0, 7), randint(0, 7)])
        startPosition.append(position[i].copy())
        direction.append([])

    for i in range(rounds):
        for j in range(figure):
            possibleMove = [0, 1, 2, 3]
            if (position[j][0] == 0):
                possibleMove.remove(3)
            if (position[j][0] == 7):
                possibleMove.remove(1)
            if (position[j][1] == 0):
                possibleMove.remove(2)
            if (position[j][1] == 7):
                possibleMove.remove(0)

            move = choices(possibleMove)[0]

            direction[j].append(move)
            if move == 0:
                position[j][1] += 1    
            elif move == 1:
                position[j][0] += 1
            elif move == 2:
                position[j][1] -= 1
            else:
                position[j][0] -= 1


    return startPosition, direction, position