import random

matrix = [['-' for _ in range(3)] for _ in range(3)]

# Ask the human player to choose 'X' or 'O'
while True:
    human_choice = input("Choose your player: 'X' or 'O'? ").upper()
    if human_choice in ['X', 'O']:
        break
    else:
        print("Invalid choice. Please enter 'X' or 'O'.")

if human_choice == 'X':
    players = ['X', 'O'] # Human is 'X', Computer is 'O'
else:
    players = ['O', 'X'] # Human is 'O', Computer is 'X'


def check_winner(board, player):
    for row in board:
        if all(cell == player for cell in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_board_full(board):
    for row in board:
        if '-' in row:
            return False
    return True

def get_computer_move(board):
    # Simple AI: choose a random empty cell
    empty_cells = [(r, c) for r in range(3) for c in range(3) if board[r][c] == '-']
    if empty_cells:
        return random.choice(empty_cells)
    return None # Should not happen if is_board_full is checked

for move in range(9):
    for row in matrix:
        print(row)

    player = players[move % 2]
    print(f"Player {player}'s turn:")

    if player == human_choice: # Human player
        while True:
            try:
                r, c = map(int, input("Enter row and column (0-2): ").split())
                if 0 <= r < 3 and 0 <= c < 3:
                    if matrix[r][c] == '-':
                        matrix[r][c] = player
                        break
                    else:
                        print("Cell already taken! Try again.")
                else:
                    print("Invalid input. Row and column must be between 0 and 2.")
            except ValueError:
                print("Invalid input. Please enter two numbers separated by a space.")
    else: # Computer player
        print("Computer is making a move...")
        r, c = get_computer_move(matrix)
        if r is not None:
            matrix[r][c] = player


    if check_winner(matrix, player):
        for row in matrix:
            print(row)
        print(f"Player {player} wins!")
        break

    if is_board_full(matrix):
        for row in matrix:
            print(row)
        print("It's a draw!")
        break
