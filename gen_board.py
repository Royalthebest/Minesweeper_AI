import random 
from math import sqrt
def gen(length, width, num):
    board = [[0]*length for i in range(width)]
    print(len(board), len(board[0]))
    cells = length * width
    mines = random.sample(range(1, cells+1), num)
    # print(mines)

    for i in mines:
        board[int((i-1)/length)][(i-1)%length] = -1


    for i in range(width):
        for j in range(length):
            if board[i][j] == -1:
                if i != 0 and j != 0 and board[i-1][j-1] != -1:
                    board[i-1][j-1] += 1
                if i != 0 and board[i-1][j] != -1:
                    board[i-1][j] += 1
                if i != 0 and j != length-1 and board[i-1][j+1] != -1:
                    board[i-1][j+1] += 1
                if j != 0 and board[i][j-1] != -1:
                    board[i][j-1] += 1
                if j != length-1 and board[i][j+1] != -1:
                    board[i][j+1] += 1
                if i != width-1 and j != 0 and board[i+1][j-1] != -1:
                    board[i+1][j-1] += 1
                if i != width-1 and board[i+1][j] != -1:
                    board[i+1][j] += 1
                if i != width-1 and j != length-1 and board[i+1][j+1] != -1:
                    board[i+1][j+1] += 1
                
    free_cells = []
    count = round(sqrt(cells))
    while count > 0:
        free_cell = random.randint(1, cells)
        free_cell -= 1
        if board[int(free_cell/length)][free_cell%length] != -1 and (int(free_cell/length),free_cell%length) not in free_cells:
            count -= 1
            # print(free_cell)
            free_cells.append((int(free_cell/length),free_cell%length ))

    return board, free_cells, mines


if __name__ == '__main__':
    gen(9, 9, 10)
