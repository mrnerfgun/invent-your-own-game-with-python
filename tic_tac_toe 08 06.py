# TicTacToe
import random

def drawBoard(board):
    def formatCell(i):
        return board[i] if board[i] != ' ' else str(i)

    print()
    print(formatCell(7) + '|' + formatCell(8) + '|' + formatCell(9))
    print('-+-+-')
    print(formatCell(4) + '|' + formatCell(5) + '|' + formatCell(6))
    print('-+-+-')
    print(formatCell(1) + '|' + formatCell(2) + '|' + formatCell(3))
    print()

def inputPlayerLetter():
    letter = ''
    while letter not in ['X', 'O']:
        print('Choose X or O: ')
        letter = input().upper()
    if letter == 'X':
        return ['X', 'O']
    else:
        return ['O', 'X']

def whoGoesFirst():
    return 'computer' if random.randint(0, 1) == 0 else 'player'

def makeMove(board, letter, move):
    board[move] = letter

def isWinner(bo, le):
    return ((bo[7] == le and bo[8] == le and bo[9] == le) or
            (bo[4] == le and bo[5] == le and bo[6] == le) or
            (bo[1] == le and bo[2] == le and bo[3] == le) or
            (bo[7] == le and bo[4] == le and bo[1] == le) or
            (bo[8] == le and bo[5] == le and bo[2] == le) or
            (bo[9] == le and bo[6] == le and bo[3] == le) or
            (bo[7] == le and bo[5] == le and bo[3] == le) or
            (bo[9] == le and bo[5] == le and bo[1] == le))

def getBoardCopy(board):
    return board[:]

def isSpaceFree(board, move):
    return board[move] == ' '

def getPlayerMove(board):
    move = ''
    while True:
        print('What is your next move? (1-9)')
        move = input()
        if move in '1 2 3 4 5 6 7 8 9'.split() and isSpaceFree(board, int(move)):
            return int(move)
        print("Invalid move. Try again.")

def chooseRandomMoveFromList(board, movesList):
    possibleMoves = [i for i in movesList if isSpaceFree(board, i)]
    if possibleMoves:
        return random.choice(possibleMoves)
    return None

def getComputerMove(board, computerLetter):
    if computerLetter == 'X':
        playerLetter = 'O'
    else:
        playerLetter = 'X'

    # First, check for a winning move
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, computerLetter, i)
            if isWinner(copy, computerLetter):
                return i

    # Block player's winning move
    for i in range(1, 10):
        copy = getBoardCopy(board)
        if isSpaceFree(copy, i):
            makeMove(copy, playerLetter, i)
            if isWinner(copy, playerLetter):
                return i

    # Try to take one of the corners
    move = chooseRandomMoveFromList(board, [1, 3, 7, 9])
    if move:
        return move

    # Take the center
    if isSpaceFree(board, 5):
        return 5

    # Move on one of the sides
    return chooseRandomMoveFromList(board, [2, 4, 6, 8])

def isBoardFull(board):
    for i in range(1, 10):
        if isSpaceFree(board, i):
            return False
    return True

# Game loop
print('Welcome to Tic-Tac-Toe!')

while True:
    theBoard = [' '] * 10
    playerLetter, computerLetter = inputPlayerLetter()
    print('Player is ' + playerLetter + ', Computer is ' + computerLetter)
    turn = whoGoesFirst()
    print('The ' + turn + ' will go first.')
    gameIsPlaying = True

    # Show initial board if player goes first
    if turn == 'player':
        drawBoard(theBoard)

    while gameIsPlaying:
        if turn == 'player':
            move = getPlayerMove(theBoard)
            makeMove(theBoard, playerLetter, move)
            drawBoard(theBoard)

            if isWinner(theBoard, playerLetter):
                print('You won!')
                gameIsPlaying = False
            elif isBoardFull(theBoard):
                print('It\'s a tie. GG!')
                break
            else:
                turn = 'computer'

        else:
            move = getComputerMove(theBoard, computerLetter)
            makeMove(theBoard, computerLetter, move)
            drawBoard(theBoard)

            if isWinner(theBoard, computerLetter):
                print('Glorious computer victory!')
                gameIsPlaying = False
            elif isBoardFull(theBoard):
                print('It\'s a tie. GG!')
                break
            else:
                turn = 'player'

    print('Wanna play again? (yes or no)')
    if not input().lower().startswith('y'):
        break
