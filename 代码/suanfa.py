import random

def generate_sudoku():
    # 创建一个空的9x9的数独棋盘
    board = [[0] * 9 for _ in range(9)]

    # 使用回溯法填充数独棋盘
    solve_sudoku(board)

    return board

def solve_sudoku(board):
    # 寻找待填充的空格
    row, col = find_empty(board)

    # 如果没有找到空格，说明数独已填满，返回True
    if row is None:
        return True

    # 生成数字的随机顺序
    random_order = random.sample(range(1, 10), 9)

    # 尝试填充随机顺序的数字
    for num in random_order:
        if is_valid(board, row, col, num):
            # 如果当前数字合法，则填充到空格中
            board[row][col] = num

            # 递归调用解决下一个空格
            if solve_sudoku(board):
                return True

            # 如果下一个空格无法填充合法数字，则回溯
            board[row][col] = 0

    # 如果不能填充任何数字，则数独无解，返回False
    return False

# 寻找还未填的空
def find_empty(board):
    # 寻找空格
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None, None

# 检测填入是否合法
def is_valid(board, row, col, num):
    # 检查行是否合法
    for i in range(9):
        if board[row][i] == num:
            return False

    # 检查列是否合法
    for i in range(9):
        if board[i][col] == num:
            return False

    # 检查3x3的小方块是否合法
    start_row = row // 3 * 3
    start_col = col // 3 * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    # 如果通过上述检查，则数字合法
    return True

# 以指定难度生成一个数独谜题
def generate_puzzle(board, difficulty):

    # 根据难度确定要挖去的数字的数量
    if difficulty == 1:
        num_puzzle = random.randint(40, 45)
    elif difficulty == 2:
        num_puzzle = random.randint(46, 53)
    elif difficulty == 3:
        num_puzzle = random.randint(54, 59)

    puzzle = [[0] * 9 for _ in range(9)]

    # 复制数独棋盘到谜题盘
    for i in range(9):
        for j in range(9):
            puzzle[i][j] = board[i][j]

    # 随机挖去指定数量的数字
    count = 0
    while count < num_puzzle:
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        if puzzle[row][col] != 0:
            puzzle[row][col] = 0
            count += 1

    return puzzle

# 调用生成数独的函数
board = generate_sudoku()
hard = 1
puzzle = generate_puzzle(board,hard)

# 打印填满的数独
for i in range(9):
    for j in range(9):
        print(board[i][j], end=' ')
    print()
print("--------------")

# 打印挖空后的数独
for i in range(9):
    for j in range(9):
        print(puzzle[i][j], end=' ')
    print()