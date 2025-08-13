import random
import math
import sys

def getNewBoard():
    board = []
    for x in range(60):
        board.append([])
        for y in range(15):
            if random.randint(0, 1) == 0:
                board[x].append('~')
            else:
                board[x].append('`')
    return board

def drawboard(board):
    labelLine = '    '
    for i in range(6):
        label = str(i * 10)
        if i == 0:
            spacing = ''  
        else:
            spacing = ' ' * (10 - len(label))  
        labelLine += spacing + label

    print('   ' + ('0123456789' * 6))
    print()

    for row in range(15):
        extraspace = ' ' if row < 10 else ''
        boardRow = ''
        for column in range(60):
            boardRow += board[column][row]
        print('%s%s %s %s' % (extraspace, row, boardRow, row))
    print()
    print('   ' + ('0123456789' * 6))
    print(labelLine)

def getRandomChest(num_chests):
    chests = []
    while len(chests) < num_chests:
        newchest = [random.randint(0, 59), random.randint(0, 14)]
        if newchest not in chests:
            chests.append(newchest)
    return chests

def isOnBoard(x, y):
    return 0 <= x <= 59 and 0 <= y <= 14

def makeMove(board, chests, x, y):
    smallestDistance = 100
    for cx, cy in chests:
        distance = math.sqrt((cx - x) * (cx - x) + (cy - y) * (cy - y))
        if distance < smallestDistance:
            smallestDistance = distance
    if smallestDistance == 0:
        chests.remove([x, y])
        board[x][y] = 'T'
        return 'You found a sunken treasure chest!'
    else:
        if smallestDistance < 10:
            board[x][y] = str(int(round(smallestDistance)))
            return 'Treasure chest detected at a distance of %s from the sonar.' % (int(round(smallestDistance)))
        else:
            board[x][y] = 'X'
            return 'Sonar did not detect anything. All chests out of range.'

def enterPlayerMove(previousMoves):
    print('Where do you want to drop the next sonar device? (0-59 0-14) (or type quit)')
    while True:
        move = input()
        if move.lower() == 'quit':
            print('Thanks for playing!')
            sys.exit()
        move = move.split()
        if len(move) == 2 and move[0].isdigit() and move[1].isdigit() and isOnBoard(int(move[0]), int(move[1])):
            if [int(move[0]), int(move[1])] in previousMoves:
                print('You already moved there.')
                continue
            return [int(move[0]), int(move[1])]
        print('Enter a number from 0 to 59, a space, and a number from 0 to 14.')

def showInstructions():
    print('''Welcome to Sonar Treasure Hunt! You are the captain of the Simon, a ship on a mission to locate three sunken treasure chests hidden in the\nocean. The map is a 60 by 15 grid representing the sea. You have 20 sonar devices to help you find them. Each turn, you drop a sonar device at a coordinate.\nIf a chest is within range (less than 10 units away), the sonar will tell you the distance to the nearest one. If it's farther than that, you'll get\nnothing. If the sonar reports a distance of 0, you've found a chest! Find all three chests before you run out of sonar devices. Good luck!''')

print('S O N A R')
print()
print('Would you like to see the instructions? yes or no')
if input().lower().startswith('y'):
    showInstructions()

while True:
    sonarDevices = 20
    theBoard = getNewBoard()
    theChests = getRandomChest(3)
    drawboard(theBoard)
    previousMoves = []

    while sonarDevices > 0:
        print('You have %s sonar device(s) left. %s treasure chest(s) remaining.' % (sonarDevices, len(theChests)))
        x, y = enterPlayerMove(previousMoves)
        previousMoves.append([x, y])
        moveResult = makeMove(theBoard, theChests, x, y)
        drawboard(theBoard)
        print(moveResult)

        if moveResult == 'You found a sunken treasure chest!':
            for x, y in previousMoves:
                makeMove(theBoard, theChests, x, y)

        if len(theChests) == 0:
            print('Good job! You found all the treasure chests!')
            break

        sonarDevices -= 1

    if sonarDevices == 0 and len(theChests) > 0:
        print('OOPS! You ran out of devices. Game over.')
        print()
        print('The remaining chests were at these coordinates:')
        for x, y in theChests:
            print('    %s %s' % (x, y))

    print('Wanna play again? yes or no')
    if not input().lower().startswith('y'):
        sys.exit()
