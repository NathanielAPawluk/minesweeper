import pygame

class Square(pygame.sprite.Sprite):
    def __init__(self, x, y, row, col, SQSIZE, value):
        self.textColors = {
            0: "red",
            1: "blue",
            2: "green",
            3: "red",
            4: "darkblue",
            5: "darkred",
            6: "cyan4",
            7: "darkorchid3",
            8: "gray30"
        }
        pygame.sprite.Sprite.__init__(self)
        pygame.init()
        self.font = pygame.font.SysFont('Cooper Black', 28)
        self.x = x
        self.y = y
        self.w = SQSIZE
        self.h = SQSIZE
        self.row = row
        self.col = col
        self.value = value
        self.image = pygame.image.load("unopened.png")
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.opened = False
        self.flagged = False
        self.text = self.font.render(str(self.value), 1, self.textColors[self.value])
        self.textw, self.texth = self.font.size(str(self.value))
        self.xoffset, self.yoffset = (self.w-self.textw) // 2, (self.h-self.texth) // 2
        self.center = [self.x + self.xoffset, self.y + self.yoffset]

    def render(self, screen):
        screen.blit(self.image, self.rect)
        if self.opened and self.value != 0 and self.value != -1:
            screen.blit(self.text, self.center)            

    def open(self):
        self.opened = True
        self.image = pygame.image.load("opened.png")
        if self.value != -1:
            self.text = self.font.render(str(self.value), 1, self.textColors[self.value])
        else:
            self.image = pygame.image.load("mine.png")
    
    def flag(self):
        if self.opened == False:
            if self.flagged == True:
                self.flagged = False
                self.image = pygame.image.load("unopened.png")
                return
            self.flagged = True
            self.image = pygame.image.load("flag.png")
        
    
    def lost(self):
        self.image = pygame.image.load("openMine.png")
