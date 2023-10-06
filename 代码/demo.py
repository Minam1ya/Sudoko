import tkinter as tk
import random
import threading
from PIL import ImageTk, Image
import pygame



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

def find_empty(board):
    # 寻找空格
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None, None

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

def validate_input(new_value):
    if new_value == "" or (new_value.isdigit() and 1 <= int(new_value) <= 9):
        return True
    else:
        return False

def generate_puzzle(board, difficulty):
    # 以指定难度生成一个数独谜题
    # difficulty: 1 - 简单, 2 - 中等, 3 - 困难

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



# 数独游戏界面类
class SudokuGameGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("数独荣耀")

        # 设定页面大小以及出现位置
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        window_width = 720
        window_height = 720
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.window.geometry(f"{window_width}x{window_height}+{x}+{y-50}")

        # 第一个页面-游戏打开页面
        self.page1 = tk.Frame(self.window)
        self.page1.pack()

        # 页面添加背景
        page1 = tk.PhotoImage(file='./file/page1.png')
        self.label1 = tk.Label(self.page1,image=page1)
        self.label1.image = page1
        self.label1.grid(row=0,column=0,rowspan=6,columnspan=3)

        # 进入游戏按钮
        enter_img = tk.PhotoImage(file = './file/page1_1.png')
        self.enter_button = tk.Button(self.page1,image=enter_img, command=self.start)
        self.enter_button.image = enter_img
        self.enter_button.grid(row=5,column=1)

        # 第二个页面-游戏首页
        self.page2 = tk.Frame(self.window)

        # 页面添加背景
        page2 = tk.PhotoImage(file='./file/page2.png')
        self.label2 = tk.Label(self.page2,image=page2)
        self.label2.image = page2
        self.label2.grid(row=0,column=0,rowspan=8,columnspan=6)


        # 开始游戏按钮
        start_img = tk.PhotoImage(file = './file/page2_1.png')
        self.start_button = tk.Button(self.page2,image=start_img, command=self.show_page4)
        self.start_button.image = start_img
        self.start_button.grid(row=7,column=1)

        # 游戏攻略按钮
        tips_img = tk.PhotoImage(file = './file/page2_2.png')
        self.tips_button = tk.Button(self.page2,image=tips_img, command=self.show_page3)
        self.tips_button.image = tips_img
        self.tips_button.grid(row=7,column=2)

        # 退出游戏按钮
        quit_img = tk.PhotoImage(file = './file/page2_3.png')
        self.quit_button = tk.Button(self.page2,image=quit_img, command=self.window.quit)
        self.quit_button.image = quit_img
        self.quit_button.grid(row=7,column=3)

        # 第三个页面-游戏攻略页面
        self.page3 = tk.Frame(self.window)

        # 页面添加背景
        page3 = tk.PhotoImage(file='./file/page3.png')
        self.label3 = tk.Label(self.page3,image=page3)
        self.label3.image = page3
        self.label3.grid(row=0,column=0,rowspan=5,columnspan=4)

        # 返回按钮
        back_img = tk.PhotoImage(file = './file/page3_1.png')
        self.back_button = tk.Button(self.page3,image=back_img, command=self.show_page2)
        self.back_button.image = back_img
        self.back_button.grid(row=4,column=3)

        # 第四个页面 - 游戏难度选择页面
        self.page4 = tk.Frame(self.window)

        # 页面添加背景
        page4 = tk.PhotoImage(file='./file/page4.png')
        self.label4 = tk.Label(self.page4,image=page4)
        self.label4.image = page4
        self.label4.grid(row=0,column=0,rowspan=5,columnspan=8)

        # 简单按钮
        easy_img = tk.PhotoImage(file='./file/page4_1.png')
        easy_button = tk.Button(self.page4,image = easy_img , command=self.playgame1)
        easy_button.image = easy_img
        easy_button.grid(row=0,column=4)

       
        # 普通按钮
        normal_img = tk.PhotoImage(file='./file/page4_2.png')
        normal_button = tk.Button(self.page4,image = normal_img , command=self.playgame2)
        normal_button.image = normal_img
        normal_button.grid(row=1,column=4)

        # 困难按钮
        hard_img = tk.PhotoImage(file='./file/page4_3.png')
        hard_button = tk.Button(self.page4,image = hard_img , command=self.playgame3)
        hard_button.image = hard_img
        hard_button.grid(row=2,column=4)

        # 输入求解按钮
        back_img = tk.PhotoImage(file='./file/page4_4.png')
        self.back_button3 = tk.Button(self.page4,image = back_img, command=self.show_page8)
        self.back_button3.image = back_img
        self.back_button3.grid(row=3, column=4)
        
        # 退出游戏按钮
        quit2_img = tk.PhotoImage(file = './file/page4_5.png')
        self.quit2_button = tk.Button(self.page4,image=quit2_img, command=self.window.quit)
        self.quit2_button.image = quit2_img
        self.quit2_button.grid(row=4,column=4)

        # 第五个页面 - 游戏界面
        self.page5 = tk.Frame(self.window)
       
        # 添加背景
        page5 = tk.PhotoImage(file='./file/page4.png')
        self.label5 = tk.Label(self.page5,image=page4)
        self.label5.image = page5
        self.label5.grid(row=0,column=0,rowspan=5,columnspan=5)
        
        # 重新游玩按钮
        self.back_button3 = tk.Button(self.page5, text="重新游玩", command=self.show_page4)
        self.back_button3.grid(row= 3, column=0)

        #查看答案按钮
        self.back_button5 = tk.Button(self.page5, text="查看答案", command=self.show_page7)
        self.back_button5.grid(row= 3, column=1)

        #退出游戏按钮
        self.back_button4 = tk.Button(self.page5, text="退出游戏", command=self.show_page6)
        self.back_button4.grid(row= 3, column=2)

        # 第六个页面 - 退出游戏页面
        self.page6 = tk.Frame(self.window)

        # 添加背景
        page6 = tk.PhotoImage(file='./file/page6.png')
        self.label6 = tk.Label(self.page6,image=page6)
        self.label6.image = page6
        self.label6.grid(row=0,column=0,rowspan=5,columnspan=4)

        
        # 确定退出按钮
        quit6_img = tk.PhotoImage(file = './file/page6_2.png')
        self.quit6_button = tk.Button(self.page6,image=quit6_img, command=self.window.quit)
        self.quit6_button.image = quit6_img
        self.quit6_button.grid(row=4,column=1)
        

        # 返回游戏按钮
        back2_img = tk.PhotoImage(file = './file/page6_1.png')
        self.back2_button = tk.Button(self.page6,image=back2_img, command=self.show_page5)
        self.back2_button.image = back2_img
        self.back2_button.grid(row=4,column=3)

        # 第七个页面 - 答案界面
        self.page7 = tk.Frame(self.window)
       
        # 添加背景
        page7 = tk.PhotoImage(file='./file/page4.png')
        self.label7 = tk.Label(self.page7,image=page4)
        self.label7.image = page7
        self.label7.grid(row=0,column=0,rowspan=5,columnspan=5)
        
        #返回题目按钮
        self.back_button5 = tk.Button(self.page7, text="返回题目", command=self.show_page5)
        self.back_button5.grid(row= 3, column=1)

        # 第八个页面 - 输入数独界面
        self.page8 = tk.Frame(self.window)
       
        
        # 创建数独面板中的单元格
        global board 
        board= []
        for i in range(9):
            row = []
            for j in range(9):
                cell = tk.Entry(self.page8, width=2, font=("Arial", 36),relief='groove',validate="key")
                cell['validatecommand'] = (cell.register(validate_input), '%P')
                cell.grid(row=i, column=j, padx=2, pady=2)
                row.append(cell)
            board.append(row)


        self.enter_button = tk.Button(self.page8,text="进行求解", font=("Arial", 16),command=self.solution)
        self.enter_button.grid(row=9,column=5,columnspan=2)

        #返回前页按钮
        self.back_button5 = tk.Button(self.page8, text="返回前页", font=("Arial", 16),command=self.show_page4)
        self.back_button5.grid(row=9,column=1,columnspan=2)

        #第九个页面 - 求解界面
        self.page9 = tk.Frame(self.window)


        #重新输入按钮
        self.back_button6 = tk.Button(self.page9, text="重新输入", font=("Arial", 16),command=self.show_page8)
        self.back_button6.grid(row=9,column=3,columnspan=3)



    # 跳转到第二个页面
    def show_page2(self):
        self.page3.pack_forget()
        self.page2.pack()


    # 跳转到第三个页面
    def show_page3(self):
        self.page2.pack_forget()
        self.page3.pack()

    # 跳转到第四个页面
    def show_page4(self):
        self.page2.pack_forget()
        self.page5.pack_forget()
        self.page8.pack_forget()
        self.page4.pack()

    # 跳转到第五个页面
    def show_page5(self):
        self.page4.pack_forget()
        self.page6.pack_forget()
        self.page7.pack_forget()
        self.page5.pack()

    # 跳转到第六个界面
    def show_page6(self):
        self.page5.pack_forget()
        self.page6.pack()

    # 跳转到第七个界面
    def show_page7(self):
        self.page5.pack_forget()
        self.page7.pack()

    # 跳转到第八个界面
    def show_page8(self):
        self.page4.pack_forget()
        self.page9.pack_forget()
        self.page8.pack()

    # 开始游戏按钮，播放bgm同时跳转到第二页
    def start(self):
        pygame.init()
        pygame.mixer.music.load("./file/bgm.mp3")
        pygame.mixer.music.set_volume (0.1)
        pygame.mixer.music.play(-1)
        self.page1.pack_forget()
        self.page2.pack()
        
    # 游戏主函数
    def createTable(self,index,hard):
        # 生成棋盘
        board = generate_sudoku()
        # 在棋盘上挖空
        puzzle = generate_puzzle(board,hard)
        # 保存题目部分
        box = tk.Label(self.page5)
        box.grid(row=index // 3, column=index % 3,)
        for i in range(9):
            for j in range(9):
                if puzzle[i][j] != 0:
                    label = tk.Label(box, text=board[i][j], font=('Arial', 12), width=2, height=1,relief='groove',bg ='#FFB6C1')
                    label.grid(row=i, column=j)

                else:
                    entry = tk.Entry(box, justify='center', font=('Arial', 12), width=2,validate="key")
                    entry['validatecommand'] = (entry.register(validate_input), '%P')
                    entry.grid(row=i, column=j)
        # 保存答案部分
        box2 = tk.Label(self.page7)
        box2.grid(row=index // 3, column=index % 3,)
        for i in range(9):
            for j in range(9):
                    label = tk.Label(box2, text=board[i][j], font=('Arial', 12), width=2, height=1,relief='groove',bg ='#FFB6C1')
                    label.grid(row=i, column=j)

    # 求解函数
    def solution(self):
        # 处理数独求解的逻辑
        # 提取数独问题
        problem = []
        for i in range(9):
            row = []
            for j in range(9):
                value = board[i][j].get()
                if value.isdigit():
                    row.append(int(value))
                else:
                    row.append(0)
            problem.append(row)
        solve_sudoku(problem)
        for i in range(9):
            for j in range(9):
                    label = tk.Label(self.page9, text=problem[i][j], font=('Arial', 36), width=2, height=1,relief='groove',bg ='#FFB6C1')
                    label.grid(row=i, column=j)    
        self.page8.pack_forget()
        self.page9.pack()

    # 多线程生成九个数独
    # 难度一
    def playgame1(self):
        for index in range(9):
            p = threading.Thread(target=self.createTable(index,1))
            p.start()
        self.page4.pack_forget()
        self.page5.pack()
    
    # 难度二
    def playgame2(self):
        for index in range(9):
            p = threading.Thread(target=self.createTable(index,2))
            p.start()
        self.page4.pack_forget()
        self.page5.pack()

    #难度三
    def playgame3(self):
        for index in range(9):
            p = threading.Thread(target=self.createTable(index,3))
            p.start()
        self.page4.pack_forget()
        self.page5.pack()

    # 运行游戏
    def run_game(self):
        self.window.mainloop()



# 创建数独游戏界面对象并运行游戏
game_gui = SudokuGameGUI()
game_gui.run_game()