import random

ROWS=6
COLS=7

def create_board():
    return [["0" for i in range(COLS)] for i in range(ROWS)]

def print_board(board):
    print('\n  0 1 2 3 4 5 6')
    print(" +" + "--"*COLS + "+")
    for row in board:
        print(" |" + " ".join(row) + "|")
    print(" +" + "--"*COLS + "+")

def is_valid_move(board, col):
    return board[0][col]=='0'

def get_next_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col]=='0':
            return r
    return None

def drop_piece(board, row, col, piece):
    board[row][col]=piece

def check_win(board, piece):
    for r in range(ROWS):
        for c in range(COLS-3):
            if all(board[r][c+i]==piece for i in range(4)):
                return True

    for c in range(COLS):
        for r in range(ROWS-3):
            if all(board[r+i][c]==piece for i in range(4)):
                return True

    for r in range(3, ROWS):
        for c in range(COLS-3):
            if all(board[r-i][c+i]==piece for i in range(4)):
                return True

    for r in range(ROWS-3):
        for c in range(COLS-3):
            if all(board[r+i][c+i]==piece for i in range(4)):
                return True

    return False

def get_valid_columns(board):
    return [c for c in range(COLS) if is_valid_move(board, c)]  


def ai_move(board):
    valid_cols = get_valid_columns(board)

    
    for col in valid_cols:
        temp_board=[row[:] for row in board]
        row=get_next_row(temp_board, col)
        drop_piece(temp_board, row, col, "B")
        if check_win(temp_board, "B"):
            return col

    
    for col in valid_cols:
        temp_board=[row[:] for row in board]
        row=get_next_row(temp_board, col)
        drop_piece(temp_board, row, col, "A")
        if check_win(temp_board, "A"):
            return col

    
    return random.choice(valid_cols)

def play_game():
    while True:
        board = create_board()
        print("Choose mode:")
        print("1 - Player vs Player")
        print("2 - Player vs AI")
        mode=input("> ")

        turn=random.randint(1, 2)
        game_over=False

        while not game_over:
            print_board(board)

            if turn%2==0:
                col=int(input("Player A, choose column (0-6): "))
                piece="A"
            else:
                if mode=="2":
                    col=ai_move(board)
                    print(f"AI chooses column {col}")
                else:
                    col=int(input("Player B, choose column (0-6): "))
                piece="B"

            if col<0 or col>=COLS or not is_valid_move(board, col):
                print("Invalid move. Try again.")
                continue

            row = get_next_row(board, col)
            drop_piece(board, row, col, piece)

            if check_win(board, piece):
                print_board(board)
                print(f'{piece} wins!')
                game_over=True
            elif len(get_valid_columns(board)) == 0:
                print_board(board)
                print('It\'s a tie!')
                game_over=True

            turn+=1
        
        start_over=input('Want to play again? (Y/N): ')
        if not start_over.lower().startswith('y'):
            break


play_game()