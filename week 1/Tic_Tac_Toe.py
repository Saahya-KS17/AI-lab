matrix = [['-' for _ in range(3)] for _ in range(3)]
players = ['X', 'O']

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

for move in range(9):
    for row in matrix:
        print(row)

    player = players[move % 2]
    print(f"Player {player}'s turn:")

    r, c = map(int, input("Enter row and column (0-2): ").split())

    if matrix[r][c] == '-':
        matrix[r][c] = player
    else:
        print("Cell already taken! Try again.")
        continue

    if check_winner(matrix, player):
        for row in matrix:
            print(row)
        print(f"Player {player} wins!")
        break
else:
    for row in matrix:
        print(row)
    print("It's a draw!")
