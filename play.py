import gen_board
import itertools
import time
# define the board and number of mines
l, w, num = 30, 16, 99
KB = []
KB0 = []

# turn coordination to an integer
def coor2int(coor):
    return coor[0] * l + coor[1] + 1

# turn an integer to a coordination
def int2coor(i):
    i -= 1
    return int(i/l), i%l

#giving a coordination, it will retuen all its neighbors
def get_neighbors(i,j):
    ret = []
    if i != 0 and j != 0:
        ret.append(coor2int([i-1, j-1]))
    if i != 0:
        ret.append(coor2int([i-1, j]))
    if i != 0 and j != l-1:
        ret.append(coor2int([i-1, j+1]))
    if j != 0:
        ret.append(coor2int([i, j-1]))
    if j != l-1:
        ret.append(coor2int([i, j+1]))
    if i != w-1 and j != 0:
        ret.append(coor2int([i+1, j-1]))
    if i != w-1:
        ret.append(coor2int([i+1, j]))
    if i != w-1 and j != l-1:
        ret.append(coor2int([i+1, j+1]))
    return ret

# giving a list and a number n, it will return a list contains all 
# combination of n element inside the list.
def get_combinations(lst, n):

    combinations = list(itertools.combinations(lst, n))
    combinations = [list(c) for c in combinations]
    return combinations

# giving a list and a list of lists, it will check whether the list 
# whether any sublist of the first list is in the second one
def contains_any_sublist(lst, check_lst):
    for sublist in check_lst:
        if all(element in lst for element in sublist):
            return True
    return False

# giving 2 lists of length 2, it will return the new clause generate 
# by theese two
def matching(x,y):
    a = x[0]
    b = x[1]
    c = y[0]
    d = y[1]
    m, n = 0, 0
    if a == -c:
        m = b
        n = d
    elif a == -d:
        m = b
        n = c
    elif b == -c:
        m = a
        n = d
    elif b == -d:
        m = a
        n = c
    if m == n:
        return [m]
    elif m == -n:
        return [0]
    else:
        return [m,n]


board, safe_lists, mine_lists = gen_board.gen(l, w, num)
print(board, safe_lists, mine_lists)

# put the initial cells into KB
for i in safe_lists:
    KB.append([-coor2int(i)])

# run the loop until KB is empty or 50000 times
for i in range(50000):
    if len(KB) == 0:
        break
    print(len(KB), len(KB0))

    # take off the first element in KB
    kb = KB[0]
    KB.remove(kb)

    if len(kb) == 1:
        # if kb is a single-lateral clause, move it into KB0
        val = kb[0]
        if kb not in KB0:
            KB0.append(kb)
        i = 0
        # remove all clauses contains kb, and all element in clause
        # contains -kb
        while i < len(KB):
            if val in KB[i]:
                KB.pop(i)
                i-=1
            elif -val in KB[i]:
                tmp = KB[i]
                KB.pop(i)
                i-=1
                tmp.remove(-val)
                KB.append(tmp)
            i += 1
        
        # If the cell is safe, get the neighbors information
        if val < 0:
            x, y = int2coor(-val)
            neighbors = get_neighbors(x,y)
            m = len(neighbors)
            n = board[x][y]

            # no mine
            if n == 0:
                for i in neighbors:
                    if [-i] not in KB0 and [-i] not in KB:
                        KB.append([-i])
            # all mine
            elif n == m:
                for i in neighbors:
                    if [i] not in KB0 and [i] not in KB:
                        KB.append([i])
            # general case
            else:
                # put all clauses into KB if it no clause in KB is stricter than it
                comb = get_combinations(neighbors, m-n+1)
                for i in comb:
                    if not contains_any_sublist(i, KB) and not contains_any_sublist(i, KB0):
                        KB.append(i)

                for i in range(len(neighbors)):
                    neighbors[i] *= -1
                
                comb = get_combinations(neighbors, n+1)
                for i in comb:
                    if not contains_any_sublist(i, KB) and not contains_any_sublist(i, KB0):
                        KB.append(i)
    # non single-lateral clause
    else:
        discard = False
        # check this clause is needed or not
        if contains_any_sublist(kb, KB):
            continue
        for i in KB0:
            if i[0] in kb:
                discard = True
                break
            if -i[0] in kb:
                kb.remove(-i[0])
        if not discard:
            KB.append(kb)
        # If the length is 2, find all clauses with the length of 2, then generate new clauses
        if len(kb) == 2:
            for i in KB:
                if len(i) == 2:
                    clause = matching(kb, i)
                    if clause[0] != 0 and clause not in KB:
                        KB.append(clause)

# GUI code

import tkinter as tk

class MinesweeperGUI:
    def __init__(self, board, explored_cells):
        self.board = board
        self.explored_cells = explored_cells
        
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        
        self.block_size = 20  # size of each block in pixels
        self.width = len(self.board[0]) * self.block_size  # calculate width of window
        self.height = len(self.board) * self.block_size  # calculate height of window
        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()
        
        self.draw_board()

    def draw_board(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                x1, y1 = col * self.block_size, row * self.block_size
                x2, y2 = x1 + self.block_size, y1 + self.block_size
                value = self.board[row][col]
                if (row, col) not in self.explored_cells:
                    color = 'grey'
                elif value < 0:
                    color = 'Hotpink1'
                else:
                    color = 'lime green'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color)
                if value == -1:
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text='x', fill='black')
                else:
                    self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(value), fill='black')


    def run(self):
        self.root.mainloop()

explore = []

for i in KB0:
    if i[0] < 0:
        i[0] = -i[0]
    x, y = int2coor(i[0])
    explore.append((x,y))

gui = MinesweeperGUI(board, explore)
gui.run()

