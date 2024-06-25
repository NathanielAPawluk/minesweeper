import pygame, sys
from square import Square
import boardState

pygame.init()

W = 600
H = 800
SQSIZE = 50
VOFFSET = 80
MINES = 40
COLS = int(W/SQSIZE)
ROWS = int(H/SQSIZE)
path = sys.argv[0].strip("minesweeper.py")

#Constant game variables
screen = pygame.display.set_mode((W,H + VOFFSET))
pygame.display.set_caption("Minesweeper")
running = True
clock = pygame.time.Clock()
font = pygame.font.SysFont('Cooper Black', 28)

#Game pieces/info
gameStarted = False
lost = False
win = False
squares = [["" for _ in range(COLS)] for _ in range(ROWS)]
icon = pygame.image.load(f"{path}/assets/faceN.png")
iconRect = pygame.Rect(275, 15, 50, 50)
for i in range(ROWS):
    for j in range(COLS):
        squares[i][j] = Square(j*SQSIZE, i*SQSIZE + VOFFSET, j, i, SQSIZE, 0)

while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        #Game Restart
        if event.type == pygame.MOUSEBUTTONUP:
            if iconRect.collidepoint(pygame.mouse.get_pos()):
                gameStarted = False
                lost = False
                win = False
                squares = [["" for _ in range(COLS)] for _ in range(ROWS)]
                icon = pygame.image.load(f"{path}/assets/faceN.png")
                for i in range(ROWS):
                    for j in range(COLS):
                        squares[i][j] = Square(j*SQSIZE, i*SQSIZE + VOFFSET, j, i, SQSIZE, 0)

        try:
            if pygame.mouse.get_pressed()[0] == True and lost == False:
                pos = pygame.mouse.get_pos()
                clicked = []
            
                for a in range(16):
                        for b in range(12):
                            if squares[a][b].rect.collidepoint(pos):
                                clicked.append(squares[a][b])
                                startPoint = (a, b)
                                break
                
                if gameStarted == False:
                    board = boardState.buildBoard(clicked[0].col, clicked[0].row)
                    for i in range(ROWS):
                        for j in range(COLS):
                            squares[i][j].value = board[i][j]
                    gameStarted = True

                if clicked[0].value == 0:
                    boardState.openAdj(squares, *startPoint)
                elif clicked[0].flagged == True:   
                    pass
                else:
                    clicked[0].open()
            
            if pygame.mouse.get_pressed()[2] == True:
                pos = pygame.mouse.get_pos()
                for a in range(16):
                        for b in range(12):
                            if squares[a][b].rect.collidepoint(pos):
                                if squares[a][b].opened == True:
                                    squares = boardState.chord(squares, a, b)
                                else:
                                    squares[a][b].flag()
            if lost == True or win == True:
                pygame.display.flip()
            else:
                if boardState.state(squares) == -1:
                    lost = True
                    icon = pygame.image.load(f"{path}/assets/faceL.png")
                elif boardState.state(squares) == 1:
                    win = True
                    icon = pygame.image.load(f"{path}/assets/faceW.png")
                pygame.display.flip()
        except IndexError:
            pass    

        screen.fill("gray90")
        MINES = boardState.minesLeft(squares)
        screen.blit(font.render(f"Mines left: {MINES}", 1, "black"), [10, 20])
        screen.blit(icon, iconRect)

        for a in squares:
            for b in a:
                b.render(screen)
    
