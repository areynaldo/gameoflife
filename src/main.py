import pygame
import random
import copy

def countNeighbours(cells, x, y):
    count = 0
    #N
    if y > 0:
        if cells[y-1][x]:
            count += 1
    #S
    if y < len(cells)-1:
        if cells[y+1][x]:
            count += 1
    #E
    if x > 0:
        if cells[y][x-1]:
            count += 1
    #W
    if x < len(cells[0])-1:
        if cells[y][x+1]:
            count += 1
    #NE
    if y > 0 and x < len(cells[0])-1:
        if cells[y-1][x+1]:
            count += 1
    #SE
    if y < len(cells)-1 and x < len(cells[0])-1:
        if cells[y+1][x+1]:
            count += 1
    #SE
    if y < len(cells)-1 and x > 0:
        if cells[y+1][x-1]:
            count += 1
    #NW
    if y > 0 and x > 0:
        if cells[y-1][x-1]:
            count += 1

    return count

#Table class
class Cgol():
    screen      = 0
    pause       = 0
    changing    = 0
    cells       = 0
    dt          = 0
    lastcell    = 0

    def __init__(self, w, h, screen):
        self.pause      = True
        self.changing   = False
        self.screen     = screen
        self.dt         = 0
        self.cells      = []
        self.lastcell   = (-1,-1)

        for i in range(0, h):
            self.cells.append([])
            for j in range(0, w):
                self.cells[i].append(False)

    def draw(self):
        h = self.screen.get_height() / len(self.cells)
        w = self.screen.get_width() / len(self.cells[0])

        for y in range(0, len(self.cells)):
            for x in range(0, len(self.cells[y])):
                if self.cells[y][x]:
                    pygame.draw.rect(self.screen, (0, 0, 0), pygame.Rect(x*w, y*h, w, h))
                elif not self.cells[y][x]:
                    pygame.draw.rect(self.screen, (255,255,255), pygame.Rect(x*w, y*h, w, h))
                pygame.draw.rect(self.screen, (200,200,200), pygame.Rect(x*w, y*h, w, h), 2)

    def changeCells(self):
        h = self.screen.get_height() / len(self.cells)
        w = self.screen.get_width() / len(self.cells[0])

        for y in range(0, len(self.cells)):
            for x in range(0, len(self.cells[y])):
                if self.lastcell != (x, y):
                    rect = pygame.Rect(x*w, y*h, w, h)
                    if rect.collidepoint(pygame.mouse.get_pos()):
                        self.cells[y][x] = False if self.cells[y][x] else True
                        self.lastcell = (x, y)

    def update(self, clock):
        if self.changing:
            self.changeCells()
        else:
            self.lastcell = (-1, -1)

        if not self.pause:
            self.dt += clock.get_time()
            print(self.dt)
            if self.dt >= 100:
                self.dt = 0
                self.nextGen()

    def nextGen(self):
        oldcells = [i[:] for i in self.cells]
        for y in range(0, len(oldcells)):
            for x in range(0, len(oldcells[y])):
                neighbours = countNeighbours(oldcells, x, y)
                if oldcells[y][x]:
                    if neighbours > 3 or neighbours < 2:
                        self.cells[y][x] = False
                elif not oldcells[y][x]:
                    if neighbours == 3:
                        self.cells[y][x] = True
                    
    def addCells(self):
        for i in self.cells:
            i.append(False)
            i.insert(0, False)
        self.cells.append([False for i in range(0, len(self.cells[0]))])
        self.cells.insert(0, [False for i in range(0, len(self.cells[0]))])

    def remCells(self):
        for i in self.cells:
            i.pop()
            i.pop(0)
        self.cells.pop()
        self.cells.pop(0)


def main():

    pygame.init()
    destSurface = pygame.display.set_mode((720, 720), pygame.RESIZABLE)
    srcSurface  = destSurface.copy()
    grunning    = True
    clock       = pygame.time.Clock()
    gol         = Cgol(48,48, srcSurface)

    while grunning:
        clock.tick(60)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                    grunning = False
            #Mouse
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button == 1:
                    gol.changing = True
            if ev.type == pygame.MOUSEBUTTONUP:
                if ev.button == 1:
                    gol.changing = False;
            #Keyboard
            if ev.type == pygame.KEYDOWN:
                if ev.key == pygame.K_SPACE:
                    gol.pause = False if gol.pause else True
                if ev.key == pygame.K_RIGHT:
                    gol.nextGen()
                if ev.key == pygame.K_UP:
                    gol.addCells()
                if ev.key == pygame.K_DOWN:
                    gol.remCells()

        gol.update(clock)
        gol.draw()
        destSurface.blit(srcSurface, (0,0))
        pygame.display.flip()

if __name__ == "__main__":
    main()