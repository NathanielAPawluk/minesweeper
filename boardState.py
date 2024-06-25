import random

xmap = [-1, 0, 1, 1, 1, 0, -1, -1]
ymap = [1, 1, 1, 0, -1, -1, -1, 0]

MINES = 40

def buildBoard(sx, sy):
    board = [["" for _ in range(12)] for _ in range(16)]
    board[sx][sy] = 0
    noMineCords = []
    for a, b in zip(xmap, ymap):
        if sx + a >= 0 and sx + a < 12 and sy + b >= 0 and sy + b < 16:
            noMineCords.append((sx + a, sy + b))
    
    random.seed()
    for _ in range(MINES):
        while True:
            x = random.randint(0, 15)
            y = random.randint(0, 11)
            if board[x][y] == "" and (x, y) not in noMineCords:
                board[x][y] = -1
                break
    for i in range(16):
        for j in range(12):
            if board[i][j] != -1:
                adj = 0
                for a, b in zip(xmap, ymap):
                    if i+a >= 0 and i+a < 16 and j+b >= 0 and j+b < 12:
                        if board[i+a][j+b] == -1:
                            adj += 1
                board[i][j] = adj
    return board

def openAdj(squares, sx, sy):
    squares[sx][sy].open()
    for xoff, yoff in zip(xmap, ymap):
        x, y = sx + xoff, sy + yoff
        if x < 16 and x >= 0 and y < 12 and y >= 0:
            if squares[x][y].opened != True and squares[x][y].flagged != True:
                squares[x][y].open()
                if squares[x][y].value == 0:
                    squares = openAdj(squares, x, y)
                elif squares[x][y].value == -1:
                    squares[x][y].lost()
                    return squares
    return squares

def chord(squares, x, y):
    flags = 0
    sqs = 0
    for a, b in zip(xmap, ymap):
        nx, ny = x + a, y + b
        if nx >= 0 and nx < 16 and ny >= 0 and ny < 12:
            if squares[nx][ny].flagged == True:
                flags += 1
            if squares[nx][ny].opened == False:
                sqs += 1
    if flags == squares[x][y].value:
        squares = openAdj(squares, x, y)
        return squares
    if sqs == squares[x][y].value:
        for a, b in zip(xmap, ymap):
            nx, ny = x + a, y + b
            if nx >= 0 and nx < 16 and ny >= 0 and ny < 12:
                if squares[nx][ny].flagged == False and squares[nx][ny].opened == False:
                    squares[nx][ny].flag()
    return squares
            
def minesLeft(squares):
    mines = MINES
    for a in squares:
        for b in a:
            if b.flagged == True:
                mines -= 1
    return mines

def openAll(squares):
    for a in squares:
        for b in a:
            b.open()

def state(squares):
    unopened = 0
    for a in squares:
        for b in a:
            if b.opened == False:
                unopened += 1
            if b.opened == True and b.value == -1:
                openAll(squares)
                b.lost()
                return -1
    
    if unopened == MINES:
        return 1
    else:
        return 0